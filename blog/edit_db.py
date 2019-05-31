from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponseRedirect
import blog.tool as tool
import blog.models as models


def edit_page(request):
    return render(request, "edit_page.html")


def edit_pic(request):
    pic1 = request.FILES.get("pic1", None)
    pic1_value = tool.savePic(pic1)
    pic2 = request.FILES.get("pic2", None)
    pic2_value = tool.savePic(pic2)
    pic3 = request.FILES.get("pic3", None)
    pic3_value = tool.savePic(pic3)
    pic_ad = request.FILES.get("pic_ad", None)
    pic_ad_value = tool.savePic(pic_ad)
    pic1_title = request.POST.get('pic1_title')
    pic2_title = request.POST.get('pic2_title')
    pic3_title = request.POST.get('pic3_title')

    tool.saveStaticData("pic1", pic1_value)
    tool.saveStaticData("pic2", pic2_value)
    tool.saveStaticData("pic3", pic3_value)
    tool.saveStaticData("pic_ad", pic_ad_value)
    tool.saveStaticData("pic1_title", pic1_title)
    tool.saveStaticData("pic2_title", pic2_title)
    tool.saveStaticData("pic3_title", pic3_title)

    return HttpResponseRedirect('edit_page')


def edit_red_black(request):
    reds = [''] * 10
    reds[0] = request.POST.get('red1')
    reds[1] = request.POST.get('red2')
    reds[2] = request.POST.get('red3')
    reds[3] = request.POST.get('red4')
    reds[4] = request.POST.get('red5')
    reds[5] = request.POST.get('red6')
    reds[6] = request.POST.get('red7')
    reds[7] = request.POST.get('red8')
    reds[8] = request.POST.get('red9')
    reds[9] = request.POST.get('red10')
    red_heads = [''] * 10
    red_heads[0] = tool.savePic(request.FILES.get("red1_head", None))
    red_heads[1] = tool.savePic(request.FILES.get("red2_head", None))
    red_heads[2] = tool.savePic(request.FILES.get("red3_head", None))
    red_heads[3] = tool.savePic(request.FILES.get("red4_head", None))
    red_heads[4] = tool.savePic(request.FILES.get("red5_head", None))
    red_heads[5] = tool.savePic(request.FILES.get("red6_head", None))
    red_heads[6] = tool.savePic(request.FILES.get("red7_head", None))
    red_heads[7] = tool.savePic(request.FILES.get("red8_head", None))
    red_heads[8] = tool.savePic(request.FILES.get("red9_head", None))
    red_heads[9] = tool.savePic(request.FILES.get("red10_head", None))
    blacks = [''] * 10
    blacks[0] = request.POST.get('black1')
    blacks[1] = request.POST.get('black2')
    blacks[2] = request.POST.get('black3')
    blacks[3] = request.POST.get('black4')
    blacks[4] = request.POST.get('black5')
    blacks[5] = request.POST.get('black6')
    blacks[6] = request.POST.get('black7')
    blacks[7] = request.POST.get('black8')
    blacks[8] = request.POST.get('black9')
    blacks[9] = request.POST.get('black10')
    black_heads = [''] * 10
    black_heads[0] = tool.savePic(request.FILES.get("black1_head", None))
    black_heads[1] = tool.savePic(request.FILES.get("black2_head", None))
    black_heads[2] = tool.savePic(request.FILES.get("black3_head", None))
    black_heads[3] = tool.savePic(request.FILES.get("black4_head", None))
    black_heads[4] = tool.savePic(request.FILES.get("black5_head", None))
    black_heads[5] = tool.savePic(request.FILES.get("black6_head", None))
    black_heads[6] = tool.savePic(request.FILES.get("black7_head", None))
    black_heads[7] = tool.savePic(request.FILES.get("black8_head", None))
    black_heads[8] = tool.savePic(request.FILES.get("black9_head", None))
    black_heads[9] = tool.savePic(request.FILES.get("black10_head", None))

    for i in range(10):
        if reds[i] == '':
            continue
        try:
            company = models.company.objects.get(company_name=reds[i])
        except models.company.DoesNotExist:
            company = models.company(company_name=reds[i], company_head=red_heads[i])
            company.save()
        if red_heads[i] != '' and red_heads[i] is not False:
            company.company_head = red_heads[i]
            company.save()
        try:
            s = models.red_black.objects.get(score=10 - i, is_red=True)
        except models.red_black.DoesNotExist:
            print('没有分数', str(10 - i), '的排名')
        else:
            s.score = 0
            s.save()
        try:
            s = models.red_black.objects.get(company_id=company)
        except models.red_black.DoesNotExist:
            s = models.red_black(company_id=company, score=10 - i, complaint_amount=0, is_red=True)
            s.save()
        else:
            s.score = 10 - i
            s.save()

    for i in range(10):
        if blacks[i] == '':
            continue
        try:
            company = models.company.objects.get(company_name=blacks[i])
        except models.company.DoesNotExist:
            company = models.company(company_name=blacks[i], company_head=black_heads[i])
            company.save()
        if black_heads[i] != '' and black_heads[i] is not False:
            company.company_head = black_heads[i]
            company.save()
        try:
            s = models.red_black.objects.get(score=10 - i, is_red=False)
        except models.red_black.DoesNotExist:
            print('没有分数', str(10 - i), '的排名')
        else:
            s.score = 0
            s.save()
        try:
            s = models.red_black.objects.get(company_id=company)
        except models.red_black.DoesNotExist:
            s = models.red_black(company_id=company, score=10 - i, complaint_amount=0, is_red=False)
            s.save()
        else:
            s.score = 10 - i
            s.save()
    return HttpResponseRedirect('edit_page')
