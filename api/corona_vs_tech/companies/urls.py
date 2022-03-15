from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.corona_vs_tech.companies.views import CompanyViewSet

companies_router = DefaultRouter()
companies_router.register("companies", CompanyViewSet, basename="companies")

urlpatterns = [path("", include(companies_router.urls))]
