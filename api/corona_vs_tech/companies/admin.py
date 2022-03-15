from django.contrib import admin

from api.corona_vs_tech.companies.models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_filter = ["status"]
    list_display = ["name", "status", "last_update"]


admin.site.register(Company, CompanyAdmin)
