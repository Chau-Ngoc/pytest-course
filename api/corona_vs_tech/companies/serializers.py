from rest_framework import serializers

from api.corona_vs_tech.companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "status",
            "last_update",
            "application_link",
            "notes",
        ]

    # def save(self, **kwargs):
    #     name = self.validated_data["name"]
    #     name = name.title()
    #     return super().save(name=name)
