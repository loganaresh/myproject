from django.shortcuts import render, redirect
from .forms import EmployeeRegistrationForm
from .models import Employee
from django.contrib.auth.hashers import make_password, check_password

def register(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.password = make_password(employee.password)  
            employee.save()
            return redirect('login')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        try:
            employee = Employee.objects.get(name=name)
            if check_password(password, employee.password):
                return render(request, 'profile.html', {'employee': employee})
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials'})
        except Employee.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')
