from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms

from .models import *
from datetime import *
import random


##################################
####      DICE HERO MAIN      #### 
##################################
def dice_hero(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    #### Redirect if no login detected ####
    if "userid" not in request.session:
        return redirect("/user_login")

    if "hero_id" not in request.POST:
        if "hero_id" not in request.session:
            return redirect('/choose_hero')
    else:
        request.session["hero_id"]=request.POST["hero_id"]

    userid=request.session["userid"]
    username=request.session["username"]

    #### Retrieve Hero ####
    hero_id=request.session["hero_id"]
    hero=Hero.objects.get(id=hero_id)
    hero_name=Hero.objects.get(id=hero_id).name
    hero_hpb=Hero.objects.get(id=hero_id).hp_base

    #### Retrieve Enemy ####
    enemy_hpb=100
    if "enemy_life" not in request.session:
        request.session["enemy_life"]=100  
    if "hero_life" not in request.session:
        request.session["hero_life"]=hero_hpb
# run a for loop depending on number of dice slots/rolls
# NOT for the number of sides on a die
    if "enemy_roll" not in request.session:
        request.session["enemy_roll"]=[0, 0, 0, 0, 0, 0]
    if "enemy_attack" not in request.session:
        request.session["enemy_attack"]=0
    if "hero_roll" not in request.session:
        request.session["hero_roll"]=[0, 0, 0, 0, 0, 0]
    if "hero_attack" not in request.session:
        request.session["hero_attack"]=0

    if "enemy_log" not in request.session:
        request.session["enemy_log"]=[]
    if "hero_log" not in request.session:
        request.session["hero_log"]=[]

    enemy_life=request.session["enemy_life"]
    hero_life=request.session["hero_life"]

    enemy_roll=request.session["enemy_roll"]
    enemy_attack=request.session["enemy_attack"]
    hero_roll=request.session["hero_roll"]
    hero_attack=request.session["hero_attack"]

    enemy_log=("<br>".join(request.session["enemy_log"]))
    hero_log=("<br>".join(request.session["hero_log"]))

    request.session["enemy_life"]=enemy_life-hero_attack
    request.session["hero_life"]=hero_life-enemy_attack
    request.session.save()

    context = {
        #user dictionary
        "userid": userid,
        "username": username,

        #hero dictionary
        "all_hero_info": hero,
        "hero_name": hero_name,
        "hero_id": hero_id,

        #enemy variables
        "enemy_life": enemy_life - hero_attack,
        "enemy_hpb": enemy_hpb,
        "enemy_roll": enemy_roll,
        "enemy_attack": enemy_attack,

        #hero variables
        "hero_life": hero_life - enemy_attack,
        "hero_hpb": hero_hpb,
        "hero_roll": hero_roll,
        "hero_attack": hero_attack,

        #other variables
        "enemy_log":enemy_log,
        "hero_log": hero_log,
    }

    if request.session["enemy_life"] < 1:
        return render(request, "success.html", context)
    if request.session["hero_life"] < 1:
        return render(request, "fail.html", context)

    request.session["enemy_attack"]=0
    request.session["hero_attack"]=0
    
    return render(request, "dice_hero_index.html", context)




####################################
####         Hero Roll          #### 
####################################
def inspect_hero(request):
    pass

def process_inspect_hero(request):
    pass
def hero_roll(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

# run a for loop depending on number of dice slots/rolls
# NOT for the number of sides on a die
    if request.POST["hero_weapon"]=="w1":
        hero_dice=[0, 1, 2, 2, 2, 4]
    if request.POST["hero_weapon"]=="w2":
        hero_dice=[0, 0, 0, 4, 4, 4]
    request.session["enemy_attack"]=0
    request.session["enemy_roll"]=[0, 0, 0, 0, 0, 0]
    request.session["hero_attack"]=0
    for i in range(0, len(hero_dice), 1):
        num=random.randint(0, 5)
        request.session["hero_roll"][i]=hero_dice[num]
        request.session["hero_attack"]+=request.session["hero_roll"][i]
    request.session["hero_log"].insert(0, "Hero attacks for "+str(request.session["hero_attack"])+ "!")
    print(request.session["hero_roll"])
    print(request.session["hero_attack"])
    request.session.save()
    return redirect("/dice_hero")

def equipment_shop(request):

    context = {
        
    }

    return render(request, "equipment_shop.html", context)

def process_equipment_shop(request):
    pass

def dice_shop(request):
    pass

def process_dice_shop(request):
    pass

def levelup(process):
    pass

def process_levelup(request):
    pass

def inventory(request):
    pass

def process_inventory(request):
    pass

####################################
####           End              #### 
####################################
