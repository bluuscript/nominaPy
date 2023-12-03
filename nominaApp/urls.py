"""
URL configuration for nominaApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from nominaApp.views import usuario as user_views
from nominaApp.views import personal as personal_views
from nominaApp.views import rrhh as rrhh_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #  Load views for Usuario
    path('', user_views.index, name="index"),
    path("login/", user_views.login, name="login"),
    path('forgot/', user_views.forgot, name='forgot'),
    path('register/', user_views.register, name='register'),
    path('logout/', user_views.logout, name='logout'),
    #  Load views for  Personal Empresa 
    path('personal/inicio/', personal_views.inicio, name='personal-inicio'),
    path('personal/mi-registro/', personal_views.mi_registro, name='mi-registro'),
    path('personal/modificar-registro/', personal_views.modificar_registro, name='modificar-registro'),
    path('personal/mis-solicitudes/', personal_views.mis_solicitudes , name='ver-solicitudes'),
    path('personal/enviar-solicitud/', personal_views.enviar_solicitud, name='enviar-solicitud'),
    #  Load views for  Personal de RRHH
    path('rrhh/inicio/', rrhh_views.inicio, name='rrhh-inicio'),
    path('rrhh/mi-registro/', personal_views.mi_registro, name='ver-registro'),
    path('rrhh/modificar-registro/', personal_views.modificar_registro, name='modificar-registro'),
    path('rrhh/mis-solicitudes/', personal_views.mis_solicitudes, name='ver-solicitudes'),
    path('rrhh/enviar-solicitud/', personal_views.enviar_solicitud, name='enviar-solicitud'),
    # Load  views for RRHH
    path('rrhh/nomina/', rrhh_views.nomina_personal, name='nomina'),
    path('rrhh/nomina/eliminar-registro/', rrhh_views.eliminar_registro_personal, name='nomina-eliminar-registro'),
    path('rrhh/nuevo-registro/', rrhh_views.nuevo_registro_personal, name='nuevo-registro'),
    path('rrhh/nomina/modificar-registro/', rrhh_views.modificar_registro_personal, name='nomina-modificar-registro'),
    path('rrhh/solicitudes/', rrhh_views.solicitudes_personal, name='solicitudes'),
]
