from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create your views here.

def login_view(request):
    # ?next=/articles/create -> future item?
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
            # commetted out all of this once we changed to the AuthenticationForm method above
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        # # print(username, password)
        # user = authenticate(request, username=username, password=password)
        # if user is None:
        #     context = {"error": "Invalid username or password."}
        #     return render(request, "accounts/login.html", context=context)
        # login(request,user)

    else:
        form = AuthenticationForm(request)
    context = {
        "form": form
    }
    return render(request, "accounts/login.html", context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/login/')
    return render(request, "accounts/logout.html", {})

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('/login')
    context = {
        "form": form
    }
    return render(request, "accounts/register.html", context)