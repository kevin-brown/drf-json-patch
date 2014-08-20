from rest_framework import mixins, response
from jsonpatch import JsonPatch, JsonPatchException, RemoveOperation
from django.utils.encoding import force_text
import sys


class JsonPatchMixin(object):

    def partial_update(self, request, *args, **kwargs):
        patch = JsonPatch(request.DATA)
        obj = self.get_object()

        serializer = self.get_serializer(instance=obj)
        doc = serializer.data

        try:
            # `jsonpatch` does not force documents to be array of operations
            # So we have to do it manually
            if not isinstance(request.DATA, list):
                raise JsonPatchException(
                    "The patch must be supplied as a list",
                )

            modified = patch.apply(doc)

            # Set the modified data to the request data
            # This will allow us to update the object using it

            request._data = modified

            return super(JsonPatchMixin, self).update(request, *args, **kwargs)
        except JsonPatchException as ex:
            message = force_text(ex)

            # `jsonpatch` does not handle unicode transparently
            # So we have to strip out the `u'` in Python 2
            if "Unknown operation u'" in message and sys.version_info < (3, 0):
                message = message.replace("u'", "'")

            data = {
                "detail": message,
            }

            return response.Response(data, status=400)


class PartialPutMixin(mixins.UpdateModelMixin):

    def update(self, *args, **kwargs):
        kwargs["partial"] = True

        return super(PartialPutMixin, self).update(*args, **kwargs)
