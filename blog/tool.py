import os
import os.path
import time
import ast
from blog import models


def dbTimeFormat(time):
    return time.strftime('%Y年%m月%d日 %H:%M')


def getPicPath(pics):
    if pics and len(pics) > 0:
        return '../static/pic/' + strToArr(pics)[0]
    else:
        return ''


def getOnePicPath(pic):
    return '../static/pic/' + pic


def getHeadPath(pic):
    return ('../static/pic/' + pic) if pic else '../static/img/default_head.png'


def file_extension(path):
    return os.path.splitext(path)[1]


def savePic(pic):
    if not pic:
        return False
    name = str(int(round(time.time() * 1000))) + file_extension(pic.name)  # 毫秒级时间戳
    destination = open(os.path.join("static/pic", name), 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in pic.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    return name


def savePics(pics):
    if not pics:
        return False
    names = []
    for pic in pics:
        name = str(int(round(time.time() * 1000))) + file_extension(pic.name)  # 毫秒级时间戳
        destination = open(os.path.join("static/pic", name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in pic.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        names.append(name)
    return names


def getOnlineUser(request):
    user_id = request.COOKIES.get('user_id')
    islogin = True
    if user_id is None:
        islogin = False
        data = {
            'islogin': islogin,
        }
    else:
        user = models.user.objects.get(id=user_id)
        data = {
            'user_id': user_id,
            'user_head': getHeadPath(user.user_head),
            'user_name': user.username,
            'real_name': user.real_name,
            'introduce': user.introduce,
            'email': user.email,
            'islogin': islogin,
        }
    return data


def strToArr(pic_str):
    try:
        arr = ast.literal_eval(pic_str)
    except:
        return []
    else:
        return arr


status_dict = {
    0: '未审核',
    1: '已审核',
    2: '协调中',
    3: '已完成'
}
status_btn_type = {
    0: 'btn-warning',
    1: 'btn-success',
    2: 'btn-danger',
    3: 'btn-default'
}
GENERAL_USER = 0
JURY_USER = 1
COMPANY_USER = 2


def getComplaintData(complaint_list):
    l = []
    for e in complaint_list:
        l.append({
            'id': e.id,
            'title': e.title,
            'content': e.content,
            'user_name': e.user_id.username,
            'pic': getPicPath(e.pic),  # 第一张图
            'reply_amount': e.reply_amount,
            'status': status_dict[e.status],
            'type': status_btn_type[e.status]
        })
    return l


def getStaticData(key):
    try:
        data = models.static_data.objects.get(key=key)
    except models.static_data.DoesNotExist:
        return ''
    return data.value


def saveStaticData(key, value):
    try:
        data = models.static_data.objects.get(key=key)
    except models.static_data.DoesNotExist:
        data = models.static_data(key=key, value=value)
        data.save()
        return
    else:
        if value is not None and value != '' and value is not False:
            data.value = value
            data.save()
