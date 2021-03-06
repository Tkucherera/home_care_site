from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('training', views.training, name='training'),
    path('certificate', views.certificate, name='certificate'),
    path('module', views.module, name='module'),
    path('portal', views.portal, name='portal'),
]