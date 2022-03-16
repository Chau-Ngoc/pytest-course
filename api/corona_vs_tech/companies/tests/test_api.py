import json
import pytest

from django.urls import reverse

from api.corona_vs_tech.companies.models import Company

companies_url = reverse("companies-list")
pytestmark = pytest.mark.django_db


def test_zero_companies_should_return_empty_list(client):
    response = client.get(companies_url)

    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_create_one_companies_should_success(client):
    a_company = Company.objects.create(name="Amazon")

    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]

    assert response.status_code == 200
    assert response_content.get("name") == a_company.name
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


# --------------------Test POST request--------------------
def test_create_a_company_without_any_arguments_should_fail(client):
    response = client.post(companies_url)

    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}


def test_create_existing_company_should_fail(client):
    Company.objects.create(name="apple")
    response = client.post(companies_url, data={"name": "apple"})

    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["company with this name already exists."]
    }


def test_create_company_with_only_name_should_pass(client):
    """
    Test that create a company with only name field filled. All
    other fields should take their default values.
    """
    response = client.post(companies_url, data={"name": "Amazon"})
    response_content = json.loads(response.content)

    assert response.status_code == 201
    assert response_content["name"] == "Amazon"
    assert response_content["status"] == "Hiring"
    assert response_content["application_link"] == ""
    assert response_content["notes"] == ""


def test_create_company_with_wrong_status_should_fail(client):
    response = client.post(
        companies_url, {"name": "Test", "status": "test status"}
    )
    # print(response.content)
    assert response.status_code == 400
    assert "test status" in str(response.content)


def raise_covid19_exception():
    raise ValueError("Corona virus detected")


def test_raise_covid19_exception():
    with pytest.raises(ValueError) as error:
        raise_covid19_exception()
    # print(error.value)
    assert str(error.value) == "Corona virus detected"
