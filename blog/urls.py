from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('index/', views.PostList.as_view(), name='post_list'),
    path('post/<int:pk>', views.DetailPostView.as_view(), name='post_detail'),
    path('category/<slug:tag_slug>/', views.TagView, name='tags'),
    path('post-like/<int:pk>', views.PostLike, name="post_like"),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('post/edit/<int:pk>', views.UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/remove', views.DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/comment/', views.AddComment, name='add_comment'),
]
