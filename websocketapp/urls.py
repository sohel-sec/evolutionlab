from django.urls import include, path
from .views import stream_nginx_logs


urlpatterns = [
    path('stream_nginx_logs/', stream_nginx_logs, name='stream_nginx_logs')
]
