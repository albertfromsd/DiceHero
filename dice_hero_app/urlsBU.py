from django.urls import path, include
# from rest_framework import routers
from . import views

urlpatterns = [
    path('post_data_check', views.post_data_check),

#### LOG IN ####
    path('user_login', views.user_login),
    path('process_login', views.process_login),
    path('choose_hero', views.choose_hero),
#### MAIN PAGE ####
    path('dice_hero', views.dice_hero),
#### REGISTER USER / CREATE HERO ####
    path('registration', views.registration),
    path('process_registration', views.process_registration),
    path('create_hero', views.create_hero),
    path('process_create_hero', views.process_create_hero),
    path('hero_created', views.hero_created),
#### ROLLS AND RESET ####
    path('hero_roll', views.hero_roll),
    path('enemy_roll', views.enemy_roll),
    path('dice_reset', views.dice_reset),
#### <[HERO GOD]> ####
    path('god_hero', views.god_hero),
    path('process_god_hero', views.process_god_hero),
    path('edit_hero', views.edit_hero),
    path('del_hero', views.del_hero),
#### <[ENEMY GOD]> ####
    path('god_enemy', views.god_enemy),
    path('process_god_enemy', views.process_god_enemy),
    path('edit_enemy', views.edit_enemy),
    path('del_enemy', views.del_enemy),
#### <[DICEFACE GOD]> ####
    path('god_diceface', views.god_diceface),
    path('process_god_diceface', views.process_god_diceface),
    path('del_diceface', views.del_diceface),
    path('edit_diceface', views.edit_diceface),
    path('basic_wpndfaces', views.basic_wpndfaces),
    path('basic_armordfaces', views.basic_armordfaces),
#### <[DICE GOD]> ####
    path('god_dice', views.god_dice),
    path('process_god_dice', views.process_god_dice),
    path('del_dice', views.del_dice),
    path('edit_dice', views.edit_dice),
    path('basic_wpndice', views.basic_wpndice),
    path('basic_armordice', views.basic_armordice),
#### <[EQUIPMENT GOD]> ####
    path('god_equip', views.god_equip),
    path('process_god_equip', views.process_god_equip),
    path('edit_equip', views.edit_equip),
    path('del_equip', views.del_equip),
# #### <[ACCESSORY GOD]> ####
#     path('god_accessory', views.god_accessory),
#     path('process_god_accessory', views.process_god_accessory),
#### <[ITEM GOD]> ####
    path('god_item', views.god_item),
    path('process_god_item', views.process_god_item),

#### SHOP ####
    path('equipment_shop', views.equipment_shop),
    path('process_equipment_shop', views.process_equipment_shop),
    path('dice_shop', views.dice_shop),
    path('process_dice_shop', views.process_dice_shop),
    path('levelup', views.levelup),
    path('process_levelup', views.process_levelup),
### HERO MANAGER ###
    path('inspect_hero', views.inspect_hero),
    path('process_inspect_hero', views.process_inspect_hero),
    path('inventory', views.inventory),
    path('process_inventory', views.process_inventory),

]
