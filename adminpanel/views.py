from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from .forms import AdminLoginForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def adminlogin(request):
    # if 's_email' in request.session:
    #     return redirect('admin_dashbord')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None and user.is_superuser:

            request.session['s_email'] = email
            auth.login(request, user)
            print('admin logged in')
            messages.success(request, 'Successfully signed up!')
            return redirect('admin_dashboard')
        else:
            print('Not authorized')
            messages.error(request, 'Not autherised')
            return redirect('adminlogin')

    else:
        form = AdminLoginForm()
        dict_forms = {
            'form': form
        }

        return render(request, 'adminpanel/adminlogin.html', dict_forms)


# dashbord
def dashbord(request):

    return render(request, 'adminpanel/admindashboard.html')


def adminlogout(request):
    if 'email' in request.session:
        request.session.flush()
    auth.logout(request)
    return redirect('adminlogin')



def admin_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('adminlogin')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'adminpanel/admin_change_password.html')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'adminpanel/admin_change_password.html')




