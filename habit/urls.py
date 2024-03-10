from django.urls import path

from habit.apps import HabitConfig
from habit.views import HabitApiList, HabitUpdateApiView, HabitDestroyApiView, HabitDetailApiView, PublicHabitApiList

app_name = HabitConfig.name

urlpatterns = [
    path('habits/', HabitApiList.as_view(), name='habit-list-create'),
    path('habits/public/', PublicHabitApiList.as_view(), name='public-habit-list'),
    path('habits/<int:pk>/', HabitDetailApiView.as_view(), name='habit'),
    path('habits/<int:pk>/edit/', HabitUpdateApiView.as_view(), name='habit-update'),
    path('habits/<int:pk>/delete/', HabitDestroyApiView.as_view(), name='habit-delete')
]
