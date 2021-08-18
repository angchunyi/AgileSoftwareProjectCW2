from django.urls import path
from . import views
from .views import ( PostListView,
                     PostDetailView,
                     PostCreateView,
                     PostUpdateView,
                     PostDeleteView,
                     UserPostListView,
                     AddCommentView,
                     AddLike,)

urlpatterns = [
    path('', PostListView.as_view(), name='TravelExperienceApp-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='TravelExperienceApp-about'),
    path('post/<int:pk>/comment/', AddCommentView.as_view(), name='add-comment'),
    path('contact/', views.contact, name='contact'),
    path('post/<int:pk>/like/', AddLike.as_view(), name='like'),
    path('search/', views.search, name='search'),

]


