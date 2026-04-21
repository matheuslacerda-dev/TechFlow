from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Department, Employee, Resolution, Ticket


class RegistrationViewTests(TestCase):
    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create User Account")

    def test_register_creates_user_and_logs_in(self):
        payload = {
            "username": "new.user",
            "email": "new.user@company.com",
            "password1": "VeryStrongPass123!",
            "password2": "VeryStrongPass123!",
        }

        response = self.client.post(reverse("register"), data=payload)

        self.assertRedirects(response, reverse("employee-create"))
        user_model = get_user_model()
        created_user = user_model.objects.get(username="new.user")
        self.assertEqual(created_user.email, "new.user@company.com")
        self.assertEqual(str(created_user.pk), self.client.session.get("_auth_user_id"))

    def test_authenticated_user_is_redirected_from_register(self):
        user = get_user_model().objects.create_user(
            username="already.in",
            password="SomePassword123!",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("register"))

        self.assertRedirects(response, reverse("ticket-list"))


class TicketAccessAndResolutionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(
            name="Infra",
            localization="HQ-3F",
            chief_of_department="Morgan",
        )

        user_model = get_user_model()

        cls.owner_user = user_model.objects.create_user(
            username="owner",
            password="OwnerPass123!",
        )
        cls.owner_employee = Employee.objects.create(
            user=cls.owner_user,
            position="Analyst",
            phone_number="+1 111 111",
            department=cls.department,
        )

        cls.other_user = user_model.objects.create_user(
            username="other",
            password="OtherPass123!",
        )
        cls.other_employee = Employee.objects.create(
            user=cls.other_user,
            position="Analyst",
            phone_number="+1 222 222",
            department=cls.department,
        )

        cls.tech_user = user_model.objects.create_user(
            username="tech",
            password="TechPass123!",
        )
        cls.tech_employee = Employee.objects.create(
            user=cls.tech_user,
            position="Technician",
            phone_number="+1 333 333",
            department=cls.department,
        )

        cls.ticket = Ticket.objects.create(
            title="VPN down",
            description="Cannot connect to corporate VPN.",
            priority="high",
            status="open",
            who_opened=cls.owner_employee,
        )

    def test_ticket_create_redirects_to_employee_profile_when_missing(self):
        user_without_employee = get_user_model().objects.create_user(
            username="no.profile",
            password="NoProfilePass123!",
        )
        self.client.force_login(user_without_employee)

        response = self.client.get(reverse("ticket-create"))

        self.assertRedirects(response, reverse("employee-create"))

    def test_employee_create_creates_profile(self):
        user_without_employee = get_user_model().objects.create_user(
            username="new.employee",
            password="NewEmployeePass123!",
        )
        self.client.force_login(user_without_employee)

        payload = {
            "position": "Analyst",
            "phone_number": "+1 444 444",
            "department": self.department.pk,
        }
        response = self.client.post(reverse("employee-create"), data=payload)

        self.assertRedirects(response, reverse("ticket-create"))
        self.assertTrue(Employee.objects.filter(user=user_without_employee).exists())

    def test_ticket_detail_is_visible_to_owner(self):
        self.client.force_login(self.owner_user)

        response = self.client.get(reverse("ticket-detail", args=[self.ticket.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "VPN down")

    def test_ticket_detail_is_forbidden_for_non_owner_non_technician(self):
        self.client.force_login(self.other_user)

        response = self.client.get(reverse("ticket-detail", args=[self.ticket.pk]))

        self.assertEqual(response.status_code, 403)

    def test_non_technician_cannot_resolve_ticket(self):
        self.client.force_login(self.owner_user)

        payload = {
            "comment": "Tried local fix",
            "spent_time": "00:20:00",
        }
        response = self.client.post(
            reverse("ticket-detail", args=[self.ticket.pk]),
            data=payload,
        )

        self.assertEqual(response.status_code, 403)

    def test_technician_can_resolve_and_close_ticket(self):
        self.client.force_login(self.tech_user)

        payload = {
            "comment": "Reset VPN gateway and refreshed policy.",
            "spent_time": "01:15:00",
        }
        response = self.client.post(
            reverse("ticket-detail", args=[self.ticket.pk]),
            data=payload,
        )

        self.assertRedirects(response, reverse("ticket-detail", args=[self.ticket.pk]))

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, "closed")

        resolution = Resolution.objects.get(ticket=self.ticket)
        self.assertEqual(resolution.technician, self.tech_employee)
        self.assertEqual(resolution.comment, "Reset VPN gateway and refreshed policy.")
        self.assertEqual(resolution.spent_time, timedelta(hours=1, minutes=15))
