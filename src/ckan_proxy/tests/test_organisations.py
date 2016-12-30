from django.test import TestCase
from django.contrib.auth import get_user_model

from ckan_proxy.logic import organization_list, organization_list_for_user
from ckan_proxy.util import test_user_key


class OrganisationTestCase(TestCase):

    def setUp(self):
        pass
