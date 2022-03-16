from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.corona_vs_tech.companies.models import Company
from api.corona_vs_tech.companies.serializers import (
    CompanySerializer,
    EmailSerializer,
)


def title_name(request: Request, serializer: Serializer):
    """
    Capitalize the first characters of each word in the company name.

    :param request: the Request object
    :param serializer: the serializer classes
    """
    serializer.validated_data["name"] = request.data["name"].title()


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            title_name(request, serializer)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        Override the partial_update method. Basically, calling the
        `title_name` function before saving the object instance.

        :param request: Request object
        :type request: Request
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            title_name(request, serializer)
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class EmailView(APIView):
    serializer_class = EmailSerializer

    def post(self, request):
        """
        Send an email.

        from: chaungoc.le1995@gmail.com

        to: playerzawesome@gmail.com
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()

        subject = serializer.validated_data.get("subject")
        body = serializer.validated_data.get("message")

        mail = EmailMessage(
            subject=subject,
            body=body,
            to=["playerzawesome@gmail.com"],
        )
        mail.send()

        return Response(
            {"status": "Success", "message": "Email was sent successfully!"},
            status.HTTP_200_OK,
        )
