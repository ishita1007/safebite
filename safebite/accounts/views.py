from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

from details.models import UserAllergen, allergenlist

from .forms import CustomUserCreationForm


def login(request):
    print("Hiii")
    if request.method=="POST":
        user_name=request.POST["user_name"]
        password1=request.POST["password1"]
        user=auth.authenticate(username=user_name,password=password1)
        if user is not None:
            print("how r u")
            print (user)
            auth.login(request,user)
            return redirect("fooddir")
        else:
            messages.info(request,"invalid credentials")
            return render(request,"login")

    else:
        return render(request,'login.html')   
# Create your views here.
# def register(request):
#     aller=""
#     if request.method=="POST":
       
#         first_name=request.POST["first_name"]
#         last_name=request.POST["last_name"]
#         user_name=request.POST["user_name"]
#         email=request.POST["email"]
#         password1=request.POST["password1"]
#         password2=request.POST["password2"]
#         if password1!=password2:
#             messages.info(request,"password incorrect")
#         else:
#             if User.objects.filter(username=user_name).exists():
#                 messages.info(request,"Username taken")
#             elif User.objects.filter(email=email).exists():
#                 messages.info(request,"Email taken")
#             else:
#                 user=User.objects.create_user(username=user_name,password=password1,email=email,first_name=first_name,last_name=last_name)
#                 print(user)
#                 user.save()
#                 messages.info(request,"user created")
#                 return redirect("login")
#         return redirect("register")
#     else:
#         return render(request,'register.html')
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.country = form.cleaned_data.get('country')
            user.profile.save()
            SelectedAllergen=allergenlist.objects.get(id="16")
            UserAllergen.objects.create(user=user, allergen=SelectedAllergen)
            
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect("/")
