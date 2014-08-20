"""
Test JSON Patch
"""

from django.core.urlresolvers import reverse
from rest_framework_json_patch import mixins
from rest_framework import serializers, viewsets
from tests import models
import json
import pytest

pytestmark = pytest.mark.django_db


class TestViewSet(mixins.JsonPatchMixin, viewsets.ModelViewSet):
    model = models.TestModel


class NestedSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("name", "children", )
        model = models.FullNested


class NestedViewSet(mixins.JsonPatchMixin, viewsets.ModelViewSet):
    model = models.FullNested
    serializer_class = NestedSerializer


view = TestViewSet.as_view({"patch": "partial_update"})
nested_view = NestedViewSet.as_view({"patch": "partial_update"})


def test_invalid_data(rf):
    obj = models.TestModel.objects.create(something="test", other="test")

    data = json.dumps({
        "invalid": "data",
    })
    result_data = {
        "detail": "The patch must be supplied as a list",
    }

    request = rf.patch(
        "testing",
        data=data,
        content_type="application/json",
    )

    response = view(request, pk=obj.pk)
    response.render()

    assert response.status_code == 400
    assert response.data == result_data


def test_invalid_operation(rf):
    obj = models.TestModel.objects.create(something="test", other="test")

    data = json.dumps([{
        "op": "invalid",
    }])
    result_data = {
        "detail": "Unknown operation 'invalid'",
    }

    request = rf.patch(
        "testing",
        data=data,
        content_type="application/json",
    )

    response = view(request, pk=obj.pk)
    response.render()

    assert response.status_code == 400
    assert response.data == result_data


def test_replace(rf):
    obj = models.TestModel.objects.create(something="test", other="test")

    data = json.dumps([{
        "op": "replace",
        "path": "/something",
        "value": "other"
    }])
    result_data = {
        "id": obj.pk,
        "other": "test",
        "something": "other",
    }

    request = rf.patch(
        "testing",
        data=data,
        content_type="application/json",
    )

    response = view(request, pk=obj.pk)
    response.render()

    assert response.status_code == 200
    assert response.data == result_data


def test_copy(rf):
    obj = models.TestModel.objects.create(something="initial", other="test")

    data = json.dumps([{
        "op": "copy",
        "path": "/other",
        "from": "/something"
    }])
    result_data = {
        "id": obj.pk,
        "other": "initial",
        "something": "initial",
    }

    request = rf.patch(
        "testing",
        data=data,
        content_type="application/json",
    )

    response = view(request, pk=obj.pk)
    response.render()

    assert response.status_code == 200
    assert response.data == result_data


def test_add(rf):
    obj = models.FullNested.objects.create(name="test")
    nested = models.ChildNested.objects.create(title="test")

    data = json.dumps([{
        "op": "add",
        "path": "/children",
        "value": [nested.pk],
    }])
    result_data = {
        "name": "test",
        "children": [nested.pk],
    }

    request = rf.patch(
        "testing",
        data=data,
        content_type="application/json",
    )

    response = nested_view(request, pk=obj.pk)
    response.render()

    assert response.status_code == 200
    assert response.data == result_data


def test_remove(rf):
    obj = models.FullNested.objects.create(name="test")
    nested = models.ChildNested.objects.create(title="test")
    obj.children.add(nested)

    data = json.dumps([{
        "op": "remove",
        "path": "/children",
        "value": [nested.pk],
    }])
    result_data = {
        "name": "test",
        "children": [],
    }

    request = rf.patch(
        "testing",
        data=data,
        content_type="application/json",
    )

    response = nested_view(request, pk=obj.pk)
    response.render()

    assert response.status_code == 200
    assert response.data == result_data
