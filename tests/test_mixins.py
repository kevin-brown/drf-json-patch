"""
Test mixins

Based on the original tests submitted by @jwhitlock for DRF JSON API.

https://github.com/jwhitlock/drf-json-api/blob/6f9de442a5d7ec72970fae3132c7870a0bf0ce13/tests/test_mixin.py
"""

from django.core.urlresolvers import reverse
from rest_framework_json_patch import mixins
from rest_framework import viewsets
from tests import models
import json
import pytest

pytestmark = pytest.mark.django_db


class TestViewSet(viewsets.ModelViewSet):
    model = models.TestModel


def test_drf_put_partial_fails(rf):
    obj = models.TestModel.objects.create(something="test", other="test")

    data = json.dumps({
        "something": "another",
    })
    result_data = {
        "other": ["This field is required."],
    }

    request = rf.put(
        "testing",
        data=data,
        content_type="application/json",
    )

    view = TestViewSet.as_view({'put': 'update'})
    response = view(request, pk=obj.pk)
    response.render()

    assert response.status_code == 400
    assert response.data == result_data


def test_json_api_put_partial_success(rf):
    class PartialPutTestViewSet(mixins.PartialPutMixin, TestViewSet):
        pass

    obj = models.TestModel.objects.create(something="test", other="test")

    data = json.dumps({
        "something": "another",
    })
    result_data = {
        "id": obj.pk,
        "something": "another",
        "other": "test",
    }

    request = rf.put(
        "testing",
        data=data,
        content_type="application/json",
    )

    view = PartialPutTestViewSet.as_view({'put': 'update'})
    response = view(request, pk=obj.pk)
    response.render()

    assert response.status_code == 200
    assert response.data == result_data
