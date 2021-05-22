from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from netmiko import ConnectHandler
import netmiko
from time import time
from multiprocessing import Queue
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import post_data,hostname,user_data
from .serializers import PostSerializer
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

@csrf_exempt
@api_view(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@api_view(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been Updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html',context)

def ssh_login(request):
    return render(request, 'users/ssh_login.html')

output_str = []

def ssh_session(ip1, command, user, password, os_type, output_q):
    import time
    output_String = ""
    print(f"{ip1} is the current device")
    # Place what you want each thread to do here, for example connect to SSH, run a command, get output
    try:
        # output_q = Queue()
        output_dict = {}
        hostname = ip1
        router = {'device_type': os_type, 'ip': ip1, 'username': user, 'password': password,
                  'secret': 'G0t2BTuf',
                  'verbose': False, }
        ssh_session1 = ConnectHandler(**router)
        time.sleep(1)
        cmd = command.split(',')
        #print(command)
        string_output = ""
        for comm in cmd:
            ssh_session1.enable()
            output = ssh_session1.send_command(comm)
            time.sleep(.5)
            comms = "command# "+ comm + '\n'
            string_output+= "\n" + comms + "\n" + output + "\n"
        if "syntax error" in string_output:
            string_output = ""
            for comm in cmd:
                output = ssh_session1.send_config_set(comm)
                time.sleep(.5)
                comms = "command# " + comm + '\n'
                string_output += "\n" + comms + "\n" + output + "\n"

        with open(ip1 + '.text', 'w') as file_var:
            file_var.write(string_output)
            # time.sleep(0.5)
        output_str.append(string_output)
        output_str.append(ip1)
        output_dict[hostname] = string_output.strip()
        output_q.put(output_dict)
        ssh_session1.disconnect()

    except netmiko.ssh_exception.NetMikoAuthenticationException:
        print('=== Bad credentials===' + ip1)
    except netmiko.ssh_exception.NetMikoTimeoutException:
        print('=== device unreachable===' + ip1)

def connect_to_device(request):
    import threading
    from flask import render_template, redirect
    start_time = time()

    if request.method == 'POST':
        ip1 = request.POST.get('ip')
        user = list(request.POST.get('user'))
        command = list(request.POST.get('command'))
        password = list(request.POST.get('password'))
        os_type = request.POST.get('os_type')
        output_q = Queue()
        ip = ip1.split(',')
        print(type(user))
        Threads = []
        for ip1 in ip:
            my_thread = threading.Thread(target=ssh_session, args=(ip1, command, user, password, os_type, output_q))
            my_thread.start()
            Threads.append(my_thread)

        main_thread = threading.currentThread()
        for thread in Threads:
            thread.join()
        end_time = time()
        final_time = end_time - start_time
        print('\n---- Total elapsed time is=', final_time)

        num_array = []  # temparary storing the output
        output_strstr1 = ''
        formating = '*' * 100
        while not output_q.empty():
            my_dict = output_q.get()  # collecting the CI name and output
            for k, val in my_dict.items():
                # time.sleep(1)
                z1 = num_array.append(">>>Device: " + k)  # appending the CI to array
                z2 = num_array.append(val)  # appending the output to array
        out = []
        for x1 in num_array:
            output_strstr1 = output_strstr1 + "\n" + x1 + '\n' + '\n' + formating + '\n'

        return render(request, 'users/input_form.html', context={'output':output_strstr1})
    # if current_user.is_authenticated:
    return render(request, 'users/connect_to_device.html')
    # else:
    #     flash('Invalid or Session Expired!!!! You must login first first', 'danger')
    #     return redirect(url_for('login'))

my_api = []

@api_view(['GET'])
def post_ips(request):
    if request.method == 'GET':
        data = hostname.objects.all()
        ip = request.query_params.get('IP_address', None)
        return (data)
@api_view(['GET', 'POST'])
def data_posted_form_one(request):
    if request.method == 'GET':
        tutorials = post_data.objects.all()
        title = request.query_params.get('title', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        tutorials_serializer = PostSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = PostSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def data_posted_form_two(request):
    if request.method == 'GET':
        tutorials = post_data.objects.all()

        title = request.query_params.get('title', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)

        tutorials_serializer = PostSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        print(tutorial_data)
        tutorial_serializer = PostSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)

def get_db_obj(request):
    obj = user_data.objects.all()
    obj1 = hostname.objects.all()
    return render(request, 'users/user_list.html',{'user_list': obj,'hostname':obj1,
                                         })
