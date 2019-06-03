from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # 增加分页功能
from django.views.generic import ListView  # Python中类可以取代函数,基于函数的视图（FBV）也可以通过基于类的视图（CBV）来实现。
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from .models import Genre, Product


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, 'rs/product/detail.html', {'product': product})


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
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'rs/edit.html', {'user_form': user_form, 'profile_form': profile_form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")

    else:
        form = LoginForm()

    return render(request, 'rs/login.html', {'form': form})


@login_required
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


def post_list(request):
    object_list = Post.published.all()
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
    return render(request, 'rs/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status="published", publish__year=year, publish__month=month,
                             publish__day=day)
    return render(request, 'rs/post/detail.html', {'post': post})

