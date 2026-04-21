from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import DatabaseError
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from tickets.models import Department, Employee, Ticket

from .forms import (
    DepartmentForm,
    EmployeeForm,
    ResolutionForm,
    TicketForm,
    UserRegistrationForm,
)

# Create your views here.


def register_view(request):
    if request.user.is_authenticated:
        return redirect("ticket-list")

    form = UserRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("employee-create")

    return render(request, "registration/register.html", {"form": form})


@login_required
def ticket_create_view(request):
    if not hasattr(request.user, "employee"):
        return redirect("employee-create")

    form = TicketForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.who_opened = request.user.employee
            ticket.save()
            return redirect("ticket-detail", pk=ticket.pk)

    return render(request, "ticket_create.html", {"form": form})


@login_required
def employee_create_view(request):
    if hasattr(request.user, "employee"):
        return redirect("ticket-create")

    form = EmployeeForm()

    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                employee = form.save(commit=False)
                employee.user = request.user
                employee.save()
                return redirect("ticket-create")
            except DatabaseError:
                form.add_error(
                    None,
                    "An error occurred while creating the employee profile. Please try again.",
                )

    return render(request, "employee_create.html", {"form": form})


class TicketListView(LoginRequiredMixin, generic.ListView):
    model = Ticket
    template_name = "ticket_list.html"
    context_object_name = "tickets"
    ordering = ["-created_at"]
    paginate_by = 15

    def get_template_names(self):
        if self.request.headers.get("HX-Request") == "true":
            return ["partials/ticket_list_content.html"]
        return [self.template_name]

    def get_queryset(self):
        queryset = (
            Ticket.objects.select_related("who_opened__user", "who_opened__department")
            .order_by("-created_at")
        )

        query = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "").strip()
        priority = self.request.GET.get("priority", "").strip()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(who_opened__user__username__icontains=query)
            )

        if status in {"open", "in_progress", "closed"}:
            queryset = queryset.filter(status=status)

        if priority in {"low", "medium", "high"}:
            queryset = queryset.filter(priority=priority)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["filters"] = {
            "q": self.request.GET.get("q", "").strip(),
            "status": self.request.GET.get("status", "").strip(),
            "priority": self.request.GET.get("priority", "").strip(),
        }
        context["stats"] = {
            "total": queryset.count(),
            "open": queryset.filter(status="open").count(),
            "in_progress": queryset.filter(status="in_progress").count(),
            "closed": queryset.filter(status="closed").count(),
        }
        context["list_title"] = "All Tickets"
        context["list_subtitle"] = (
            "Monitor requests across every department in one operational dashboard."
        )
        context["filter_url"] = reverse_lazy("ticket-list")
        return context


class MyTicketsListView(LoginRequiredMixin, generic.ListView):
    model = Ticket
    template_name = "ticket_list.html"
    context_object_name = "tickets"
    ordering = ["-created_at"]
    paginate_by = 10

    def get_template_names(self):
        if self.request.headers.get("HX-Request") == "true":
            return ["partials/ticket_list_content.html"]
        return [self.template_name]

    def get_queryset(self):
        queryset = (
            Ticket.objects.select_related("who_opened__user", "who_opened__department")
            .filter(who_opened__user=self.request.user)
            .order_by("-created_at")
        )

        query = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "").strip()
        priority = self.request.GET.get("priority", "").strip()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        if status in {"open", "in_progress", "closed"}:
            queryset = queryset.filter(status=status)

        if priority in {"low", "medium", "high"}:
            queryset = queryset.filter(priority=priority)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["filters"] = {
            "q": self.request.GET.get("q", "").strip(),
            "status": self.request.GET.get("status", "").strip(),
            "priority": self.request.GET.get("priority", "").strip(),
        }
        context["stats"] = {
            "total": queryset.count(),
            "open": queryset.filter(status="open").count(),
            "in_progress": queryset.filter(status="in_progress").count(),
            "closed": queryset.filter(status="closed").count(),
        }
        context["list_title"] = "My Tickets"
        context["list_subtitle"] = "Focus on the requests you created and their live progress."
        context["filter_url"] = reverse_lazy("my-tickets")
        return context


class TicketDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ticket
    template_name = "ticket_detail.html"
    context_object_name = "ticket"

    def get_is_technician(self):
        user = self.request.user
        return (
            hasattr(user, "employee")
            and user.employee.position.lower() == "technician"
        )

    def get_object(self, queryset=None):
        ticket = super().get_object(queryset)
        user = self.request.user

        has_profile = hasattr(user, "employee")
        is_owner = has_profile and ticket.who_opened.user == user
        is_tech = self.get_is_technician()

        if is_owner or is_tech:
            return ticket

        raise PermissionDenied("Access denied.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = self.get_object()
        is_tech = self.get_is_technician()
        context["is_technician"] = is_tech
        context["resolutions"] = ticket.resolutions.select_related("technician__user").all()
        if is_tech and ticket.status != "closed":
            context["resolution_form"] = ResolutionForm()
        return context

    def post(self, request, *args, **kwargs):
        if not self.get_is_technician():
            raise PermissionDenied("Only technicians can resolve tickets.")

        self.object = self.get_object()
        form = ResolutionForm(request.POST)

        if form.is_valid():
            resolution = form.save(commit=False)
            resolution.ticket = self.object
            resolution.technician = request.user.employee
            resolution.save()

            self.object.status = "closed"
            self.object.save()

            return redirect("ticket-detail", pk=self.object.pk)

        context = self.get_context_data(object=self.object)
        context["resolution_form"] = form
        return self.render_to_response(context)


class DepartmentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "department_create.html"
    success_url = reverse_lazy("ticket-list")


class TicketUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = "ticket_update.html"
    success_url = reverse_lazy("ticket-list")

    def get_object(self, queryset=None):
        ticket = super().get_object(queryset)
        user = self.request.user

        has_profile = hasattr(user, "employee")
        is_owner = has_profile and ticket.who_opened.user == user

        if is_owner:
            return ticket

        raise PermissionDenied("Access denied.")


class EmployeeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "employee_update.html"
    success_url = reverse_lazy("ticket-list")

    def get_object(self, queryset=None):
        user = self.request.user

        if hasattr(user, "employee"):
            return user.employee

        raise PermissionDenied("Access denied.")
