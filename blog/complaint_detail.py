from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponseRedirect
import blog.tool as tool
import blog.models as models
import json
from django.db.models import Q


def complaint_detail(request):
    head = tool.getOnlineUser(request)

    post_id = request.GET.get('post_id')
    complaint = models.complaint.objects.get(id=post_id)
    user = complaint.user_id
    pics = tool.strToArr(complaint.pic)
    for i in range(0, len(pics)):
        pics[i] = tool.getOnePicPath(pics[i])
    isCollected = True
    try:
        if 'user_id' in head.keys():
            models.collection_complaint.objects.get(
                user_id=models.user.objects.get(id=head['user_id']),
                collected_complaint_id=models.complaint.objects.get(id=post_id))
        else:
            isCollected = False
    except models.collection_complaint.DoesNotExist:
        isCollected = False
    return render(request, 'complaint.html', {
        'user_id': user.id,
        'user_name': user.username,
        'user_head': tool.getHeadPath(user.user_head),
        'title': complaint.title,
        'content': complaint.content,
        'time': tool.dbTimeFormat(complaint.create_time),
        'pics': pics,
        'head': head,
        'post_id': post_id,
        'amount': complaint.reply_amount,
        'like': models.collection_complaint.objects.filter(collected_complaint_id=post_id).count(),
        'isCollected': isCollected
    })


def complaint_top(request):
    post_id = request.GET.get('post_id')
    comment_company_list = models.comment.objects.filter(complaint_id=post_id,
                                                         user_id__type=tool.COMPANY_USER)
    comment_jury_list = models.comment.objects.filter(complaint_id=post_id,
                                                      user_id__type=tool.JURY_USER)
    l = []
    num = 1
    for e in comment_company_list:
        user = e.user_id
        l.append({
            'user_id': user.id,
            'user_name': user.username,
            'user_head': tool.getHeadPath(user.user_head),
            'content': e.content,
            'time': tool.dbTimeFormat(e.create_time),
            'num': num,
            'type_name': '企业'
        })
        num += 1

    for e in comment_jury_list:
        user = e.user_id
        l.append({
            'user_id': user.id,
            'user_name': user.username,
            'user_head': tool.getHeadPath(user.user_head),
            'content': e.content,
            'time': tool.dbTimeFormat(e.create_time),
            'num': num,
            'type_name': '评审团'
        })
        num += 1
    return JsonResponse({'list': l})


def complaint_reply(request):
    post_id = request.GET.get('post_id')
    comment_list = models.comment.objects.filter(complaint_id=post_id,
                                                 user_id__type=tool.GENERAL_USER)
    l = []
    num = 1
    for e in comment_list:
        user = e.user_id
        l.append({
            'user_id': user.id,
            'user_name': user.username,
            'user_head': tool.getHeadPath(user.user_head),
            'content': e.content,
            'time': tool.dbTimeFormat(e.create_time),
            'num': num
        })
        num += 1
    return JsonResponse({'list': l})


def complaint_comment(request):
    head = tool.getOnlineUser(request)
    post_id = request.GET.get('post_id')
    content = request.GET.get('send_content')
    user = models.user.objects.get(id=head['user_id'])
    comment = models.comment(content=content,
                             user_id=user,
                             complaint_id=models.complaint.objects.get(id=post_id))
    comment.save()

    complaint = models.complaint.objects.get(id=post_id)
    complaint.reply_amount += 1
    if complaint.status == 0:
        if user.type == tool.JURY_USER:
            complaint.status = 2
        elif user.type == tool.COMPANY_USER:
            complaint.status = 3
        else:
            complaint.status = 1
    complaint.save()
    return HttpResponseRedirect('post_detail?post_id=' + post_id)


def complaint_collect(request):
    head = tool.getOnlineUser(request)
    post_id = request.GET.get('post_id')
    rows = models.collection_complaint.objects.filter(
        user_id=head['user_id'],
        collected_complaint_id=post_id)
    if len(rows) > 0:
        return JsonResponse({'result': False})
    else:
        collection = models.collection_complaint(
            user_id=models.user.objects.get(id=head['user_id']),
            collected_complaint_id=models.complaint.objects.get(id=post_id))
        collection.save()
    return JsonResponse({'result': True})


def complaint_cancel_collect(request):
    head = tool.getOnlineUser(request)
    post_id = request.GET.get('post_id')
    rows = models.collection_complaint.objects.filter(
        user_id=head['user_id'],
        collected_complaint_id=post_id)
    if len(rows) > 0:
        rows.delete()
        return JsonResponse({'result': True})
    else:
        return JsonResponse({'result': False})
