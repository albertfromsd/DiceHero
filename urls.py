
from django.urls import path, include

urlpatterns = [
    path('', include('dice_hero_app.urls')),
    path('', include('hero_mgr.urls')),
    path('', include('battle_system.urls')),
]
