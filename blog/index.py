from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponseRedirect
import blog.tool as tool
import blog.models as models
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger


def index(request):
    pic1 = tool.getOnePicPath(tool.getStaticData('pic1'))
    pic2 = tool.getOnePicPath(tool.getStaticData('pic2'))
    pic3 = tool.getOnePicPath(tool.getStaticData('pic3'))
    pic1_title = tool.getStaticData('pic1_title')
    pic2_title = tool.getStaticData('pic2_title')
    pic3_title = tool.getStaticData('pic3_title')
    pic_ad = tool.getOnePicPath(tool.getStaticData('pic_ad'))

    return render(request, 'index.html', {
        'head': tool.getOnlineUser(request),
        'title': '主页',
        'isIndex': True,
        'pic_ad': pic_ad,
        'pic1': pic1,
        'pic2': pic2,
        'pic3': pic3,
        'pic1_title': pic1_title,
        'pic2_title': pic2_title,
        'pic3_title': pic3_title
    })


def write_page(request):
    return render(request, 'blog_write.html')


def carousel_map(request):
    data = {
        'list': [
            {
                'title': '',
                'pic': ''
            },
            {
                'title': '',
                'pic': ''
            }
        ]}

    return JsonResponse(data)


def latest_posts(request):
    page = int(request.GET.get('page'))
    posts = models.complaint.objects.filter(user_id__type=0).order_by('-update_time')
    paginator = Paginator(posts, 6)
    data = {'list': []}
    try:
        p = paginator.page(page)
        data['list'] = tool.getComplaintData(p.object_list)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        print('没有此页', page)
    return JsonResponse(data)


def hot_posts(request):
    page = request.GET.get('page')
    data = {
        'list': [
            {
                'title': '',
                'content': '',
                'user_name': '',
                'pic': ''
            },
            {
                'title': '',
                'content': '',
                'user_name': '',
                'pic': ''
            }
        ]}

    return JsonResponse(data)


def hot_articles(request):
    hot_articles = models.hot_news.objects.filter()
    data = {'list': []}
    for e in hot_articles:
        item = {
            'title': e.news_id.title,
            'content': e.news_id.content
        }
        data['list'].append(item)
    return JsonResponse(data)


def post_complain(request):
    user_data = tool.getOnlineUser(request)
    post_brand = request.POST.get('post_brand')
    post_product = request.POST.get('post_product')
    post_title = request.POST.get('post_title')
    post_content = request.POST.get('post_content')

    post_img = request.FILES.getlist("post_img")
    names = tool.savePics(post_img)
    try:
        company = models.company.objects.get(company_name=post_brand)
    except models.company.DoesNotExist:
        company = models.company(company_name=post_brand, company_head='', company_introduce='')
        company.save()

    complain = models.complaint(brand_id=company, product=post_product, title=post_title,
                                content=post_content,
                                user_id=models.user.objects.get(id=user_data['user_id']),
                                category_id=models.category.objects.get(id=1),
                                pic=names if names else '',
                                reply_amount=0,
                                status=0)
    complain.save()
    return HttpResponseRedirect('index')
