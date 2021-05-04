from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from .forms import RegistrationForm, LoginForm
from django.views import View


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

        request.title = ("Tizimga kirish")

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
                messages.success(request, _("Xushkelibsiz, {}!".format(user.username)))

                return redirect('main:index')

            form.add_error('password', _("Login va/yoki parol noyo'ri."))

        return render(request, 'layouts/form.html', {
            'form': form
        })
@login_required
def client_logout(request):
    messages.success(request, "Xayr {}!".format(request.user.username))
    logout(request)

    return redirect('main:index')

