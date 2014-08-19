from rest_framework import mixins


class JsonPatchMixin(object):
    pass


class PartialPutMixin(mixins.UpdateModelMixin):

    def update(self, *args, **kwargs):
        kwargs["partial"] = True

        return super(PartialPutMixin, self).update(*args, **kwargs)
