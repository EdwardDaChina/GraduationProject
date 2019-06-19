from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # 增加分页功能
from django.views.generic import ListView  # Python中类可以取代函数,基于函数的视图（FBV）也可以通过基于类的视图（CBV）来实现。
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, CommentForm
from .models import Profile, Genre, Product, Post, Comment
from django.contrib import messages
from taggit.models import Tag


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    comments = product.comments.filter(active=True)

    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # 通过表单直接创建新数据对象，但是不要保存到数据库中
            new_comment = comment_form.save(commit=False)
            # 设置外键为当前文章
            new_comment.product = product
            # 将评论数据对象写入数据库
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'rs/product/detail.html', {'product': product, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})


@login_required
def product_list(request, genre_slug=None):
    genre = None
    genres = Genre.objects.all()  # 编译器问题，不影响代码执行
    products = Product.objects.all()
    if genre_slug:
        genre = get_object_or_404(genres, slug=genre_slug)
        products = products.filter(genre=genre)

    return render(request, 'rs/product/list.html',
                  {'genre': genre, 'genres': genres, 'products': products})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'rs/edit.html', {'user_form': user_form, 'profile_form': profile_form})


def user_login(request):
    if request.method == "POST":  # 当视图接受一个GET请求，通过form = LoginForm()实例化一个空白表单
        form = LoginForm(request.POST)  # 使用提交的数据实例化一个表单对象
        if form.is_valid():  # 验证表单数据。如果未通过，则将当前表单对象展示在页面中
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])  # 接受三个参数到数据库中进行匹配，匹配成功会返回一个User数据对象
            if user is not None:
                if user.is_active:
                    login(request, user)  # login()用于在当前会话中设置登录状态
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")

    else:
        form = LoginForm()

    return render(request, 'rs/login.html', {'form': form})


@login_required  # 装饰器，表示被装饰的视图只有在用户登录的情况下才会被执行
def dashboard(request):
    return render(request, 'rs/dashboard.html', {'section': 'dashboard'})


def register(request):  # 注册
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # 建立新数据对象但是不写入数据库
            new_user = user_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_form.cleaned_data['password'])
            # 保存User对象
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'rs/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'rs/register.html', {'user_form': user_form})


class PostListView(ListView):  # 使用内置的基于类的视图（提供了基类View）
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3  # 每页显示三篇文章
    template_name = 'rs/post/list.html'


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)  # 每页显示3篇文章（分页功能）
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page参数不是一个整数就返回第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出总页数就返回最后一页
        posts = paginator.page(paginator.num_pages)
    return render(request, 'rs/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status="published", publish__year=year, publish__month=month, publish__day=day)
    # 列出文章对应的所有活动的评论
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # 通过表单直接创建新数据对象，但是不要保存到数据库中
            new_comment = comment_form.save(commit=False)
            # 设置外键为当前文章
            new_comment.post = post
            # 将评论数据对象写入数据库
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'rs/post/detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})
  # save()方法仅对ModelForm生效，因为Form类没有关联到任何数据模型。






