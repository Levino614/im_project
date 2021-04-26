from django.shortcuts import render, redirect
from erpapp.forms import EmployeeForm
from erpapp.models import Employee
from erpapp.models import Assignment
from erpapp.models import Project
from erpapp.models import Chair
from erpapp.models import Position
from erpapp.models import Task


# Create your views here.
def index(request):
    return render(request, 'index.html')


def employee(request):
    employees = Employee.objects.all()
    return render(request, 'employee.html', {'employees': employees})


def add_new_emp(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = EmployeeForm()
    context = {
        'form': form
    }
    return render(request, 'add_new_emp.html', context)


def edit_emp(request, id):
    employee = Employee.objects.get(id=id)
    context = {
        'employee': employee
    }
    return render(request, 'edit_emp.html', context)


def update_emp(request, id):
    employee = Employee.objects.get(id=id)
    form = EmployeeForm(request.POST, instance=employee)
    if form.is_valid():
        form.save()
        return redirect('/')
    context = {
        'employee': employee
    }
    return render(request, 'edit_emp.html', context)


def delete_emp(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect('/')


def overview(request):
    employees = Employee.objects.all()
    assignments = Assignment.objects.all()
    projects = Project.objects.all()
    chairs = Chair.objects.all()
    positions = Position.objects.all()
    tasks = Task.objects.all()
    employeeprojects = []

    for employee in employees:
        employee_prj_hours = []
        employee_prj_hours_id = []
        for project in projects:
            for assignment in assignments:
                if assignment.task.id == project.id and assignment.employee.id == employee.id:
                    employee_prj_hours.append(assignment.percentage)
                    employee_prj_hours_id.append(project.id)
        employee_list = []
        employee_list.append(employee)
        for project in projects:
            if project.id in employee_prj_hours_id:
                employee_list.append(employee_prj_hours[employee_prj_hours_id.index(project.id)])
            else: employee_list.append(0)

        employeeprojects.append(employee_list)
    print(employeeprojects)




    context = {
        'employees': employees,
        'assignments': assignments,
        'projects': projects,
        'chairs': chairs,
        'positions': positions,
        'employeeprojects': employeeprojects
    }
    print("-----------")
    for task in tasks:
        print(str(task) + ", id: " + str(task.id))
    return render(request, 'Overview/overview.html', context)
