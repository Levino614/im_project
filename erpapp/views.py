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
    employee_tasks = []
    employee_chairs_tasks = []
    employee_positions_tasks = []

    for employee in employees:  # For Project start
        employee_prj_hours = []
        employee_prj_hours_id = []
        for project in projects:
            for assignment in assignments:
                if assignment.task.id == project.id and assignment.employee.id == employee.id:
                    employee_prj_hours.append(assignment.percentage)
                    employee_prj_hours_id.append(project.id)
        employee_list_project = [employee]
        for project in projects:
            if project.id in employee_prj_hours_id:
                employee_list_project.append(employee_prj_hours[employee_prj_hours_id.index(project.id)])
            else:
                employee_list_project.append(0)

        employee_tasks.append(employee_list_project)  # For Project end

    for employee in employees: # Start for Chairs
        employee_ch_hours = []
        employee_ch_hours_id = []
        for chair in chairs:
            for assignment in assignments:
                if assignment.task.id == chair.id and assignment.employee.id == employee.id:
                    employee_ch_hours.append(assignment.percentage)
                    employee_ch_hours_id.append(chair.id)
        employee_list_chair = []
        for chair in chairs:
            if chair.id in employee_ch_hours_id:
                employee_list_chair.append(employee_ch_hours[employee_ch_hours_id.index(chair.id)])
            else:
                employee_list_chair.append(0)
        employee_chairs_tasks.append(employee_list_chair)

    i = 0
    while i < len(employee_tasks):
        j = 0
        while j < len(employee_chairs_tasks[i]):
            employee_tasks[i].append(employee_chairs_tasks[i][j])
            j = j + 1
        i = i + 1 # end for chairs

    # Start for positions
    for employee in employees:  # For Project start
        employee_pos_hours = []
        employee_pos_hours_id = []
        for position in positions:
            for assignment in assignments:
                if assignment.task.id == position.id and assignment.employee.id == employee.id:
                    employee_pos_hours.append(assignment.percentage)
                    employee_pos_hours_id.append(position.id)
        employee_list_position = []
        for position in positions:
            if position.id in employee_pos_hours_id:
                employee_list_position.append(employee_pos_hours[employee_pos_hours_id.index(position.id)])
            else:
                employee_list_position.append(0)
        employee_positions_tasks.append(employee_list_position)

    ii = 0
    while ii < len(employee_tasks):
        jj = 0
        while jj < len(employee_positions_tasks[ii]):
            employee_tasks[ii].append(employee_positions_tasks[ii][jj])
            jj = jj + 1
        ii = ii + 1  # end for positions




    print("hier: ")
    print(employee_positions_tasks)
    print("stop")

    context = {
        'employees': employees,
        'assignments': assignments,
        'projects': projects,
        'chairs': chairs,
        'positions': positions,
        'employeetasks': employee_tasks
    }
    print(employee_chairs_tasks)
    print(employee_tasks)
    print("-----------")
    for task in tasks:
        print(str(task) + ", id: " + str(task.id))
    return render(request, 'Overview/overview.html', context)
