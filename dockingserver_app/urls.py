from django.urls import path

from . import views

app_name = 'dockingserver_app'

urlpatterns = [
    path(r'api', views.DockingAPI.as_view(), name='docking_api')
]
