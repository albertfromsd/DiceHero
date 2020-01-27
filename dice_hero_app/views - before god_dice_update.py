from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
import bcrypt

# from django.contrib.auth import (
#     authenticate,
#     get_user_model
#     login,
#     logout,
# )
from .models import *
from datetime import *
import random

####################################
####      POST DATA CHECK       #### 
####################################

def post_data_check(request):
    # if "dob" in request.POST:
    #     dob=request.POST["dob"]
    # dobStr=dob[0:4]+dob[5:7]+dob[8:]
    # dobInteger=int(dobStr)
    # today=int(datetime.today().strftime('%Y%m%d'))
    # if dobInteger > today:
    #     message = "Cannot be born after today's date"
    # else:
    #     message = "Valid date"
    context = {
        "postData": request.POST,
        "sessionData": request.session,
        "message": message
        # "username": request.POST["username"],
        # "email": request.POST["email"],
        # "dobStr": dobStr,
        # "dobInteger": dobInteger,
        # "today": today,
        # "message": message,
    }
    
    return render(request, "post_data_check.html", context)

####################################
#####      Register User       #####
####################################
def registration(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    if "session" in request:
        request.session.clear()
    return render(request, "register_new_user.html")

def process_registration(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    errors=User.objects.basic_validator(request.POST)
    #### Set Variables ####
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/registration')
    else:
        username=request.POST["username"]
        email=request.POST["email"]
        pw_prehash=request.POST['password']
        pw_hashed = bcrypt.hashpw(pw_prehash.encode(), bcrypt.gensalt()).decode()

        User.objects.create(username=username, email=email, password=pw_hashed)
        request.session["userid"] = User.objects.last().id
        request.session["username"] = User.objects.last().username

        return redirect("/create_hero")

####################################
#####       Create Hero        #####
####################################
def create_hero(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))
    
    message = "Create a new hero!"

    context = {
        "message": message,
        "username": request.session["username"],
        "userid": request.session["userid"],
    }

    return render(request, "create_new_hero.html", context)

####################################
#####   Process Create Hero    #####
####################################
def process_create_hero(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))
    
    #### Set Variables ####
    userid=request.session["userid"]
    user=User.objects.get(id=userid)
    hero_name=request.POST["hero_name"]
    hp_base=int(request.POST["hp_base"])
    atk_base=int(request.POST["atk_base"])
    def_base=int(request.POST["def_base"])
    int_base=int(request.POST["int_base"])
    spd_base=int(request.POST["spd_base"])

    #### CREATE ####
    Hero.objects.create(name=hero_name, user=user, hp_base=hp_base, atk_base=atk_base, def_base=def_base, int_base=int_base, spd_base=spd_base)

    #### NEW HERO STATS ####
    request.session["hero_name"]=Hero.objects.last().name
    request.session["hero_id"]=Hero.objects.last().id
    request.session["hero_hp"]=Hero.objects.last().hp_base
    request.session["hero_atk"]=Hero.objects.last().atk_base
    request.session["hero_def"]=Hero.objects.last().def_base
    request.session["hero_int"]=Hero.objects.last().int_base
    request.session["hero_spd"]=Hero.objects.last().spd_base
    request.session["hero_gold"]=Hero.objects.last().gold
    request.session["hero_gems"]=Hero.objects.last().gems

    return redirect("/hero_created")


####################################
#####    Created Hero Stats    #####
####################################
def hero_created(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    if "new_hero" not in request.session:
        redirect('/user_login')
    
    hero_name=request.session["hero_name"]
    hero_id=request.session["hero_id"]
    hero_hp=request.session["hero_hp"]=Hero.objects.last().hp_base
    hero_atk=request.session["hero_atk"]=Hero.objects.last().atk_base
    hero_def=request.session["hero_def"]=Hero.objects.last().def_base
    hero_int=request.session["hero_int"]=Hero.objects.last().int_base
    hero_spd=request.session["hero_spd"]=Hero.objects.last().spd_base
    hero_gold=request.session["hero_gold"]=Hero.objects.last().gold
    hero_gems=request.session["hero_gems"]=Hero.objects.last().gems

    context = {
        "new_hero": Hero.objects.last(),
        "name": hero_name,
        "id": hero_id,
        "hp": hero_hp,
        "atk": hero_atk,
        "def": hero_def,
        "int": hero_int,
        "spd": hero_spd,
        "gold": hero_gold,
        "gems": hero_gems,
    }

    return render(request, "new_hero_created.html", context)

####################################
####         Log In Page        #### 
####################################
def user_login(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    if "login_error" in request.session:
        error = request.session["login_error"]
        color = "red"
        del request.session["login_error"]
    else:
        error = " "
        color = "black"

    context = {
        "error": error,
        "color": color,
    }

    request.session.clear()

    return render(request, "user_login.html", context)


####################################
####       Process Log In       #### 
####################################
def process_login(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    if User.objects.filter(username=request.POST['username']).count()==1:
        user=User.objects.get(username=request.POST['username'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session["userid"]=user.id
            request.session["username"]=user.username
            if User.objects.get(id=request.session["userid"]).heroes.all().count()>0:
                return redirect("/choose_hero")
            else:
                return redirect("/create_hero")
        else:
            request.session["login_error"] = "Incorrect password"
            return redirect("/user_login")
    else:
        request.session["login_error"] = "No such user exists"
        return redirect("/user_login")

def choose_hero(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    userid = request.session["userid"]

    context= {
        "heroes": User.objects.get(id=userid).heroes.all()
    }

    return render(request, "choose_hero.html", context)

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
            

    #### Retrieve Hero ####
    hero_id=request.session["hero_id"]
    hero_name=Hero.objects.get(id=hero_id).name

    hero=Hero.objects.get(id=hero_id)

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

    # enemy_roll=request.session["enemy_roll"]
    # hero_roll=request.session["hero_roll"]

    enemy_attack=request.session["enemy_attack"]
    hero_attack=request.session["hero_attack"]

    enemy_log=("<br>".join(request.session["enemy_log"]))
    hero_log=("<br>".join(request.session["hero_log"]))

    request.session["enemy_life"]=enemy_life-hero_attack
    request.session["hero_life"]=hero_life-enemy_attack
    request.session.save()

    if request.session["enemy_life"] < 1:
        return render(request, "success.html")
    if request.session["hero_life"] < 1:
        return render(request, "fail.html")

    context = {
        #hero dictionary
        "all_hero_info": hero,
        "hero_name": hero_name,
        "hero_id": hero_id,

        #enemy variables
        "enemy_life": enemy_life - hero_attack,
        "enemy_hpb": enemy_hpb,
        "enemy_roll": request.session["enemy_roll"],
        "enemy_attack": enemy_attack,

        #hero variables
        "hero_life": hero_life - enemy_attack,
        "hero_hpb": hero_hpb,
        "hero_roll": request.session["hero_roll"],
        "hero_attack": hero_attack,

        #other variables
        "enemy_log":enemy_log,
        "hero_log": hero_log,
    }

    request.session["enemy_attack"]=0
    request.session["hero_attack"]=0
    
    return render(request, "dice_hero_index.html", context)


####################################
####         Enemy Roll         #### 
####################################
def enemy_roll(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

# run a for loop depending on number of dice slots/rolls
# NOT for the number of sides on a die

    enemy_dice = [1, 1, 2, 2, 2, 3]
    request.session["enemy_attack"]=0
    request.session["hero_attack"]=0
    request.session["hero_roll"]=[0, 0, 0, 0, 0, 0]
    for i in range(0, len(enemy_dice), 1):
        num=random.randint(0, 5)
        request.session["enemy_roll"][i]=enemy_dice[num]
        request.session["enemy_attack"]+=request.session["enemy_roll"][i]
    request.session["enemy_log"].insert(0, "Enemy attacks for "+str(request.session["enemy_attack"])+ "!")
    print(request.session["enemy_roll"])
    print(request.session["enemy_attack"])
    request.session.save()
    return redirect("/dice_hero")


####################################
####         Hero Roll          #### 
####################################
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



####################################
#####      God of Heroes       #####
####################################
def god_hero(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    if "new_hero_id" in request.session:
        new_hero_id=request.session["new_hero_id"]=Hero.objects.last().id


    context = {
        "all_heroes": Hero.objects.all(),
        "new_hero": Hero.objects.get(id=new_hero_id),

    }

    return render(request, "god_hero.html", context)

def edit_hero(request):
    if "edit_name" in request.POST:
        hero_to_edit=request.POST["edit_name"]
        new_name=request.POST["new_name"]
        name_to_edit=Hero.objects.get(id=hero_to_edit)
        name_to_edit.name=new_name
        name_to_edit.save()

    if "edit_element" in request.POST:
        hero_to_edit=request.POST["edit_element"]
        new_element=request.POST["new_element"]
        element_to_edit=Hero.objects.get(id=hero_to_edit)
        element_to_edit.element=new_element
        element_to_edit.save()

    if "edit_gold" in request.POST:
        hero_to_edit=request.POST["edit_gold"]
        new_gold=request.POST["new_gold"]
        gold_to_edit=Hero.objects.get(id=hero_to_edit)
        gold_to_edit.gold=new_gold
        gold_to_edit.save()

    if "edit_hp" in request.POST:
        hero_to_edit=request.POST["edit_hp"]
        new_hp=request.POST["new_hp"]
        hp_to_edit=Hero.objects.get(id=hero_to_edit)
        hp_to_edit.hp_base=new_hp
        hp_to_edit.save()

    if "edit_gems" in request.POST:
        hero_to_edit=request.POST["edit_gems"]
        new_gems=request.POST["new_gems"]
        gems_to_edit=Hero.objects.get(id=hero_to_edit)
        gems_to_edit.gems=new_gems
        gems_to_edit.save()

    if "edit_atk" in request.POST:
        hero_to_edit=request.POST["edit_atk"]
        new_atk=request.POST["new_atk"]
        new_atk_to_edit=Hero.objects.get(id=hero_to_edit)
        new_atk_to_edit.atk_base=new_atk
        new_atk_to_edit.save()

    if "edit_def" in request.POST:
        hero_to_edit=request.POST["edit_def"]
        new_def=request.POST["new_def"]
        def_to_edit=Hero.objects.get(id=hero_to_edit)
        def_to_edit.def_base=new_def
        def_to_edit.save()

    if "edit_int" in request.POST:
        hero_to_edit=request.POST["edit_int"]
        new_int=request.POST["new_int"]
        int_to_edit=Hero.objects.get(id=hero_to_edit)
        int_to_edit.int_base=new_int
        int_to_edit.save()

    if "edit_spd" in request.POST:
        hero_to_edit=request.POST["edit_spd"]
        new_spd=request.POST["new_spd"]
        spd_to_edit=Hero.objects.get(id=hero_to_edit)
        spd_to_edit.spd_base=new_spd
        spd_to_edit.save()

    if "edit_wpn1" in request.POST:
        hero_to_edit=request.POST["edit_wpn1"]
        new_wpn1=request.POST["new_wpn1"]
        wpn1_to_edit=Hero.objects.get(id=hero_to_edit)
        wpn1_to_edit.wpn1=new_wpn1
        wpn1_to_edit.save()
    
    if "edit_wpn2" in request.POST:
        hero_to_edit=request.POST["edit_wpn2"]
        new_wpn2=request.POST["new_wpn2"]
        wpn2_to_edit=Hero.objects.get(id=hero_to_edit)
        wpn2_to_edit.ability=new_wpn2
        wpn2_to_edit.save()

    if "edit_armor" in request.POST:
        hero_to_edit=request.POST["edit_armor"]
        new_armor=request.POST["new_armor"]
        armor_to_edit=Hero.objects.get(id=hero_to_edit)
        armor_to_edit.arm=new_armor
        armor_to_edit.save()

    return redirect("/god_hero")


def process_god_hero(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    hero_name=request.POST["hero_name"]
    hero_element=request.POST["hero_element"]
    hero_hp=request.POST["hero_hp"]
    hero_gold=request.POST["hero_gold"]
    hero_gems=request.POST["hero_gems"]
    hero_atk=request.POST["hero_atk"]
    hero_def=request.POST["hero_def"]
    hero_int=request.POST["hero_int"]
    hero_spd=request.POST["hero_spd"]
    hero_wpn1_id=request.POST["hero_wpn1"]
    hero_wpn1=Weapon.objects.get(id=hero_wpn1_id)
    hero_wpn2_id=request.POST["hero_wpn2"]
    hero_wpn2=Weapon.objects.get(id=hero_wpn2_id)
    hero_armor_id=request.POST["hero_armor"]
    hero_armor=Weapon.objects.get(id=hero_armor_id)

    Hero.objects.create(name=hero_name, element=hero_element, hp_base=hero_hp, gold=hero_gold, gems=hero_gems, atk_base=hero_atk, def_base=hero_def, int_base=hero_int, spd_base=hero_spd, wpn1=hero_wpn1, wpn2=hero_wpn2, arm=hero_armor)

    request.session["new_hero_id"]=Hero.objects.last().id

    return redirect("/god_hero")

def del_hero(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    hero_to_delete=request.POST["delete"]
    Hero.objects.get(id=hero_to_delete).delete()

    return redirect("/god_hero")

####################################
#####    God of DiceFaces      #####
####################################

# class DiceFaceViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = DiceFace.objects.all()
#     serializer_class = DiceFaceSerializer

def god_diceface(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    #[top] to load errorfree without request.POST/session
    if "df_ability" not in request.POST:
        request.session["df_ability"] = "None"
    else:
        request.session["df_ability"] = request.POST["df_ability"]

    if "df_critical" not in request.POST:
        request.session["df_critical"] = "False"
    else:
        request.session["df_critical"] = request.POST["df_critical"]

    if "df_id" not in request.session:
        df_id=" "
    else:
        df_id=request.session["df_id"]

    if "df_name" not in request.session:
        request.session["df_name"]=" "
    if "df_type" not in request.session:
        request.session["df_type"]=" "
    if "df_element" not in request.session:
        request.session["df_element"]=" "
    if "df_price" not in request.session:
        request.session["df_price"]=" "
    if "df_roll_value" not in request.session:
        request.session["df_roll_value"]=" "

    #[end] to load errorfree without request.POST/session

    
    df_name=request.session["df_name"]
    df_type=request.session["df_type"]
    df_element=request.session["df_element"]
    df_price=request.session["df_price"]
    df_roll_value=request.session["df_roll_value"]
    df_critical=request.session["df_critical"]
    df_ability=request.session["df_ability"]

    #DYNAMIC DATABASE
    df_db=" "
    db_title="No Database Chosen"
    new_df_type=" "

    if "df_type" in request.session:
        if request.session["df_type"]=="WpnDface":
            df_db=WpnDface.objects.all()
            db_title="Weapon Dice Faces"
            new_df_type="Weapon DiceFace"
        if request.session["df_type"]=="ArmorDface":
            df_db=ArmorDface.objects.all()
            db_title="Armor Dice Faces"
            new_df_type="Armor DiceFace"
    if "df_type" in request.POST:
        request.session["df_type"]=request.POST["df_type"]
        if request.POST["df_type"]=="WpnDface":
            df_db=WpnDface.objects.all()
            db_title="Weapon Dice Faces"
        if request.POST["df_type"]=="ArmorDface":
            df_db=ArmorDface.objects.all()
            db_title="Armor Dice Faces"

    if "error_msg" in request.session:
        error_msg = request.session["error_msg"]
        msg_color= "red"
        del request.session["error_msg"]
    else:
        error_msg = " Please enter stats below "
        msg_color="black"
        request.session["error_msg"] = " "
    
    hero_id=request.session["hero_id"]
    hero_name=Hero.objects.get(id=hero_id).name
    userid=request.session["userid"]
    username=request.session["username"]

    context = {
        "hero_id": hero_id,
        "hero_name": hero_name,
        "userid": userid,
        "username": username,
        "df_db": df_db,
        "db_title": db_title,
        "id": df_id,
        "type": new_df_type,
        "name": df_name,
        "element": df_element,
        "price": df_price,
        "roll_value": df_roll_value,
        "df_critical": df_critical,
        "df_ability": df_ability,
        "error_msg": error_msg,
        "msg_color": msg_color,
    }


    return render(request, "god_diceface.html", context)


def process_god_diceface(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    if "df_type" not in request.POST:
        request.session["error_msg"] = "Please select a Dice Face type"
        return redirect("/god_diceface")


    #[SESSION] from post data
    request.session["df_name"]=request.POST["df_name"]
    request.session["df_type"]=request.POST["df_type"]
    request.session["df_element"]=request.POST["df_element"]
    request.session["df_price"]=request.POST["df_price"]
    request.session["df_roll_value"]=request.POST["df_roll_value"]

    if "df_ability" not in request.POST:
        request.session["df_ability"] = "None"
    else:
        request.session["df_ability"] = request.POST["df_ability"]

    if "df_critical" not in request.POST:
        request.session["df_critical"] = "False"
    else:
        request.session["df_critical"] = request.POST["df_critical"]
    


    #[VARIABLES] from session
    df_name=request.session["df_name"]
    # heroid=Hero.objects.get(id=request.session["hero_id"])
    df_element=request.session["df_element"]
    df_price=int(request.session["df_price"])
    df_roll_value=int(request.session["df_roll_value"])
    df_ability = request.session["df_ability"]
    df_critical=request.session["df_ability"]
    #df_forAtk defined above
    #df_ability defined above

    #[CREATE] WpnDFace
    if request.POST["df_type"] == "WpnDface":
        request.session["df_type"] = request.POST["df_type"]
        WpnDface.objects.create(name=df_name, price=df_price, roll_value=df_roll_value, critical=df_critical)
        request.session["df_id"]=WpnDface.objects.last().id
        request.session["df_name"]=WpnDface.objects.last().name
        request.session["df_price"]=WpnDface.objects.last().price
        request.session["df_roll_value"]=WpnDface.objects.last().roll_value
        request.session["df_critical"]=WpnDface.objects.last().critical
        # request.session["df_element"]=WpnDface.objects.last().element
        # request.session["df_ability"]=WpnDface.objects.last().ability

    #[CREATE] ArmorDFace
    if request.POST["df_type"] == "ArmorDface":
        request.session["df_type"] = request.POST["df_type"]
        ArmorDface.objects.create(name=df_name, price=df_price, roll_value=df_roll_value, critical=df_critical)
        request.session["df_id"]=ArmorDface.objects.last().id 
        request.session["df_name"]=ArmorDface.objects.last().name
        request.session["df_price"]=ArmorDface.objects.last().price
        request.session["df_roll_value"]=ArmorDface.objects.last().roll_value
        request.session["df_critical"]=ArmorDface.objects.last().critical
        # request.session["df_element"]=ArmorDface.objects.last().element
        # request.session["df_ability"]=ArmorDface.objects.last().ability

    return redirect("/god_diceface")

def del_diceface(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    df_to_delete=request.POST["delete"]

    if request.session["df_type"] == "WpnDface":
        WpnDface.objects.get(id=df_to_delete).delete()
    if request.session["df_type"] == "ArmorDface":
        ArmorDface.objects.get(id=df_to_delete).delete()

    return redirect("/god_diceface")

def edit_diceface(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))
    
    if request.session["df_type"] == "WpnDface":
        DiceFace=WpnDface
    if request.session["df_type"] == "ArmorDface":
        DiceFace=ArmorDface


    if "edit_owner" in request.POST:

        df_to_edit=request.POST["edit_owner"]
        new_hero_id=request.POST["new_owner"]
        name_to_edit=DiceFace.objects.get(id=df_to_edit)
        name_to_edit.owner_id=new_hero_id
        name_to_edit.save()

    if "edit_parent" in request.POST:
        df_to_edit=request.POST["edit_parent"]
        new_parent_id=request.POST["new_parent"]
        name_to_edit=DiceFace.objects.get(id=df_to_edit)
        name_to_edit.parent_id=new_parent_id
        name_to_edit.save()

    if "edit_name" in request.POST:
        df_to_edit=request.POST["edit_name"]
        new_name=request.POST["new_name"]
        name_to_edit=DiceFace.objects.get(id=df_to_edit)
        name_to_edit.name=new_name
        name_to_edit.save()

    if "edit_roll_value" in request.POST:
        df_to_edit=request.POST["edit_roll_value"]
        new_roll_value=request.POST["new_roll_value"]
        roll_value_to_edit=DiceFace.objects.get(id=df_to_edit)
        roll_value_to_edit.roll_value=new_roll_value
        roll_value_to_edit.save()

    if "edit_forAtk" in request.POST:
        df_to_edit=request.POST["edit_forAtk"]
        new_forAtk=request.POST["new_forAtk"]
        forAtk_to_edit=DiceFace.objects.get(id=df_to_edit)
        forAtk_to_edit.forAtk=new_forAtk
        forAtk_to_edit.save()

    if "edit_price" in request.POST:
        df_to_edit=request.POST["edit_price"]
        new_price=request.POST["new_price"]
        price_to_edit=DiceFace.objects.get(id=df_to_edit)
        price_to_edit.price=new_price
        price_to_edit.save()

    if "edit_element" in request.POST:
        df_to_edit=request.POST["edit_element"]
        new_element=request.POST["new_element"]
        element_to_edit=DiceFace.objects.get(id=df_to_edit)
        element_to_edit.element=new_element
        element_to_edit.save()

    if "edit_critical" in request.POST:
        df_to_edit=request.POST["edit_critical"]
        new_critical=request.POST["new_critical"]
        critical_to_edit=DiceFace.objects.get(id=df_to_edit)
        critical_to_edit.critical=new_critical
        critical_to_edit.save()
    
    if "edit_ability" in request.POST:
        df_to_edit=request.POST["edit_ability"]
        new_ability=request.POST["new_ability"]
        ability_to_edit=DiceFace.objects.get(id=df_to_edit)
        ability_to_edit.ability=new_ability
        ability_to_edit.save()

    return redirect("/god_diceface")


###############################
#####       Dice God      #####
###############################
def god_dice(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    #[LOAD] to load error free without request.POST/session
    if "wpn_dice_ability" not in request.POST:
        wpn_dice_ability = "None"
    else:
        wpn_dice_ability = request.POST["wpn_dice_ability"]

    #[CONTEXT] SET VARIABLES FROM SESSION
    if "wpn_dice_name" not in request.session:
        wpn_dice_name=" "
    else:
        wpn_dice_name=request.session["wpn_dice_name"]

    if "wpn_dice_id" not in request.session:
        wpn_dice_id=" "
    else:
        wpn_dice_id=request.session["wpn_dice_id"]

    if "wpn_dice_element" not in request.session:
        wpn_dice_element=" "
    else:
        wpn_dice_element=request.session["wpn_dice_element"]

    if "wpn_dice_price" not in request.session:
        wpn_dice_price=" "
    else:
        wpn_dice_price=request.session["wpn_dice_price"]

    #[CONTEXT] DICE SIDE VARs FROM SESSION (saved in /process_god_dice)
    # if it does not exist, set value to DiceFace ID#44 (Basic 0)
    if "wpn_df1" not in request.session:
        wpn_df1 = 44
    else:
        wpn_df1 = request.session["wpn_df1"]

    if "wpn_df2" not in request.session:
        wpn_df2 = 44
    else:
        wpn_df2 = request.session["wpn_df2"]

    if "wpn_df3" not in request.session:
        wpn_df3 = 44
    else:
        wpn_df3 = request.session["wpn_df3"]

    if "wpn_df4" not in request.session:
        wpn_df4 = 44
    else:
        wpn_df4 = request.session["wpn_df4"]

    if "wpn_df5" not in request.session:
        wpn_df5 = 44
    else:
        wpn_df5 = request.session["wpn_df5"]

    if "wpn_df6" not in request.session:
        wpn_df6 = 44
    else:
        wpn_df6 = request.session["wpn_df6"]

    context = {
        "all_wpn_dice": WpnDice.objects.all(),
        "wpn_dice_name": wpn_dice_name,
        "wpn_dice_id": wpn_dice_id,
        "wpn_dice_element": wpn_dice_element,
        "wpn_dice_price": wpn_dice_price,
        "wpn_dice_ability": wpn_dice_ability,
        "wpn_df1": wpn_df1,
        "wpn_df2": wpn_df2,
        "wpn_df3": wpn_df3,
        "wpn_df4": wpn_df4,
        "wpn_df5": wpn_df5,
        "wpn_df6": wpn_df6,
        "wpn_df1_name": DiceFace.objects.get(id=wpn_df1).name,
        "wpn_df2_name": DiceFace.objects.get(id=wpn_df2).name,
        "wpn_df3_name": DiceFace.objects.get(id=wpn_df3).name,
        "wpn_df4_name": DiceFace.objects.get(id=wpn_df4).name,
        "wpn_df5_name": DiceFace.objects.get(id=wpn_df5).name,
        "wpn_df6_name": DiceFace.objects.get(id=wpn_df6).name,

    }

    return render(request, "god_dice.html", context)

def del_dice(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    dice_to_delete=request.POST["delete"]
    WpnDice.objects.get(id=dice_to_delete).delete()

    return redirect("/god_dice")

def edit_dice(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    if "edit_name" in request.POST:
        d_to_edit=request.POST["edit_name"]
        new_name=request.POST["new_name"]
        name_to_edit=WpnDice.objects.get(id=d_to_edit)
        name_to_edit.name=new_name
        name_to_edit.save()

    if "edit_price" in request.POST:
        d_to_edit=request.POST["edit_price"]
        new_price=request.POST["new_price"]
        price_to_edit=WpnDice.objects.get(id=d_to_edit)
        price_to_edit.price=new_price
        price_to_edit.save()

    if "edit_element" in request.POST:
        d_to_edit=request.POST["edit_element"]
        new_element=request.POST["new_element"]
        element_to_edit=WpnDice.objects.get(id=d_to_edit)
        element_to_edit.element=new_element
        element_to_edit.save()

    if "edit_df1" in request.POST:
        d_to_edit=request.POST["edit_df1"]
        new_df1=request.POST["new_df1_id"]
        df1_to_edit=WpnDice.objects.get(id=d_to_edit)
        df1_to_edit.dface1=DiceFace.objects.get(id=new_df1)
        df1_to_edit.save()

    if "edit_df2" in request.POST:
        d_to_edit=request.POST["edit_df2"]
        new_df2=request.POST["new_df2_id"]
        df2_to_edit=WpnDice.objects.get(id=d_to_edit)
        df2_to_edit.dface2=DiceFace.objects.get(id=new_df2)
        df2_to_edit.save()

    if "edit_df3" in request.POST:
        d_to_edit=request.POST["edit_df3"]
        new_df3=request.POST["new_df3_id"]
        df3_to_edit=WpnDice.objects.get(id=d_to_edit)
        df3_to_edit.dface3=DiceFace.objects.get(id=new_df3)
        df3_to_edit.save()
    
    if "edit_df4" in request.POST:
        d_to_edit=request.POST["edit_df4"]
        new_df4=request.POST["new_df4_id"]
        df4_to_edit=WpnDice.objects.get(id=d_to_edit)
        df4_to_edit.dface4=DiceFace.objects.get(id=new_df4)
        df4_to_edit.save()

    if "edit_df5" in request.POST:
        d_to_edit=request.POST["edit_df5"]
        new_df5=request.POST["new_df5_id"]
        df5_to_edit=WpnDice.objects.get(id=d_to_edit)
        df5_to_edit.dface5=DiceFace.objects.get(id=new_df5)
        df5_to_edit.save()

    if "edit_df6" in request.POST:
        d_to_edit=request.POST["edit_df6"]
        new_df6=request.POST["new_df6_id"]
        df6_to_edit=WpnDice.objects.get(id=d_to_edit)
        df6_to_edit.dface6=DiceFace.objects.get(id=new_df6)
        df6_to_edit.save()
    
    if "edit_ability" in request.POST:
        d_to_edit=request.POST["edit_ability"]
        new_ability=request.POST["new_ability"]
        ability_to_edit=WpnDice.objects.get(id=d_to_edit)
        ability_to_edit.ability=new_ability
        ability_to_edit.save()

    return redirect("/god_dice")


def process_god_dice(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    #[CONTEXT] Setting Variables &
    #[ON LOAD] Safeguard against user ommission 
    if "wpn_dice_ability" not in request.POST:
        request.session["wpn_dice_ability"] = "None"
    else:
        request.session["wpn_dice_ability"] = request.POST["wpn_dice_ability"]


    if "wpn_df1" not in request.POST:
        wpn_df1_id = 44
    else:
        wpn_df1_id = request.POST["wpn_df1"]

    if "wpn_df2" not in request.POST:
        wpn_df2_id = 44
    else:
        wpn_df2_id = request.POST["wpn_df2"]

    if "wpn_df3" not in request.POST:
        wpn_df3_id = 44
    else:
        wpn_df3_id = request.POST["wpn_df3"]

    if "wpn_df4" not in request.POST:
        wpn_df4_id = 44
    else:
        wpn_df4_id = request.POST["wpn_df4"]

    if "wpn_df5" not in request.POST:
        wpn_df5_id = 44
    else:
        wpn_df5_id = request.POST["wpn_df5"]

    if "wpn_df6" not in request.POST:
        wpn_df6_id = 44
    else:
        wpn_df6_id = request.POST["wpn_df6"]
    
    #[SESSION] SAVING SIDES TO SESSION TO PRINT IN NEW DICE BOX
    request.session["wpn_df1"]=wpn_df1_id
    request.session["wpn_df2"]=wpn_df2_id
    request.session["wpn_df3"]=wpn_df3_id
    request.session["wpn_df4"]=wpn_df4_id
    request.session["wpn_df5"]=wpn_df5_id
    request.session["wpn_df6"]=wpn_df6_id


    #### [CREATE] SET VARIABLES FROM R.POST ####
    wpn_dice_name=request.POST["wpn_dice_name"]
    wpn_dice_element=request.POST["wpn_dice_element"]
    wpn_dice_price=int(request.POST["wpn_dice_price"])
    #wpn_dice_ability defined above
    #wpn_df1, df2, df3, df4 defined above
    #wpn_df5, df6 are always 0

    #### [CREATE] ####
    df1=DiceFace.objects.get(id=wpn_df1_id)
    df2=DiceFace.objects.get(id=wpn_df2_id)
    df3=DiceFace.objects.get(id=wpn_df3_id)
    df4=DiceFace.objects.get(id=wpn_df4_id)
    df5=DiceFace.objects.get(id=wpn_df5_id)
    df6=DiceFace.objects.get(id=wpn_df6_id)

    WpnDice.objects.create(name=wpn_dice_name, forAtk="Attack", element=wpn_dice_element, price=wpn_dice_price, dface1=df1, dface2=df2, dface3=df3, dface4=df4, dface5=df5, dface6=df6)
    

    #### [SESSION] SAVE NEWEST (LAST) DICEFACE STATS ####
    request.session["wpn_dice_name"]=WpnDice.objects.last().name
    request.session["wpn_dice_id"]=WpnDice.objects.last().id
    request.session["wpn_dice_element"]=WpnDice.objects.last().element
    request.session["wpn_dice_price"]=WpnDice.objects.last().price

    return redirect("/god_dice")


####################################
#####      Armor Dice God      #####
####################################
def god_armor_dice(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    #[LOAD] to load error free without request.POST/session
    if "armor_dice_ability" not in request.POST:
        armor_dice_ability = "None"
    else:
        armor_dice_ability = request.POST["armor_dice_ability"]

    #[CONTEXT] SET VARIABLES FROM SESSION
    if "armor_dice_name" not in request.session:
        armor_dice_name=" "
    else:
        armor_dice_name=request.session["armor_dice_name"]

    if "armor_dice_id" not in request.session:
        armor_dice_id=" "
    else:
        armor_dice_id=request.session["armor_dice_id"]

    if "armor_dice_element" not in request.session:
        armor_dice_element=" "
    else:
        armor_dice_element=request.session["armor_dice_element"]

    if "armor_dice_price" not in request.session:
        armor_dice_price=" "
    else:
        armor_dice_price=request.session["armor_dice_price"]

    #[CONTEXT] DICE SIDE VARs FROM SESSION (saved in /process_god_armor_dice)
    # if it does not exist, set value to DiceFace ID#44 (Basic 0)
    if "armor_df1" not in request.session:
        armor_df1 = 51
    else:
        armor_df1 = request.session["armor_df1"]

    if "armor_df2" not in request.session:
        armor_df2 = 52
    else:
        armor_df2 = request.session["armor_df2"]

    if "armor_df3" not in request.session:
        armor_df3 = 53
    else:
        armor_df3 = request.session["armor_df3"]
    
    #Armor dice should only have 3 side available to modify
    if "armor_df4" not in request.session:
        armor_df4 = 54
    else:
        armor_df4 = request.session["armor_df4"]
    if "armor_df5" not in request.session:
            armor_df5 = 54
    else:
        armor_df5 = request.session["armor_df5"]
    if "armor_df6" not in request.session:
            armor_df6 = 54
    else:
        armor_df6 = request.session["armor_df6"]

    context = {
        "all_armor_dice": ArmrDice.objects.all(),
        "armor_dice_name": armor_dice_name,
        "armor_dice_id": armor_dice_id,
        "armor_dice_element": armor_dice_element,
        "armor_dice_price": armor_dice_price,
        "armor_dice_ability": armor_dice_ability,
        "armor_df1": armor_df1,
        "armor_df2": armor_df2,
        "armor_df3": armor_df3,
        "armor_df4": armor_df4,
        "armor_df5": armor_df5,
        "armor_df6": armor_df6,
        "armor_df1_name": DiceFace.objects.get(id=armor_df1).name,
        "armor_df2_name": DiceFace.objects.get(id=armor_df2).name,
        "armor_df3_name": DiceFace.objects.get(id=armor_df3).name,
        "armor_df4_name": DiceFace.objects.get(id=armor_df4).name,
        "armor_df5_name": DiceFace.objects.get(id=armor_df5).name,
        "armor_df6_name": DiceFace.objects.get(id=armor_df6).name,
    
    }

    return render(request, "god_armor_dice.html", context)

def del_armor_dice(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    dice_to_delete=request.POST["delete"]
    ArmrDice.objects.get(id=dice_to_delete).delete()

    return redirect("/god_armor_dice")

def edit_armor_dice(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    if "edit_name" in request.POST:
        d_to_edit=request.POST["edit_name"]
        new_name=request.POST["new_name"]
        name_to_edit=ArmrDice.objects.get(id=d_to_edit)
        name_to_edit.name=new_name
        name_to_edit.save()

    if "edit_price" in request.POST:
        d_to_edit=request.POST["edit_price"]
        new_price=request.POST["new_price"]
        price_to_edit=ArmrDice.objects.get(id=d_to_edit)
        price_to_edit.price=new_price
        price_to_edit.save()

    if "edit_element" in request.POST:
        d_to_edit=request.POST["edit_element"]
        new_element=request.POST["new_element"]
        element_to_edit=ArmrDice.objects.get(id=d_to_edit)
        element_to_edit.element=new_element
        element_to_edit.save()

    if "edit_df1" in request.POST:
        d_to_edit=request.POST["edit_df1"]
        new_df1=request.POST["new_df1_id"]
        df1_to_edit=ArmrDice.objects.get(id=d_to_edit)
        df1_to_edit.dface1=DiceFace.objects.get(id=new_df1)
        df1_to_edit.save()

    if "edit_df2" in request.POST:
        d_to_edit=request.POST["edit_df2"]
        new_df2=request.POST["new_df2_id"]
        df2_to_edit=ArmrDice.objects.get(id=d_to_edit)
        df2_to_edit.dface2=DiceFace.objects.get(id=new_df2)
        df2_to_edit.save()

    if "edit_df3" in request.POST:
        d_to_edit=request.POST["edit_df3"]
        new_df3=request.POST["new_df3_id"]
        df3_to_edit=ArmrDice.objects.get(id=d_to_edit)
        df3_to_edit.dface3=DiceFace.objects.get(id=new_df3)
        df3_to_edit.save()
    
    if "edit_df4" in request.POST:
        d_to_edit=request.POST["edit_df4"]
        new_df4=request.POST["new_df4_id"]
        df4_to_edit=ArmrDice.objects.get(id=d_to_edit)
        df4_to_edit.dface4=DiceFace.objects.get(id=new_df4)
        df4_to_edit.save()

    if "edit_df5" in request.POST:
        d_to_edit=request.POST["edit_df5"]
        new_df5=request.POST["new_df5_id"]
        df5_to_edit=ArmrDice.objects.get(id=d_to_edit)
        df5_to_edit.dface5=DiceFace.objects.get(id=new_df5)
        df5_to_edit.save()

    if "edit_df6" in request.POST:
        d_to_edit=request.POST["edit_df6"]
        new_df6=request.POST["new_df6_id"]
        df6_to_edit=ArmrDice.objects.get(id=d_to_edit)
        df6_to_edit.dface6=DiceFace.objects.get(id=new_df6)
        df6_to_edit.save()
    
    if "edit_ability" in request.POST:
        d_to_edit=request.POST["edit_ability"]
        new_ability=request.POST["new_ability"]
        ability_to_edit=ArmrDice.objects.get(id=d_to_edit)
        ability_to_edit.ability=new_ability
        ability_to_edit.save()

    return redirect("/god_armor_dice")

def process_god_armor_dice(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    #[CONTEXT] Setting Variables &
    #[ON LOAD] Safeguard against user ommission 
    if "armor_dice_ability" not in request.POST:
        request.session["armor_dice_ability"] = "None"
    else:
        request.session["armor_dice_ability"] = request.POST["armor_dice_ability"]

    if "armor_df1" not in request.POST:
        armor_df1_id = 51
    else:
        armor_df1_id = request.POST["armor_df1"]

    if "armor_df2" not in request.POST:
        armor_df2_id = 52
    else:
        armor_df2_id = request.POST["armor_df2"]

    if "armor_df3" not in request.POST:
        armor_df3_id = 53
    else:
        armor_df3_id = request.POST["armor_df3"]

    # Armor dice should only have 3 available faces to upgrade
    # if "armor_df4" not in request.POST:
    #     armor_df4_id = 44
    # else:
    #     wpn_df4_id = request.POST["armor_df4"]
    
    #[SESSION] SAVING SIDES TO SESSION
    request.session["armor_df1"]=armor_df1_id
    request.session["armor_df2"]=armor_df2_id
    request.session["armor_df3"]=armor_df3_id
    request.session["armor_df4"]=armor_df4_id
    request.session["armor_df5"]=armor_df5_id
    request.session["armor_df6"]=armor_df6_id


    #### [CREATE] SET VARIABLES TO R.POST ####
    armor_dice_name=request.POST["armor_dice_name"]
    armor_dice_element=request.POST["armor_dice_element"]
    armor_dice_price=int(request.POST["armor_dice_price"])
    #armor_dice_ability defined above
    #armor_df1, df2, df3, df4 defined above
    #armor_df5, df6 are always 0

    #### [CREATE] ####
    df1=DiceFace.objects.get(id=armor_df1_id)
    df2=DiceFace.objects.get(id=armor_df2_id)
    df3=DiceFace.objects.get(id=armor_df3_id)
    df4=DiceFace.objects.get(id=armor_df4_id)
    df5=DiceFace.objects.get(id=armor_df5_id)
    df6=DiceFace.objects.get(id=armor_df6_id)

    ArmrDice.objects.create(name=armor_dice_name, forAtk="Defense", element=armor_dice_element, price=armor_dice_price, dface1=df1, dface2=df2, dface3=df3, dface4=df4, dface5=df5, dface6=df6)
    

    #### [SESSION] SAVE NEWEST (LAST) DICEFACE STATS ####
    request.session["armor_dice_name"]=ArmrDice.objects.last().name
    request.session["armor_dice_id"]=ArmrDice.objects.last().id
    request.session["armor_dice_element"]=ArmrDice.objects.last().element
    request.session["armor_dice_price"]=ArmrDice.objects.last().price
    
    return redirect ("/god_armor_dice")

####################################
#####        Weapon God        #####
####################################
def god_weapon(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    #No abilities as of 2020-01-23
    if "weapon_ability" not in request.POST:
        weapon_ability = "None"
    else:
        weapon_ability = request.POST["weapon_ability"]

    #[CONTEXT] SET VARIABLES FROM SESSION
    if "weapon_name" not in request.session:
        weapon_name=" "
    else:
        weapon_name=request.session["weapon_name"]

    if "weapon_id" not in request.session:
        weapon_id=" "
    else:
        weapon_id=request.session["weapon_id"]

    if "weapon_element" not in request.session:
        weapon_element=" "
    else:
        weapon_element=request.session["weapon_element"]

    if "weapon_price" not in request.session:
        weapon_price=" "
    else:
        weapon_price=request.session["weapon_price"]

    #[CONTEXT] DICE SIDE VARs FROM SESSION (saved in /process_god_weapon)
    # if it does not exist, set value to DiceFace ID#44 (Basic 0)
    if "wpn_dslot1" not in request.session:
        wpn_dslot1 = 22
    else:
        wpn_dslot1 = request.session["wpn_dslot1"]

    if "wpn_dslot2" not in request.session:
        wpn_dslot2 = 22
    else:
        wpn_dslot2 = request.session["wpn_dslot2"]

    if "wpn_dslot3" not in request.session:
        wpn_dslot3 = 22
    else:
        wpn_dslot3 = request.session["wpn_dslot3"]
    
    if "wpn_dslot4" not in request.session:
        wpn_dslot4 = 22
    else:
        wpn_dslot4 = request.session["wpn_dslot4"]

    if "wpn_dslot5" not in request.session:
        wpn_dslot5 = 22
    else:
        wpn_dslot5 = request.session["wpn_dslot5"]

    if "wpn_dslot6" not in request.session:
        wpn_dslot6 = 22
    else:
        wpn_dslot6 = request.session["wpn_dslot6"]

    context = {
        "all_weapons": Weapon.objects.all(),
        "new_weapon": Weapon.objects.last(),
        "weapon_name": weapon_name,
        "weapon_id": weapon_id,
        "weapon_element": weapon_element,
        "weapon_price": weapon_price,
        "weapon_ability": weapon_ability,
        "wpn_dslot1": wpn_dslot1,
        "wpn_dslot2": wpn_dslot2,
        "wpn_dslot3": wpn_dslot3,
        "wpn_dslot4": wpn_dslot4,
        "wpn_dslot5": wpn_dslot5,
        "wpn_dslot6": wpn_dslot6,
        "armor_df1_name": DiceFace.objects.get(id=armor_df1).name,
        "armor_df2_name": DiceFace.objects.get(id=armor_df2).name,
        "armor_df3_name": DiceFace.objects.get(id=armor_df3).name,
        "armor_df4_name": DiceFace.objects.get(id=armor_df4).name,
        "armor_df5_name": DiceFace.objects.get(id=armor_df5).name,
        "armor_df6_name": DiceFace.objects.get(id=armor_df6).name,
    }
    
    return render(request, "god_weapon.html", context)

def process_god_weapon(request):
    pass

def edit_weapon(request):
    pass

def del_weapon(request):
    pass

####################################
#####       Armor God          #####
####################################
def god_armor(request):
    pass

def process_god_armor(request):
    pass

####################################
#####        Item God          #####
####################################
def god_item(request):
    pass

def process_god_item(request):
    pass

####################################
#####        Dice Shop         #####
####################################
def equipment_shop(request):
    hero_id=request.session["hero_id"]
    hero=Hero.objects.get(id=hero_id)

    context = {
        "hero": hero,
    }

    return render(request, "shop.html", context)

def process_equipment_shop(request):
    pass

def dice_shop(request):
    pass

def process_dice_shop(request):
    pass

def levelup(request):
    pass

def process_levelup(request):
    pass



####################################
####           Reset            #### 
####################################
def dice_reset(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    #####  Restart Fight  #####
    if request.POST["reset"]=="reset":
        del request.session["enemy_life"]
        del request.session["hero_life"]

        del request.session["enemy_roll"]
        del request.session["hero_roll"]

        del request.session["enemy_attack"]
        del request.session["hero_attack"]

        del request.session["enemy_log"]
        del request.session["hero_log"]
        return redirect("/dice_hero")

    ##### Logout #####
    if request.POST["reset"]=="logout": #change all instances of "new-log_in " to logout
        if "session" in request:
            request.session.clear()

        return redirect("/user_login")



####################################
####           End              #### 
####################################


# [continue later]
# ####################################
# #####     Accessory God        #####
# ####################################
# def god_accessory(request):
#     pass

# def process_god_accessory(request):
#     pass