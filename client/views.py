from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView
from .models import User
from .forms import RegistrationForm, LoginForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class ClientRegistration(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        request.title = _('Ro\'yhatdan o\'tish')

    def get(self, request):
        return render(request, 'layouts/form.html', {
            'form': RegistrationForm()
        })

    def post(self, request):
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()

            messages.success(request, _("Siz muvaffaqiyatli ro'yhatdan o'tingiz !!!"))
            return redirect("main:index")

        return render(request, 'layouts/form.html', {
            'form': form
        })


class ClientLogin(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        request.title = _("Tizimga kirish")

    def get(self, request):
        return render(request, 'layouts/form.html', {
            'form': LoginForm()
        })

    def post(self, request):
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if not user is None:
                login(request, user)
                messages.success(request, _("Xush kelibsiz, {}!").format(user.username))

                return redirect('main:index')

            form.add_error('password', _("Login va/yoki parol noyo'ri."))

        return render(request, 'layouts/form.html', {
            'form': form
        })


@login_required
def client_logout(request):
    messages.success(request, _("Xayr {}!").format(request.user.username))
    logout(request)

    return redirect('main:index')


class ClientProfile(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'email', 'photo']
    template_name = 'layouts/form.html'
    success_url = reverse_lazy('client:profile')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        request.title = _("Profil")
        request.button_title = _("Saqlash")

    def get_object(self, queryset=None):
        return self.request.user
