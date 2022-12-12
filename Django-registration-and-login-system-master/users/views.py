from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
import matplotlib.pyplot as plt
import io
import urllib, base64
import pandas as pd
import numpy as np
from datetime import datetime
import random
import matplotlib.dates as mdates
import json
from django.shortcuts import HttpResponse
import time

@login_required
def home(request):
    return render(request, 'users/home.html')

def EquipmentDetails(request):

# setting the global data

    global a  
    global b   
    global c   
    global d  
    global e  
    global f  
    global g

    global name
    global number 
    global date1
    global date2
    global interval 
    global temp1 
    global temp2

    global data
    global lst 
    global df 
    global df2
    global df3

# getting the respective inputs for the variables
    name = request.POST['name']  
    number = request.POST['number']  
    date1 = request.POST['date1']   
    date2 = request.POST['date2']
    interval = request.POST['interval']   
    temp1 = request.POST['temp1']   
    temp2 = request.POST['temp2']  
 
 # perform typecasting for the respective input to perform calculations.
    if name.isalpha() and number.isdigit():
        a = str(name) 
        b = int(number)  
        c =  datetime.strptime(date1,"%d/%m/%Y %H:%M") 
        d =  datetime.strptime(date2,"%d/%m/%Y %H:%M")
        interval = int(interval) 
        e = float(temp1)
        f = float(temp2)
        g = interval

        data = pd.date_range(start=date1, end=date2, freq=str(interval)+'min')
        df = pd.DataFrame(
            {
                "Date": data,
            }
        )
        
        df.index = np.arange(1, len(df) + 1)

        lst = []
        for i in range(len(df)):
            ran = random.uniform(float(temp1), float(temp2))
            ran2 = round(ran, 2)
            lst.append(ran2)

        df = df.assign(Temperature = lst)

        df2 = pd.DataFrame()
        df2['Date'] = [d.date() for d in df['Date']]
        df2['Time'] = [d.time() for d in df['Date']]
        df2 = df2.assign(Temperature = lst)
    
        df2.index = np.arange(1, len(df2) + 1)
        df2['Interval'] = interval
        df3 = df2.to_html()

        df2.to_csv('users\csv\df_print.csv', index=False)

        df4 = pd.read_csv('users\csv\df_print.csv')

        json_records = df4.reset_index().to_json(orient ='records')

        data2 = []
        data2 = json.loads(json_records)

        return render(request, "users/result.html", {"result": a,
                                                    "result2": b,
                                                    "result3": c,
                                                    "result4": d,
                                                    "result_interval": interval,
                                                    "result5": e,
                                                    "result6": f,
                                                    "d2" : data2,})


    else:
        res = "Type Correct Value"
        return render(request, "users/result.html", {"result": res})



def ProcessData(request):  


    return HttpResponse(df3)
    
   # df2 = pd.DataFrame()
   # df2['Date'] = [d.date() for d in df['Date']]
   # df2['Time'] = [d.time() for d in df['Time']]
   # df2 = df.assign(Temperature = lst)

    # df2.to_csv('df_print.csv', index = False)

    





    

    





class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
