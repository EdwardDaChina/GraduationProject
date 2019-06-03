from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # 使用内置验证视图
from django.conf import settings
from django.conf.urls.static import static

app_name = 'rs'

urlpatterns = [
    # post views
    # path('', views.post_list, name='post_list'),  将基于函数的视图改为基于类的视图
    path('post_list/', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
   # path('edit/', views.edit, name='edit'),
    path('product_list/', views.product_list, name='product_list'),
    path('<slug:genre_slug>/', views.product_list, name='product_list_by_genre'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

