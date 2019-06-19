from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # 使用内置验证视图
from django.conf import settings
from django.conf.urls.static import static

app_name = 'rs'

urlpatterns = [
    # post views
    # path('', views.post_list, name='post_list'),  将基于函数的视图改为基于类的视图
    # path('post_list/', views.PostListView.as_view(), name='post_list'),
    path('post_list/', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),  # 增加一行通过标签显示文章的URL
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('rs:password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('rs:password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('rs:password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('edit/', views.edit, name='edit'),
    path('product_list/', views.product_list, name='product_list'),
    path('<slug:genre_slug>/', views.product_list, name='product_list_by_genre'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

