from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
import bcrypt

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

    hero_id=request.session["hero_id"]
    hero_name=Hero.objects.get(id=hero_id).name
    userid=request.session["userid"]
    username=request.session["username"]

    context = {
    ### fix HTML template
        "hero_id": hero_id,
        "hero_name": hero_name,
        "userid": userid,
        "username": username,
        "new_hero": Hero.objects.last(),
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

    userid=request.session["userid"]
    username=request.session["username"]

    context = {
        "userid": userid,
        "username": username,
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

        #dice_index
        # "die_index": ???,

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
        request.session[i+1]=i+1
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

    # hero=Hero.objects.get(id=request.session["userid"])
    # wpn1=hero.weapons.first()
    # wpn2=hero.weapons.last()
    # wpn1_dice=wpn1.wpn_dice.all()
    # wpn2_dice=wpn2.wpn_dice.all()

# run a for loop depending on number of dice slots/rolls
# NOT for the number of sides on a die
    if request.POST["hero_weapon"]=="w1":
        # hero_dice=Hero.objects.get(id=request.session["userid"]).weapons.first.first.roll_value
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
        request.session[i+1]=i+1

    request.session["hero_log"].insert(0, "Hero attacks for "+str(request.session["hero_attack"])+ "!")
    print(request.session["hero_roll"])
    print(request.session["hero_attack"])
    request.session.save()
    return redirect("/dice_hero")


####################################
#####       HERO MANAGER       #####
####################################

def inspect_hero(request):
    hero_id=request.session["hero_id"]
    hero=Hero.objects.get(id=hero_id)
    hero_name=Hero.objects.get(id=hero_id).name
    userid=request.session["userid"]
    username=request.session["username"]
    hero_weapons = Hero.objects.get(id=hero_id).weapons.all()
    hero_armors = Hero.objects.get(id=hero_id).armors.all()

    context = {
        "hero_id": hero_id,
        "hero_name": hero_name,
        "userid": userid,
        "username": username,
        "hero": hero,
        "hero_weapons": hero_weapons,
        "hero_armors": hero_armors,
    }
    
    return render(request, "inspect_hero.html", context)

def process_inspect_hero(request):
    pass

def inventory(request):
    pass

def process_inventory(request):
    pass


####################################
#####      God of Heroes       #####
####################################
def god_hero(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    if "new_hero_id" in request.session:
        new_hero=Hero.objects.get(id=request.session["new_hero_id"])
    else:
        new_hero=Hero.objects.last()


    userid=request.session["userid"]
    username=request.session["username"]

    context = {
        "userid": userid,
        "username": username,
        "all_heroes": Hero.objects.all(),
        "hero_name": new_hero.name,
        "hero_id": new_hero.id,
        "hero_hp": new_hero.hp_base,
        "hero_atk": new_hero.atk_base,
        "hero_def": new_hero.def_base,
        "hero_int": new_hero.int_base,
        "hero_spd": new_hero.spd_base,
        "hero_gold": new_hero.gold,
        "hero_gems": new_hero.gems,
    }

    return render(request, "god_hero.html", context)


def process_god_hero(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    hero_name=request.POST["hero_name"]
    hero_hp=request.POST["hero_hp"]
    hero_atk=request.POST["hero_atk"]
    hero_def=request.POST["hero_def"]
    hero_int=request.POST["hero_int"]
    hero_spd=request.POST["hero_spd"]
    hero_gold=request.POST["hero_gold"]
    hero_gems=request.POST["hero_gems"]


    Hero.objects.create(name=hero_name, hp_base=hero_hp, atk_base=hero_atk, def_base=hero_def, int_base=hero_int, spd_base=hero_spd, gold=hero_gold, gems=hero_gems)

    request.session["new_hero_id"]=Hero.objects.last().id

    return redirect("/god_hero")

def edit_hero(request):
    if "edit_name" in request.POST:
        hero_to_edit=request.POST["edit_name"]
        new_name=request.POST["new_name"]
        name_to_edit=Hero.objects.get(id=hero_to_edit)
        name_to_edit.name=new_name
        name_to_edit.save()
    
    if "edit_user" in request.POST:
        hero_to_edit=request.POST["edit_user"]
        new_userid=request.POST["new_user"]
        new_user=User.objects.get(id=new_userid)
        name_to_edit=Hero.objects.get(id=hero_to_edit)
        name_to_edit.user=new_user
        name_to_edit.save()
    
    if "edit_level" in request.POST:
        hero_id=request.POST["edit_level"]
        new_level=request.POST["new_level"]
        hero=Hero.objects.get(id=hero_id)
        hero.level=new_level
        hero.save()

    if "edit_hp" in request.POST:
        hero_to_edit=request.POST["edit_hp"]
        new_hp=request.POST["new_hp"]
        hp_to_edit=Hero.objects.get(id=hero_to_edit)
        hp_to_edit.hp_base=new_hp
        hp_to_edit.save()

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
    
    if "edit_gold" in request.POST:
        hero_to_edit=request.POST["edit_gold"]
        new_gold=request.POST["new_gold"]
        gold_to_edit=Hero.objects.get(id=hero_to_edit)
        gold_to_edit.gold=new_gold
        gold_to_edit.save()
    
    if "edit_gems" in request.POST:
        hero_to_edit=request.POST["edit_gems"]
        new_gems=request.POST["new_gems"]
        gems_to_edit=Hero.objects.get(id=hero_to_edit)
        gems_to_edit.gems=new_gems
        gems_to_edit.save()

    return redirect("/god_hero")



def del_hero(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    hero_to_delete=request.POST["delete"]
    Hero.objects.get(id=hero_to_delete).delete()

    return redirect("/god_hero")


####################################
#####      God of Enemies       #####
####################################
def god_enemy(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    if "new_enemy_id" in request.session:
        new_enemy=Enemy.objects.get(id=request.session["new_enemy_id"])
    # else:
    #     new_enemy=


    userid=request.session["userid"]
    username=request.session["username"]

    context = {
        "userid": userid,
        "username": username,
        "all_enemies": Enemy.objects.all(),
        # "enemy_name": new_enemy.name,
        # "enemy_id": new_enemy.id,
        # "enemy_hp": new_enemy.hp_base,
        # "enemy_atk": new_enemy.atk_base,
        # "enemy_def": new_enemy.def_base,
        # "enemy_int": new_enemy.int_base,
        # "enemy_spd": new_enemy.spd_base,
        # "enemy_gold": new_enemy.gold,
        # "enemy_gems": new_enemy.gems,
        # "enemy_items": new_enemy.items,
    }

    return render(request, "god_enemies.html", context)


def process_god_enemy(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    enemy_name=request.POST["enemy_name"]
    enemy_hp=request.POST["enemy_hp"]
    enemy_atk=request.POST["enemy_atk"]
    enemy_def=request.POST["enemy_def"]
    enemy_int=request.POST["enemy_int"]
    enemy_spd=request.POST["enemy_spd"]
    enemy_gold=request.POST["enemy_gold"]
    enemy_gems=request.POST["enemy_gems"]
    # enemy_items=request.POST["enemy_items"]


    Enemy.objects.create(name=enemy_name, hp_base=enemy_hp, atk_base=enemy_atk, def_base=enemy_def, int_base=enemy_int, spd_base=enemy_spd, gold=enemy_gold, gems=enemy_gems)

    request.session["new_enemy_id"]=Enemy.objects.last().id

    return redirect("/god_enemy")

def edit_enemy(request):
    if "edit_name" in request.POST:
        enemyid=request.POST["edit_name"]
        new_name=request.POST["new_name"]
        name_to_edit=Enemy.objects.get(id=enemyid)
        name_to_edit.name=new_name
        name_to_edit.save()
    
    if "edit_level" in request.POST:
        enemyid=request.POST["edit_level"]
        new_level=request.POST["new_level"]
        enemy=Enemy.objects.get(id=enemyid)
        enemy.level=new_level
        enemy.save()

    if "edit_hp" in request.POST:
        enemyid=request.POST["edit_hp"]
        new_hp=request.POST["new_hp"]
        enemy=Enemy.objects.get(id=enemyid)
        enemy.hp_base=new_hp
        enemy.save()

    if "edit_atk" in request.POST:
        enemyid=request.POST["edit_atk"]
        new_atk=request.POST["new_atk"]
        enemy=Enemy.objects.get(id=enemyid)
        enemy.atk_base=new_atk
        enemy.save()

    if "edit_def" in request.POST:
        enemyid=request.POST["edit_def"]
        new_def=request.POST["new_def"]
        enemy=Enemy.objects.get(id=enemyid)
        enemy.def_base=new_def
        enemy.save()

    if "edit_int" in request.POST:
        enemyid=request.POST["edit_int"]
        new_int=request.POST["new_int"]
        enemy=Enemy.objects.get(id=enemyid)
        enemy.int_base=new_int
        enemy.save()

    if "edit_spd" in request.POST:
        enemyid=request.POST["edit_spd"]
        new_spd=request.POST["new_spd"]
        enemy=Enemy.objects.get(id=enemyid)
        enemy.spd_base=new_spd
        enemy.save()
    
    if "edit_gold" in request.POST:
        enemyid=request.POST["edit_gold"]
        new_gold=request.POST["new_gold"]
        enemy=Enemy.objects.get(id=enemyid)
        enemy.gold=new_gold
        enemy.save()
    
    if "edit_gems" in request.POST:
        enemyid=request.POST["edit_gems"]
        new_gems=request.POST["new_gems"]
        enemy=Enemy.objects.get(id=enemyid)
        enemy.gems=new_gems
        enemy.save()
    
    # if "edit_items" in request.POST:
    #     enemyid=request.POST["edit_items"]
    #     new_items=request.POST["new_items"]
    #     enemy=Enemy.objects.get(id=enemyid)
    #     enemy.items=new_items
    #     enemy.save()


    return redirect("/god_enemy")



def del_enemy(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    enemyid=request.POST["delete"]
    Enemy.objects.get(id=enemyid).delete()

    return redirect("/god_enemy")


####################################
#####    God of DiceFaces      #####
####################################
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

def basic_wpndfaces(request):
    WpnDface.objects.create(name="ATK 1", roll_value="1", price="50")
    WpnDface.objects.create(name="ATK 2", roll_value="2", price="150")
    WpnDface.objects.create(name="ATK 3", roll_value="3", price="450")
    WpnDface.objects.create(name="ATK 4", roll_value="4", price="1350")
    WpnDface.objects.create(name="ATK 5", roll_value="5", price="4050")
    WpnDface.objects.create(name="ATK 6", roll_value="6", price="12150")
    WpnDface.objects.create(name="ATK 0", roll_value="0", price="0")
    request.session["df_type"]="WpnDface"
    return redirect("/god_diceface")

def basic_armordfaces(request):
    ArmorDface.objects.create(name="DEF 1", roll_value="1", price="100")
    ArmorDface.objects.create(name="DEF 2", roll_value="2", price="300")
    ArmorDface.objects.create(name="DEF 3", roll_value="3", price="900")
    ArmorDface.objects.create(name="DEF 4", roll_value="4", price="2700")
    ArmorDface.objects.create(name="DEF 5", roll_value="5", price="8100")
    ArmorDface.objects.create(name="DEF 6", roll_value="6", price="24300")
    ArmorDface.objects.create(name="DEF 0", roll_value="0", price="0")
    request.session["df_type"]="ArmorDface"
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

    #[top] to load errorfree without request.POST/session
    if "dice_ability" not in request.POST:
        request.session["dice_ability"] = "None"
    else:
        request.session["dice_ability"] = request.POST["dice_ability"]

    # if "dice_critical" not in request.POST:
    #     request.session["dice_critical"] = "False"
    # else:
    #     request.session["dice_critical"] = request.POST["dice_critical"]

    if "dice_id" not in request.session:
        dice_id=" "
    else:
        dice_id=request.session["dice_id"]

    if "dice_name" not in request.session:
        request.session["dice_name"]=" "
    if "dice_type" not in request.session:
        request.session["dice_type"]=" "
    # if "dice_element" not in request.session:
    #     request.session["dice_element"]=" "
    if "dice_price" not in request.session:
        request.session["dice_price"]=" "


    #[end] to load errorfree without request.POST/session

    
    dice_name=request.session["dice_name"]
    dice_type=request.session["dice_type"]
    dice_price=request.session["dice_price"]
    dice_ability=request.session["dice_ability"]

    #DYNAMIC DATABASE
    dice_db=" "
    db_title="No Database Chosen"
    new_dice_type=" "

    if "dice_type" in request.session:
        if request.session["dice_type"]=="WpnDice":
            dice_db=WpnDice.objects.all()
            db_title="Weapon Dice"
            new_dice_type="Weapon Dice"
        if request.session["dice_type"]=="ArmorDice":
            dice_db=ArmorDice.objects.all()
            db_title="Armor Dice Faces"
            new_dice_type="Armor Dice"
    if "dice_type" in request.POST:
        request.session["dice_type"]=request.POST["dice_type"]
        if request.POST["dice_type"]=="WpnDice":
            dice_db=WpnDice.objects.all()
            db_title="Weapon Dice"
        if request.POST["dice_type"]=="ArmorDice":
            dice_db=ArmorDice.objects.all()
            db_title="Armor Dice"

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
        "dice_db": dice_db,
        "db_title": db_title,
        "id": dice_id,
        "type": new_dice_type,
        "name": dice_name,
        "price": dice_price,
        "dice_ability": dice_ability,
        "error_msg": error_msg,
        "msg_color": msg_color,
    }

    return render(request, "god_dice.html", context)

def process_god_dice(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    if "dice_type" not in request.POST:
        request.session["error_msg"] = "Please select a Dice Face type"
        return redirect("/god_dice")


    #[SESSION] from post data
    request.session["dice_name"]=request.POST["dice_name"]
    request.session["dice_type"]=request.POST["dice_type"]
    request.session["dice_price"]=request.POST["dice_price"]

    if "dice_ability" not in request.POST:
        request.session["dice_ability"] = "None"
    else:
        request.session["dice_ability"] = request.POST["dice_ability"]    


    #[VARIABLES] from session
    dice_name=request.session["dice_name"]
    # heroid=Hero.objects.get(id=request.session["hero_id"])
    dice_price=int(request.session["dice_price"])
    dice_ability = request.session["dice_ability"]

    #[CREATE] WpnDice
    if request.POST["dice_type"] == "WpnDice":
        request.session["dice_type"] = request.POST["dice_type"]
        WpnDice.objects.create(name=dice_name, price=dice_price)
        request.session["dice_id"]=WpnDice.objects.last().id
        request.session["dice_name"]=WpnDice.objects.last().name
        request.session["dice_price"]=WpnDice.objects.last().price
        # request.session["df_ability"]=WpnDface.objects.last().ability

    #[CREATE] ArmorDice
    if request.POST["dice_type"] == "ArmorDice":
        request.session["dice_type"] = request.POST["dice_type"]
        ArmorDice.objects.create(name=dice_name, price=dice_price)
        request.session["dice_id"]=ArmorDice.objects.last().id 
        request.session["dice_name"]=ArmorDice.objects.last().name
        request.session["dice_price"]=ArmorDice.objects.last().price
        # request.session["df_ability"]=ArmorDface.objects.last().ability

    return redirect("/god_dice")

def basic_wpndice(request):
    WpnDice.objects.create(name="WpnDie 1", price="1000")
    WpnDice.objects.create(name="WpnDie 2", price="1000")
    WpnDice.objects.create(name="WpnDie 3", price="1000")
    WpnDice.objects.create(name="WpnDie 4", price="1000")
    WpnDice.objects.create(name="WpnDie 5", price="1000")
    WpnDice.objects.create(name="WpnDie 6", price="1000")
    request.session["dice_type"]="WpnDice"
    return redirect("/god_dice")

def basic_armordice(request):
    ArmorDice.objects.create(name="ArmorDie 1", price="2000")
    ArmorDice.objects.create(name="ArmorDie 2", price="2000")
    ArmorDice.objects.create(name="ArmorDie 3", price="2000")
    ArmorDice.objects.create(name="ArmorDie 4", price="2000")
    ArmorDice.objects.create(name="ArmorDie 5", price="2000")
    ArmorDice.objects.create(name="ArmorDie 6", price="2000")
    request.session["dice_type"]="ArmorDice"
    return redirect("/god_dice")

def edit_dice(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))
    
    if request.session["dice_type"] == "WpnDice":
        Dice=WpnDice
    if request.session["dice_type"] == "ArmorDice":
        Dice=ArmorDice


    if "edit_owner" in request.POST:
        dice_to_edit=request.POST["edit_owner"]
        new_hero_id=request.POST["new_owner"]
        name_to_edit=Dice.objects.get(id=dice_to_edit)
        name_to_edit.owner_id=new_hero_id
        name_to_edit.save()

    if "edit_parent" in request.POST:
        dice_to_edit=request.POST["edit_parent"]
        new_parent_id=request.POST["new_parent"]
        name_to_edit=Dice.objects.get(id=dice_to_edit)
        name_to_edit.parent_id=new_parent_id
        name_to_edit.save()

    if "edit_name" in request.POST:
        dice_to_edit=request.POST["edit_name"]
        new_name=request.POST["new_name"]
        name_to_edit=Dice.objects.get(id=dice_to_edit)
        name_to_edit.name=new_name
        name_to_edit.save()

    if "edit_price" in request.POST:
        dice_to_edit=request.POST["edit_price"]
        new_price=request.POST["new_price"]
        price_to_edit=Dice.objects.get(id=dice_to_edit)
        price_to_edit.price=new_price
        price_to_edit.save()
    
    if "edit_ability" in request.POST:
        dice_to_edit=request.POST["edit_ability"]
        new_ability=request.POST["new_ability"]
        ability_to_edit=Dice.objects.get(id=dice_to_edit)
        ability_to_edit.ability=new_ability
        ability_to_edit.save()

    return redirect("/god_dice")


def del_dice(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    dice_to_delete=request.POST["delete"]

    if request.session["dice_type"] == "WpnDice":
        WpnDice.objects.get(id=dice_to_delete).delete()
    if request.session["dice_type"] == "ArmorDice":
        ArmorDice.objects.get(id=dice_to_delete).delete()

    return redirect("/god_dice")


####################################
#####      Equipment God       #####
####################################
def god_equip(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    #[top] to load errorfree without request.POST/session
    if "equip_ability" not in request.POST:
        request.session["equip_ability"] = "None"
    else:
        request.session["equip_ability"] = request.POST["equip_ability"]

    if "equip_id" not in request.session:
        equip_id=" "
    else:
        equip_id=request.session["equip_id"]

    if "equip_name" not in request.session:
        request.session["equip_name"]=" "
    if "equip_type" not in request.session:
        request.session["equip_type"]=" "
    if "hp_boost" not in request.session:
        request.session["hp_boost"]=" "
    if "atk_boost" not in request.session:
        request.session["atk_boost"]=" "
    if "def_boost" not in request.session:
        request.session["def_boost"]=" "
    if "int_boost" not in request.session:
        request.session["int_boost"]=" "
    if "spd_boost" not in request.session:
        request.session["spd_boost"]=" "
    if "equip_ability" not in request.session:
        request.session["equip_ability"]=" "
    if "equip_element" not in request.session:
        request.session["equip_element"]=" "
    if "equip_price" not in request.session:
        request.session["equip_price"]=" "
    #[end] to load errorfree without request.POST/session

    
    equip_name = request.session["equip_name"]
    equip_type = request.session["equip_type"]
    hp_boost = request.session["hp_boost"]
    atk_boost = request.session["atk_boost"]
    def_boost = request.session["def_boost"]
    int_boost = request.session["int_boost"]
    def_boost = request.session["def_boost"]
    equip_ability = request.session["equip_ability"]
    equip_element = request.session["equip_element"]
    equip_price = request.session["equip_price"]


    #DYNAMIC DATABASE
    equip_db=" "
    db_title="No Database Chosen"
    new_equip_type=" "

    if "equip_type" in request.session:
        if request.session["equip_type"]=="Weapon":
            equip_db=Weapon.objects.all()
            db_title="Weapons"
            new_equip_type="Weapons"
        if request.session["equip_type"]=="Armor":
            equip_db=Armor.objects.all()
            db_title="Armor"
            new_equip_type="Armor"
    if "equip_type" in request.POST:
        request.session["equip_type"]=request.POST["equip_type"]
        if request.POST["equip_type"]=="Weapon":
            equip_db=Weapon.objects.all()
            db_title="Weapon"
        if request.POST["equip_type"]=="Armor":
            equip_db=Armor.objects.all()
            db_title="Armor"

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
        "equip_db": equip_db,
        "db_title": db_title,
        "id": equip_id,
        "type": new_equip_type,
        "name": equip_name,
        "hp": hp_boost,
        "atk": atk_boost,
        "def": def_boost,
        "int": int_boost,
        "def": def_boost,
        "price": equip_price,
        "dice_ability": equip_ability,
        "error_msg": error_msg,
        "msg_color": msg_color,
    }

    
    return render(request, "god_equip.html", context)

def process_god_equip(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    if "equip_type" not in request.POST:
        request.session["error_msg"] = "Please select a Equipment type"
        return redirect("/god_equip")


    #[SESSION] from post data
    request.session["equip_name"]=request.POST["equip_name"]
    request.session["equip_type"]=request.POST["equip_type"]

    request.session["hp_boost"]=request.POST["hp_boost"]
    request.session["atk_boost"]=request.POST["atk_boost"]
    request.session["def_boost"]=request.POST["def_boost"]
    request.session["int_boost"]=request.POST["int_boost"]
    request.session["spd_boost"]=request.POST["spd_boost"]
    request.session["slots"]=request.POST["slots"]
    request.session["equip_ability"]=request.POST["equip_ability"]
    request.session["equip_element"]=request.POST["equip_element"]
    request.session["equip_price"]=request.POST["equip_price"]


    #[VARIABLES] from session
    equip_name=request.session["equip_name"]
    hp_boost=request.session["hp_boost"]
    atk_boost=request.session["atk_boost"]
    def_boost=request.session["def_boost"]
    int_boost=request.session["int_boost"]
    spd_boost=request.session["spd_boost"]
    slots=request.session["slots"]
    ability=request.session["equip_ability"]
    element=request.session["equip_element"]
    price=int(request.session["equip_price"])

    #[CREATE] Weapon
    if request.POST["equip_type"] == "Weapon":
        request.session["equip_type"] = request.POST["equip_type"]
        Weapon.objects.create(name=equip_name, hp_boost=hp_boost, atk_boost=atk_boost, def_boost=def_boost, int_boost=int_boost, spd_boost=spd_boost, slots=slots, price=price)
        request.session["equip_id"]=Weapon.objects.last().id
        # request.session["equip_name"]=Weapon.objects.last().name
        # request.session["equip_price"]=Weapon.objects.last().price
        # request.session["df_ability"]=WpnDface.objects.last().ability

    #[CREATE] Armor
    if request.POST["equip_type"] == "Armor":
        request.session["equip_type"] = request.POST["equip_type"]
        Armor.objects.create(name=equip_name, hp_boost=hp_boost, atk_boost=atk_boost, def_boost=def_boost, int_boost=int_boost, spd_boost=spd_boost, slots=slots, price=price)
        request.session["equip_id"]=Armor.objects.last().id
        # request.session["equip_name"]=Armor.objects.last().name
        # request.session["equip_price"]=Armor.objects.last().price
        # request.session["df_ability"]=ArmorDface.objects.last().ability

    return redirect("/god_equip")

def edit_equip(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))
    
    if request.session["equip_type"] == "Weapon":
        Equipment=Weapon
    if request.session["equip_type"] == "Armor":
        Equipment=Armor

    if "edit_owner" in request.POST:
        equipid=request.POST["edit_owner"]
        new_ownerid=request.POST["new_owner"]
        new_owner=Hero.objects.get(id=request.session["userid"])
        equip=Equipment.objects.get(id=equipid)
        new_owner.add_owner(equip)
        new_owner.save()

    if "edit_name" in request.POST:
        equip_to_edit=request.POST["edit_name"]
        new_name=request.POST["new_name"]
        name_to_edit=Equipment.objects.get(id=equip_to_edit)
        name_to_edit.name=new_name
        name_to_edit.save()

    if "edit_price" in request.POST:
        equip_to_edit=request.POST["edit_price"]
        new_price=request.POST["new_price"]
        price_to_edit=Equipment.objects.get(id=equip_to_edit)
        price_to_edit.price=new_price
        price_to_edit.save()
    
    if "edit_hp" in request.POST:
        equip_to_edit=request.POST["edit_hp"]
        new_hp=request.POST["new_hp"]
        hp_to_edit=Equipment.objects.get(id=equip_to_edit)
        hp_to_edit.hp_boost=new_hp
        hp_to_edit.save()
    
    if "edit_atk" in request.POST:
        equip_to_edit=request.POST["edit_atk"]
        new_atk=request.POST["new_atk"]
        atk_to_edit=Equipment.objects.get(id=equip_to_edit)
        atk_to_edit.atk_boost=new_atk
        atk_to_edit.save()
    
    if "edit_def" in request.POST:
        equip_to_edit=request.POST["edit_def"]
        new_def=request.POST["new_def"]
        def_to_edit=Equipment.objects.get(id=equip_to_edit)
        def_to_edit.def_boost=new_def
        def_to_edit.save()
    
    if "edit_int" in request.POST:
        equip_to_edit=request.POST["edit_int"]
        new_int=request.POST["new_int"]
        int_to_edit=Equipment.objects.get(id=equip_to_edit)
        int_to_edit.int_boost=new_int
        int_to_edit.save()
    
    if "edit_spd" in request.POST:
        equip_to_edit=request.POST["edit_spd"]
        new_spd=request.POST["new_spd"]
        spd_to_edit=Equipment.objects.get(id=equip_to_edit)
        spd_to_edit.spd_boost=new_spd
        spd_to_edit.save()
    
    if "edit_slots" in request.POST:
        equip_to_edit=request.POST["edit_slots"]
        new_slots=request.POST["new_slots"]
        slots_to_edit=Equipment.objects.get(id=equip_to_edit)
        slots_to_edit.slots=new_slots
        slots_to_edit.save()
    
    if "edit_ability" in request.POST:
        equip_to_edit=request.POST["edit_ability"]
        new_ability=request.POST["new_ability"]
        ability_to_edit=Equipment.objects.get(isd=equip_to_edit)
        ability_to_edit.ability=new_ability
        ability_to_edit.save()
    
    if "edit_element" in request.POST:
        equip_to_edit=request.POST["edit_element"]
        new_element=request.POST["new_element"]
        element_to_edit=Equipment.objects.get(id=equip_to_edit)
        element_to_edit.element=new_element
        element_to_edit.save()

    return redirect("/god_equip")

def del_equip(request):
    print("Post: " + str(request.POST))
    print("Session: " + str(request.session))

    equip_id=request.POST["delete"]

    if request.session["equip_type"] == "Weapon":
        Weapon.objects.get(id=equip_id).delete()
    if request.session["equip_type"] == "Armor":
        Armor.objects.get(id=equip_id).delete()

    return redirect("/god_equip")


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
    hero_name=Hero.objects.get(id=hero_id).name
    userid=request.session["userid"]
    username=request.session["username"]
    hero_weapons = Hero.objects.get(id=hero_id).weapons.all()
    hero_armors = Hero.objects.get(id=hero_id).armors.all()

    context = {
        "hero_id": hero_id,
        "hero_name": hero_name,
        "userid": userid,
        "username": username,
        "hero": hero,
        "hero_weapons": hero_weapons,
        "hero_armors": hero_armors,
    }

    return render(request, "equipment_shop.html", context)

def process_equipment_shop(request):
    pass

def dice_shop(request):
    pass

def process_dice_shop(request):
    pass

def levelup(request):

    hero_id=request.session["hero_id"]
    hero=Hero.objects.get(id=hero_id)
    hero_name=Hero.objects.get(id=hero_id).name
    userid=request.session["userid"]
    username=request.session["username"]
    hero_weapons = Hero.objects.get(id=hero_id).weapons.all()
    hero_armors = Hero.objects.get(id=hero_id).armors.all()

    #determine price
    level=hero.level
    price=10+(2*(level-1))

    #too poor
    if "too_poor" in request.session:
        too_poor = request.session["too_poor"]
    else:
        too_poor = " "

    context = {
        "hero_id": hero_id,
        "hero_name": hero_name,
        "userid": userid,
        "username": username,
        "hero": hero,
        "hero_weapons": hero_weapons,
        "hero_armors": hero_armors,
        "price": price,
        "too_poor": too_poor,
    }

    if "too_poor" in request.session:
        del request.session["too_poor"]

    return render (request, "levelup.html", context)

def process_levelup(request):
    hero=Hero.objects.get(id=request.session["hero_id"])
    price=10+(1*(hero.level-1))

    if price>hero.gems:
        request.session["too_poor"]= "You don't have enough gems to level up"
        return redirect("/levelup")

    if "hp_up" in request.POST:
        hero.hp_base=int(hero.hp_base)+int(request.POST["hp_up"])
        print(int(hero.hp_base)+int(request.POST["hp_up"]))
    if "atk_up" in request.POST:
        hero.atk_base=int(hero.atk_base)+int(request.POST["atk_up"])
    if "def_up" in request.POST:
        hero.def_base=int(hero.def_base)+int(request.POST["def_up"])
    if "int_up" in request.POST:
        hero.int_base=int(hero.int_base)+int(request.POST["int_up"])
    if "spd_up" in request.POST:
        hero.spd_base=int(hero.spd_base)+int(request.POST["spd_up"])
    hero.level=int(hero.level)+1
    hero.gems=int(hero.gems)-price
    hero.save()

    return redirect("/levelup")


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