from django.db import models
from django.utils.timezone import now


class Company(models.Model):
    class Meta:
        verbose_name_plural = "Companies"

    class CompanyStatus(models.TextChoices):
        LAYOFF = "Layoff"
        HIRING = "Hiring"
        HIRING_FREEZE = "Hiring Freeze"

    name = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        choices=CompanyStatus.choices,
        default=CompanyStatus.HIRING,
        max_length=50,
    )
    last_update = models.DateTimeField(default=now)
    application_link = models.URLField(max_length=200, blank=True)
    notes = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.name = f"{self.name}".title()
        self.last_update = now()
        return super().save(*args, **kwargs)
