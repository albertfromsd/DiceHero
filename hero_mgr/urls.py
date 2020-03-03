from django.urls import path, include
from . import views

urlpatterns = [

#### SHOP ####
    path('equipment_shop', views.equipment_shop),
    path('process_equipment_shop', views.process_equipment_shop),
    path('dice_shop', views.dice_shop),
    path('process_dice_shop', views.process_dice_shop),
    path('levelup', views.levelup),
    path('process_levelup', views.process_levelup),
#### ROLLS AND RESET ####
    path('inspect_hero', views.inspect_hero),
    path('process_inspect_hero', views.process_inspect_hero),

    path('inventory', views.inventory),
    path('process_inventory', views.process_inventory),

]
