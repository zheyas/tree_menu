
from django.contrib import admin
from django.urls import path, re_path
from tree_menu import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='home'),
    re_path(r'^(?P<slug>[\w/-]+)/$', views.universal_page, name='universal_page'),
]
