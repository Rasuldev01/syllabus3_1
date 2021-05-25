
import time
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView
from .models import Post, Category, PostComment
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.db import transaction
from main.forms import PostCommentForm

class MainIndex(View):
    def get(self, request, pk=None):
        cat = None
        query = Post.objects.order_by('-id')
        if pk is not None:
            cat = Category.objects.get(id=pk)
            query = query.filter(category_id=pk)


        paginator = Paginator(query, 2)
        page = paginator.get_page(request.GET.get('page'))

        return render(request, 'main/index.html', {
            'cat': cat,
            'object_list': page.object_list,
            'page_obj': page

        })

class MainCatAjax(View):
    def get(self, request, pk):
        time.sleep(1)
        query = Post.objects.order_by('-id')
        if pk is not None:
            cat = Category.objects.get(id=pk)
            query = query.filter(category_id=pk)

        paginator = Paginator(query, 1)
        page = paginator.get_page(request.GET.get('page'))

        return render(request, 'main/cat-ajax.html', {
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

class PostCommentView(ListView):
    model = PostComment
    paginate_by = 10
    ordering = '-id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(post_id=self.kwargs['post_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['post'] = Post.objects.get(id=self.kwargs['post_id'])
        context['form'] = PostCommentForm
        return context

    def post(self, request, post_id):
        if not request.user.is_authenticated:
            return redirect('main:comment', post_id=self.kwargs['post_id'])

        form = PostCommentForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            comment:PostComment = form.save(commit=False)
            comment.post_id = post_id
            comment.user = self.request.user
            comment.save()

            return redirect('main:comment', post_id=post_id)

        return self.get(request, post_id=post_id)