from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings





urlpatterns = [

    path('inicio/',views.mi_vista, name='mi_vista'),
    path('', views.mi_vista2, name='mi_vista2'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)