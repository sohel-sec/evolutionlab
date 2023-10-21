from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def stream_celery_logs(request):
    log_file_path = "/path/to/celery.log"  # Replace with the actual path to your Celery worker log
    context = {}
    return render(request, "list_view.html", context)

def stream_nginx_logs(request):
    context = {
        'message' : 'This is a log....',
        'room_name' : 'room_num1'
    }
    return render(request, "websocketapp/nginx_log.html", context)

