from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Article, Summary
from accounts.models import Profile

# Create your views here.

def detail(request, article_id):
    article = get_object_or_404(Article, pk = article_id)
    summary_list = Summary.objects.filter(belongsto_article=article_id)
    context = {
        'article':article,
        'summary_list':summary_list,
    }

    return render(request,"article/article_detail.html", context)

def summary(request, article_id):

    if request.method == "POST":
        summary = Summary()
        summary.belongsto_article = Article.objects.get(id=article_id)
        user = request.user
        profile = Profile.objects.get(user=user)
        summary.belongsto_user = profile
        summary.content = request.POST['content']
        summary.save()
        return redirect('article:detail', article_id)
    else:
        return render(request, 'article/summary.html')

def summary_obj(request, summary_id):
    
    summary = Summary.objects.get(id=summary_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    check_sbj_sum = profile.sbj_sum.filter(id=summary_id)

    if check_sbj_sum.exists():
        profile.sbj_sum.remove(summary)
        profile.obj_sum.add(summary)
        summary.sbj_count -= 1
        summary.obj_count += 1
        summary.save()

    else:
        profile.obj_sum.add(summary)
        summary.obj_count += 1
        summary.save()

    return redirect('article:detail', summary.belongsto_article.id)

def summary_sbj(request, summary_id):
    
    summary = Summary.objects.get(id=summary_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    check_obj_sum = profile.obj_sum.filter(id=summary_id)

    if check_obj_sum.exists():
        profile.obj_sum.remove(summary)
        profile.sbj_sum.add(summary)
        summary.obj_count -= 1
        summary.sbj_count += 1
        summary.save()
    else:
        profile.sbj_sum.add(summary)
        summary.sbj_count += 1
        summary.save()

    return redirect('article:detail', summary.belongsto_article.id)