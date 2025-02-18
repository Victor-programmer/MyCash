from django.urls import path
from . import views
from .views import historico_view

urlpatterns = [
    path('', views.index, name='index'),
    path('criar/', views.criar_conta_view, name='criar_conta'),
    path("historico/", historico_view, name="historico"),
    path('desativar_conta/<int:id>/', views.desativar_conta_view, name='desativar_conta'),
    path('transferir_saldo/', views.transferir_saldo_view, name='transferir_saldo'),
    path('movimentar_dinheiro/', views.movimentar_dinheiro_view, name='movimentar_dinheiro'),
]

