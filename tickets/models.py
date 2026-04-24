from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    @property
    def has_employee_profile(self):
        return hasattr(self, "employee")

    @property
    def is_technician(self):
        return self.has_employee_profile and self.employee.is_technician

    @property
    def can_manage_departments(self):
        return self.is_superuser or self.is_staff or self.is_technician

    @property
    def can_view_all_tickets(self):
        return self.is_authenticated and (
            self.is_superuser or self.is_staff or self.is_technician
        )

    def can_edit_ticket(self, ticket):
        if not self.is_authenticated:
            return False

        if self.is_superuser or self.is_staff:
            return True

        return (
            self.has_employee_profile and ticket.who_opened_id == self.employee.id
        )


class Department(models.Model):
    name = models.CharField(max_length=155)
    localization = models.CharField(max_length=155)
    chief_of_department = models.CharField(max_length=155)

    def __str__(self):
        return (
            f"{self.name} - {self.localization} - {self.chief_of_department}"
        )


class Employee(models.Model):
    class Position(models.TextChoices):
        ANALYST = "analyst", "Analyst"
        TECHNICIAN = "technician", "Technician"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(
        max_length=20,
        choices=Position.choices,
        default=Position.ANALYST,
    )
    phone_number = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    @property
    def is_technician(self):
        return self.position == self.Position.TECHNICIAN


class Ticket(models.Model):
    title = models.CharField(max_length=155)
    description = models.TextField()
    priority = models.CharField(
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        max_length=20,
        default="medium",
    )
    status = models.CharField(
        choices=[
            ("open", "Open"),
            ("in_progress", "In Progress"),
            ("closed", "Closed"),
        ],
        max_length=20,
        default="open",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    who_opened = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="opened_tickets"
    )

    def __str__(self):
        return f"{self.title} - {self.priority} - {self.status}"


class Resolution(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="resolutions"
    )
    technician = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="resolved_tickets"
    )
    comment = models.TextField()
    spent_time = models.DurationField()
