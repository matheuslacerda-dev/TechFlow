from django.urls import path

from .views import (
    DepartmentCreateView,
    EmployeeUpdateView,
    MyTicketsListView,
    TicketDetailView,
    TicketListView,
    TicketUpdateView,
    employee_create_view,
    register_view,
    ticket_create_view,
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("", TicketListView.as_view(), name="ticket-list"),
    path("create/", ticket_create_view, name="ticket-create"),
    path("my-tickets/", MyTicketsListView.as_view(), name="my-tickets"),
    path("employee/create/", employee_create_view, name="employee-create"),
    path("<int:pk>/", TicketDetailView.as_view(), name="ticket-detail"),
    path("<int:pk>/update/", TicketUpdateView.as_view(), name="ticket-update"),
    path(
        "department/create/",
        DepartmentCreateView.as_view(),
        name="department-create",
    ),
    path(
        "employee/profile/update/",
        EmployeeUpdateView.as_view(),
        name="employee-update",
    ),
]
