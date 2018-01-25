from django.shortcuts import render
from django.template.context_processors import csrf
from bbs import models
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from bbs import comment_handler, form
import json

category_list = models.Category.objects.filter(set_as_top_menu=True).order_by('position_index')


# Create your views here.
def index(request):
    articles_list = models.Articles.objects.filter(status='published')
    # category_obj = models.Category.objects.get(position_index=1)
    return render(request, 'bbs/index.html', {'category_list': category_list, 'articles_list': articles_list})


def rootUrl(request):
    return HttpResponseRedirect('/bbs')


def category(request, id):
    category_obj = models.Category.objects.get(id=id)
    if category_obj.position_index == 1:  # 全部
        articles_list = models.Articles.objects.filter(status='published')
    else:
        articles_list = models.Articles.objects.filter(category__id=id, status='published')
    return render(request, 'bbs/category.html',
                  {'category_list': category_list, 'category_obj': category_obj, 'articles_list': articles_list})


def acc_login(request):
    if request.method == "POST":
        print(request.POST)
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next') or '/bbs')
        else:
            login_err = "Wrong username or password!"
            return render(request, 'login.html', {'login_err': login_err, 'category_list': category_list})
    return render(request, 'login.html', {'category_list': category_list}, csrf(request))


def acc_logout(request):
    logout(request)
    next_url = request.GET.get('next')
    if next_url == '/bbs/new_article/':
        next_url = '/bbs/'
    return HttpResponseRedirect(next_url or '/bbs/')


def article_detail(request, article_id):
    article_obj = models.Articles.objects.get(id=article_id)
    comment_tree = comment_handler.build_tree(article_obj.comment_set.select_related())
    return render(request, 'bbs/article_detail.html', {'article_obj': article_obj, 'category_list': category_list})


def comment(request):
    print(request.POST)
    if request.method == 'POST':
        new_comment_obj = models.Comment(
            articles_id=request.POST.get('article_id'),
            parent_comment_id=request.POST.get('parent_comment_id') or None,
            comment_type=request.POST.get('comment_type'),
            user_id=request.user.userprofile.id,
            comment=request.POST.get('comment')
        )
        new_comment_obj.save()
    return HttpResponse('post-comment-success')


def get_comments(request, article_id):
    article_obj = models.Articles.objects.get(id=article_id)
    comment_tree = comment_handler.build_tree(article_obj.comment_set.select_related().filter(comment_type=1))
    tree_html = comment_handler.render_comment_tree(comment_tree)
    return HttpResponse(tree_html)


@login_required
def new_article(request):
    if request.method == 'GET':
        article_form = form.ArticleModelForm()
        return render(request, 'bbs/new_article.html', {'article_form': article_form, 'category_list':category_list}, csrf(request))
    elif request.method == 'POST':
        article_form = form.ArticleModelForm(request.POST, request.FILES)
        if article_form.is_valid():
            data = article_form.cleaned_data
            data['author_id'] = request.user.userprofile.id
            article_obj = models.Articles(**data)
            article_obj.save()
            return HttpResponse("发布成功")
        else:
            return render(request, 'bbs/new_article.html', {'article_form': article_form, 'category_list':category_list}, csrf(request))


def file_upload(request):
    print(request.FILES)
    file_obj = request.FILES.get('filename')
    with open('uploads/%s' % file_obj.name, 'wb+') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)
    return render(request, 'bbs/new_article.html', csrf(request))


def get_latest_article_count(request):
    latest_article_id = request.GET.get("latest_id")
    if latest_article_id:
        new_article_count = models.Articles.objects.filter(id__gt = latest_article_id).count()
        print("new_article_count:", new_article_count)
    else:
        new_article_count = 0
    return HttpResponse(json.dumps({'new_article_count': new_article_count}))
