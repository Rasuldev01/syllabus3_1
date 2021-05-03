from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from .forms import RegistrationForm
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
            user = form.user(commit=False)
            user.set_password(user.password)
            user.save()


            messages.success(request, _("Siz muvaffaqiyatli ro'yhatdan o'tingiz !!!"))
            return redirect("main:index")

        return render(request, 'layouts/form.html', {
            'form': form
        })