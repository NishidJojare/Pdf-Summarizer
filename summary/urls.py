from django.urls import path
from summary import views

urlpatterns = [
    path('',views.upload_pdf,name='upload_pdf'),
]
