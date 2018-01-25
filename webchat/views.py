from django.shortcuts import render, HttpResponse
import bbs.views
from django.contrib.auth.decorators import login_required
from webchat import models
import queue, json, time

# Create your views here.

GLOBAL_MSG_QUEUES = {}


@login_required
def dashboard(request):
    return render(request, 'webchat/dashboard.html', {'category_list': bbs.views.category_list})


@login_required
def send_msg(request):
    # print(request.POST)
    msg_data = request.POST.get('data')
    if msg_data:
        msg_data = json.loads(msg_data)

        time_string = time.strftime("%H:%M:%S")
        hour = time_string.split(':')[0]
        if int(time_string.split(':')[0]) > 12:
            hour = int(time_string.split(':')[0]) - 12
        time_string = "下午%s:%s:%s" % (hour, time_string.split(':')[1], time_string.split(':')[2])
        msg_data['timestamp'] = time_string
        if msg_data['type'] == 'single':
            if not GLOBAL_MSG_QUEUES.get(int(msg_data['to'])):
                GLOBAL_MSG_QUEUES[int(msg_data['to'])] = queue.Queue()
            GLOBAL_MSG_QUEUES[int(msg_data['to'])].put(msg_data)
            print(msg_data)
        else:
            # group chat
            group_obj = models.WebGroup.objects.get(id=int(msg_data['to']))
            for member in group_obj.members.select_related():
                if not GLOBAL_MSG_QUEUES.get(member.id):  # 如果字典里不存在该用户的queue
                    GLOBAL_MSG_QUEUES[member.id] = queue.Queue()
                if member.id != request.user.userprofile.id:
                    GLOBAL_MSG_QUEUES[member.id].put(msg_data)
    else:
        return HttpResponse("no message")
    # print(GLOBAL_MSG_QUEUES)
    return HttpResponse('---msg sent---')


@login_required
def get_new_msg(request):
    if request.user.userprofile.id not in GLOBAL_MSG_QUEUES:
        print("no queue for user [%s]" % request.user.userprofile.id, request.user)
        GLOBAL_MSG_QUEUES[request.user.userprofile.id] = queue.Queue()
        print("queue established:", GLOBAL_MSG_QUEUES[request.user.userprofile.id])
    q_obj = GLOBAL_MSG_QUEUES[request.user.userprofile.id]
    msg_count = q_obj.qsize()
    msg_list = []
    if msg_count > 0:
        for msg in range(msg_count):
            msg_list.append(q_obj.get())
    else:
        # 没有消息
        print("no message for ", request.user.userprofile.id)
        try:
            msg_list.append(q_obj.get(timeout=60))
        except queue.Empty:
            print("\033[41;1mno msg for [%s][%s], timeout\033[0m" % (
            request.user.userprofile.id, request.user.userprofile.name))
    return HttpResponse(json.dumps(msg_list))


def file_upload(request):
    print(request.POST, request.FILES)
    file_obj = request.FILES.get('file')
    with open("uploads/%s" % file_obj.name, 'wb') as new_file_obj:
        for chunk in file_obj.chunks():
            new_file_obj.write(chunk)
    return HttpResponse("upload succcess test")
