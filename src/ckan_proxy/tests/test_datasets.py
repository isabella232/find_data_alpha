from django.test import TestCase
from django.contrib.auth import get_user_model

from ckan_proxy.logic import datasets_for_user
from ckan_proxy.util import test_user_key


class DatasetsTestCase(TestCase):

    def setUp(self):
        pass
