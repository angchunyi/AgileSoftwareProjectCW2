from django.shortcuts import render, get_object_or_404,redirect, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import View,ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CommentForm
from .models import Comment
from django.urls import reverse, reverse_lazy
from .models import Contact
from django.http import HttpResponseRedirect
# Create your views here.

posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]

# home page
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'TravelExperienceApp/home.html', context)

# about page
def about(request):
    return render(request, 'TravelExperienceApp/about.html', {'title':'about'})



class PostListView(ListView):
    model = Post
    template_name = 'TravelExperienceApp/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

class UserPostListView(ListView):
    model = Post
    template_name = 'TravelExperienceApp/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post




class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['file','title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class AddCommentView(LoginRequiredMixin,CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'TravelExperienceApp/add_comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('TravelExperienceApp-home')

def contact(request):
    if request.method=="POST":
        contact=Contact()
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        contact.name=name
        contact.email=email
        contact.message=message
        contact.save()
        return HttpResponse("<h1> Thank You for contacting us!</h1>")
    return render(request, 'TravelExperienceApp/contact.html',{'title':'Contact'})


class AddLike(LoginRequiredMixin, View):
    def post (self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)


        is_like = False
        for like in post.likes.all():
            if like ==request.user:
                is_like=True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts=Post.objects.filter(title__contains=searched) | Post.objects.filter(content__contains=searched)
        return render(request, 'TravelExperienceApp/search.html',{'searched':searched,'posts':posts })
    else:
        return render(request, 'TravelExperienceApp/search.html',{})

