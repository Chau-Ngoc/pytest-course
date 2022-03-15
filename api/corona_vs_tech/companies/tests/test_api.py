import json
from unittest import TestCase

import pytest
from django.test.client import Client
from django.urls import reverse

from api.corona_vs_tech.companies.models import Company


@pytest.mark.django_db
class BaseCompanyAPITestCase(TestCase):
    def setUp(self):
        self.api_client = Client()
        self.companies_url = reverse("companies-list")

    def tearDown(self):
        pass


class TestGetCompanies(BaseCompanyAPITestCase):
    def test_zero_companies_should_return_empty_list(self):
        response = self.api_client.get(self.companies_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_create_one_companies_should_success(self):
        a_company = Company.objects.create(name="Amazon")

        response = self.api_client.get(self.companies_url)
        response_content = json.loads(response.content)[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name"), a_company.name)
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")


class TestPOSTCompany(BaseCompanyAPITestCase):
    def test_create_a_company_without_any_arguments_should_fail(self):
        response = self.api_client.post(self.companies_url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"name": ["This field is required."]},
        )

    def test_create_existing_company_should_fail(self):
        Company.objects.create(name="apple")
        response = self.api_client.post(
            self.companies_url, data={"name": "apple"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"name": ["company with this name already exists."]},
        )

    def test_create_company_with_only_name_should_pass(self):
        """
        Test that create a company with only name field filled. All
        other fields should take their default values.
        """
        response = self.api_client.post(
            self.companies_url, data={"name": "Amazon"}
        )
        response_content = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_content["name"], "Amazon")
        self.assertEqual(response_content["status"], "Hiring")
        self.assertEqual(response_content["application_link"], "")
        self.assertEqual(response_content["notes"], "")

    def test_create_company_with_wrong_status_should_fail(self):
        response = self.api_client.post(
            self.companies_url, {"name": "Test", "status": "test status"}
        )
        # print(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn("test status", str(response.content))


def raise_covid19_exception():
    raise ValueError("Corona virus detected")


def test_raise_covid19_exception():
    with pytest.raises(ValueError) as error:
        raise_covid19_exception()
    # print(error.value)
    assert str(error.value) == "Corona virus detected"
