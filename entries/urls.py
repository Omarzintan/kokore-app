from django.urls import path
from entries import views

urlpatterns = [
        path("", views.entry_index, name="entry_index"),
        path("<int:pk>/", views.entry_detail, name="entry_detail"),
]

