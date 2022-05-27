from django.urls import path
from linux.views import IndexView, RunView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('run/', RunView.as_view(), name='run'),
]
