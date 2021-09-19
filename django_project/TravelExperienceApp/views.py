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

# home page
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'TravelExperienceApp/home.html', context)

# about page
def about(request):
    return render(request, 'TravelExperienceApp/about.html', {'title':'about'})

# post list view - home page
class PostListView(ListView):
    model = Post
    template_name = 'TravelExperienceApp/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

# user post list
class UserPostListView(ListView):
    model = Post
    template_name = 'TravelExperienceApp/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# a post detail view
class PostDetailView(DetailView):
    model = Post



# create a post page
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['file','title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# update post
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

# delete post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# add comment, login required
class AddCommentView(LoginRequiredMixin,CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'TravelExperienceApp/add_comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('TravelExperienceApp-home')


#  contact us page
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


# add like to the post, login is required
class AddLike(LoginRequiredMixin, View):
    def post (self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        is_like = False
        for like in post.likes.all():
            if like ==request.user:
                is_like=True
                break

        # if the user clicked on the like button, then one like will added
        if not is_like:
            post.likes.add(request.user)

        # if the user clicked twice on the like button, then the one like will be removed
        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


# search for post
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts=Post.objects.filter(title__contains=searched) | Post.objects.filter(content__contains=searched)
        return render(request, 'TravelExperienceApp/search.html',{'searched':searched,'posts':posts })
    else:
        return render(request, 'TravelExperienceApp/search.html',{})



