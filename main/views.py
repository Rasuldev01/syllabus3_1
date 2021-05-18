from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from .models import Post, Category
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import Http404
from django.db import transaction

class MainIndex(View):
    def get(self, request, pk=None):
        query = Post.objects.order_by('-id')
        if id is None:
            query = query.filter(category_id=pk)
        paginator = Paginator(query, 2)
        page = paginator.get_page(request.GET.get('page'))

        return render(request, 'main/index.html', {
            'object_list': page.object_list,
            'page_obj': page

        })


class UploadPost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['category', 'comment', 'file']
    template_name = 'layouts/form.html'
    success_url = reverse_lazy('main:upload')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        request.title = _("Yuklash")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, _("Muvaffaqiyatli qo'shildi."))

        return super().form_valid(form)

class CategoryView(View):
    def get(self, request):
        return render(request, 'main/index.html', {
            'category': Category.objects.all()
        })

class PostLike(View):
    def get(self, request, post_id, action):
        if action not in ['like', 'dislike']:
            raise Http404

        def _redirect():
            return redirect(request.GET.get('return', 'main:index'))
        with transaction.atomic():
            try:
                post = Post.objects.select_for_update().get(id=post_id)
            except:
                return _redirect()

            if action == 'like':
                post.like += 1
            else:
                post.dislike += 1
            post.save()

            return _redirect()