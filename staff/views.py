from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.contrib import messages
from register.forms import RegisterForm
from register.models import UserDetails
from payapp.models import Transaction
from payapp.models import MoneyRequest
from staff.forms import AdminRegisterForm
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def viewStaffHome(request):
    return render(request, "staffHome.html")
@staff_member_required
def viewUsers(request):
    userDetails = UserDetails.objects.all()
    return render(request, "users.html", {'users': userDetails})
@staff_member_required
def viewTransactions(request):
    transactionDetails = Transaction.objects.all().order_by('-timestamp')
    return render(request, "allTransactions.html", {'transactions': transactionDetails})
@staff_member_required
def viewRequests(request):
    requests = MoneyRequest.objects.all().order_by('-timestamp')
    return render(request, "requests.html", {'requests': requests})
@staff_member_required
def adminRegister(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_superuser = True
            user.is_staff = True
            user.save()
            return redirect("staffHome")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'adminRegister.html', {"register_user": AdminRegisterForm()})