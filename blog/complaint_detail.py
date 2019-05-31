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
    for i in range(len(pics)):
        pics[i] = '../static/pic/' + pics[i]

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


def complaint_jury(request):
    # post_id = int(request.GET.get('post_id'))
    post_id = 1
    article_list = models.complaint.objects.get(id=post_id)
    article_id = int(article_list.id)
    comment_list = models.comment.objects.filter(complaint_id_id=article_id)
    jury_flag = False
    dataset = {}
    for com in comment_list:
        user_id = int(com.user_id_id)
        user_list = models.user.objects.filter(Q(id=user_id) & Q(is_jury=1))
        print(len(user_list))
        if len(user_list) > 0:
            user_list = models.user.objects.get(id=user_id)
            jury_list = models.jury.objects.get(user_id_id=user_id)
            data = {
                'user_id': com.user_id_id,
                'user_name': user_list.username,
                'user_head': tool.getHeadPath(user_list.user_head),
                'real_name': jury_list.real_name,
                'introduce': jury_list.jury_introduce,
                'content': com.content,
                'time': com.create_time,
            }
            dataset[com.user_id_id] = data
            jury_flag = True
    if jury_flag:
        return dataset
    else:
        return


def complaint_reply(request):
    global item
    post_id = request.GET.get('post_id')
    comment_list = models.comment.objects.filter(complaint_id=post_id)
    # pic = request.FILES.get("pic", None)
    # flag = True
    # while(flag):
    #     res = tool.savePic(pic)
    #     if res:
    #         flag = False
    data = {'list': []}

    for e in comment_list:
        user = e.user_id
        if not user.is_jury:
            data['list'].append({
                'user_id': user.id,
                'user_name': user.username,
                'user_head': tool.getHeadPath(user.user_head),
                'content': e.content,
                'time': tool.dbTimeFormat(e.create_time),
            })
    return JsonResponse(data)


def complaint_comment(request):
    head = tool.getOnlineUser(request)
    post_id = request.GET.get('post_id')
    content = request.GET.get('send_content')
    comment = models.comment(content=content,
                             user_id=models.user.objects.get(id=head['user_id']),
                             complaint_id=models.complaint.objects.get(id=post_id))
    comment.save()

    complaint = models.complaint.objects.get(id=post_id)
    complaint.reply_amount += 1
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
