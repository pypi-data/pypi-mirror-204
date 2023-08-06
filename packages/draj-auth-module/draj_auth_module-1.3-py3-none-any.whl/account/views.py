from django.views.generic.edit import CreateView, FormView
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        html = "<html><body>Home page</body></html>"
        return HttpResponse(html)


class RegistrationView(CreateView):
    template_name = 'account/signup.html'
    success_url = '/'
    form_class = RegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        super().form_valid(form)

        user, created = User.objects.get_or_create(
            username=self.object.username,
            first_name=self.object.first_name,
            last_name=self.object.last_name,
            email=self.object.email
        )
        print(created)
        user.set_password(self.request.POST.get('password'))
        user.is_active = True
        user.save()
        self.object.user = user
        self.object.save()

        messages.success(self.request,
                         "User register successfully. Please varify your email for login"
                         )
        return redirect('login')


class LoginView(FormView):
    template_name = "account/login.html"
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "User logged in successfully.")
        return redirect("home")


class LogoutView(FormView):
    def get(self, *args, **kwargs):
        logout(self.request)
        messages.success(self.request, "User logged out successfully.")
        return redirect('/')
