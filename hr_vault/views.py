from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import EmployeeRecord


@login_required
def add_employee(request):
    if request.method == "POST":
        employee_name = (request.POST.get("employee_name") or "").strip()
        department = (request.POST.get("department") or "").strip()
        bank_account_number = (request.POST.get("bank_account_number") or "").strip()
        annual_salary_raw = (request.POST.get("annual_salary") or "").strip()

        # Minimal validation so the view does not crash.
        if not employee_name or not department or not bank_account_number or not annual_salary_raw:
            return render(
                request,
                "add_employee.html",
                {
                    "error": "All fields are required.",
                },
                status=400,
            )

        try:
            annual_salary = Decimal(annual_salary_raw)
        except Exception:
            return render(
                request,
                "add_employee.html",
                {
                    "error": "Annual salary must be a valid number.",
                },
                status=400,
            )

        with transaction.atomic():
            EmployeeRecord.objects.create(
                employee_name=employee_name,
                department=department,
                bank_account_number=bank_account_number,
                annual_salary=annual_salary,
                added_by=request.user,
            )

        return redirect("hr_vault:list_employees")

    return render(request, "add_employee.html")


@login_required
def list_employees(request):
    employees = EmployeeRecord.objects.select_related("added_by").order_by("-id")
    return render(request, "hr_vault/list_employees.html", {"employees": employees})

def home(request):
    return HttpResponse("Welcome to the HR Vault. Go to /hr/list/ to view employee records.")
