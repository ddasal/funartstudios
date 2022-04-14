from django.contrib.auth.decorators import login_required, permission_required
from django.http import request
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm
from accounts.models import FileUpload

from events.models import User
from .forms import UserProfile, UserForm, UserProfileForm, RegisterForm
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

# Create your views here.

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            try:
                valuenext = request.GET['next']
                # valuenext = request.path
                return redirect(valuenext)
            except:
                return redirect('/')

    else:
        form = AuthenticationForm(request)

    context = {
        "form": form
    }
    return render(request, "accounts/login.html", context)

@login_required
def logout_view(request):
    # added to shortcut logging out
    logout(request)
    return redirect('/account/login/')
    #making the if request invalid, but leaving for now
    if request.method == "POST":
        logout(request)
        return redirect('/account/login/')
    return render(request, "accounts/logout.html", {})

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/account/login/')
    context = {
        "form": form
    }
    return render(request, "accounts/register.html", context)

def change_password_view(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
        user_obj = form.save()
        return redirect('/')
    context = {
        "form": form
    }
    return render(request, "accounts/change-password.html", context)

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # messages = None
            # messages.success(request, _('New user created successfully'))
            return redirect('/account/staff/')
        else:
            pass
            # messages = None
            # messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'accounts/user-profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@permission_required('accounts.change_userprofile')
def profile_admin_update_view(request, id=None):
    obj = get_object_or_404(UserProfile, id=id)
    user_form = UserForm(request.POST or None, instance=obj.user)
    profile_form = UserProfileForm(request.POST or None, instance=obj)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "object": obj,
    }
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        context['message'] = 'Staff data saved.'

    if request.htmx:
        return render(request, "accounts/partials/forms.html", context)
    return render(request, "accounts/admin-user-profile.html", context) 

@permission_required('accounts.view_userprofile')
def account_list_view(request):
    qs = UserProfile.objects.filter(active=True).order_by('user__last_name', 'user__first_name')
    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 10)
    account_count = paginator.count
    try:
        accounts = paginator.page(page)
    except PageNotAnInteger:
        accounts = paginator.page(1)
    except EmptyPage:
        accounts = paginator.page(paginator.num_pages)
    context = {
        "accounts": accounts,
        "account_count": account_count
    }
    return render(request, "accounts/list.html", context)

@permission_required('accounts.view_fileupload')
def staff_file_list_view(request):
    qs = FileUpload.objects.filter(active=True).order_by('category__title', 'title')
    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 10)
    fileuploads_count = paginator.count
    try:
        fileuploads = paginator.page(page)
    except PageNotAnInteger:
        fileuploads = paginator.page(1)
    except EmptyPage:
        accofileuploadsunts = paginator.page(paginator.num_pages)
    context = {
        "fileuploads": fileuploads,
        "fileuploads_count": fileuploads_count
    }
    return render(request, "accounts/files.html", context)
