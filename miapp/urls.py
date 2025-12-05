from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.saludo, name="segundario"),
    path("principal/", views.vista, name="principal"),
    path("formulario/", views.formulario, name="formulario"),
    path("formulario/editar/<int:id>/", views.editar, name="editar"),
    path("login/", views.login, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("usuarios/", views.usuarios, name="usuarios"),
    path("eliminar/<int:id>/", views.eliminar, name="eliminar"),
]
