from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, ResponseForm
from .models import Question, UserResponse
from django.http import HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator


@login_required
def home(request):
    questions = Question.objects.filter(is_active=True)
    response_form = ResponseForm()

    # paginator = Paginator(questions, 5)
    # page = request.GET.get('page', 1)
    # questions = paginator.get_page(page)

    if request.method == 'POST':
        response_form = ResponseForm(request.POST)
        if response_form.is_valid():
            response_obj = response_form.save(commit=False)
            response_obj.user = request.user
            response_obj.save()
            messages.success(request, 'Response submitted successfully')
            return redirect(reverse('response-summary'))

    return render(request, 'users/home.html', {'questions': questions, 'response_form': response_form, 'user': request.user})

@login_required
def respond_to_question(request):
    if request.method == 'POST':
        for question in Question.objects.filter(is_active=True):
            response_value = request.POST.get(f'response_{question.id}')
            user_response, created = UserResponse.objects.get_or_create(user=request.user, question=question)
            user_response.answer = response_value
            user_response.save()

        # Redirect to the response summary page after successful submission
        return redirect(reverse('response-summary'))

    return HttpResponse("Invalid request method")

@login_required
def response_summary(request):
    user_responses = UserResponse.objects.filter(user=request.user)
    yes_count = user_responses.filter(answer=True).count()
    no_count = user_responses.filter(answer=False).count()

    return render(request, 'users/response_summary.html', {'user_responses': user_responses, 'yes_count': yes_count, 'no_count': no_count})


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
    pass
    # if request.method == 'POST':
    #     user_form = UpdateUserForm(request.POST, instance=request.user)
    #     profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
    #     sensor_form = SensorForm(request.POST)
    #     if user_form.is_valid() and profile_form.is_valid():
    #         user_form.save()
    #         profile_form.save()
    #         messages.success(request, 'Your profile is updated successfully')
    #         return redirect(to='users-profile')
    # else:
    #     user_form = UpdateUserForm(instance=request.user)
    #     profile_form = UpdateProfileForm(instance=request.user.profile)

    # return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})




