from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Post
from taggit.models import Tag
from .forms import PostForm, EditForm, CommentForm


def HomeView(request):
    return render(request, 'home.html')


class PostList(generic.ListView):
    model = Post
    template_name = 'index.html'


class DetailPostView(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'
    fields = ['title', 'tags', 'content']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data


def PostLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


def TagView(request, tag_slug):
    tag_list = Post.objects.all()
    tag = get_object_or_404(Tag, slug=tag_slug)
    tag_list = tag_list.filter(tags__in=[tag])
    paginator = Paginator(tag_list, 20)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results

        posts = paginator.page(paginator.num_pages)

    return render(request, 'tags.html', locals())


class AddPostView(generic.CreateView):
    model = Post
    template_name = 'add_post.html'
    # fields = ['title', 'author', 'content']
    form_class = PostForm


class UpdatePostView(generic.UpdateView):
    model = Post
    template_name = 'update_post.html'
    # fields = ['title', 'content']
    form_class = EditForm


class DeletePostView(generic.DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('post_list')


def AddComment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})
