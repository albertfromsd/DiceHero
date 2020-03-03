from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError
# from django.db.models.signals import m2m_changed
# from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
import re
import bcrypt

def get_model_fields(model):
    return model._meta.fields



####################################
######          User          ######
####################################

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['username']) < 3:
            errors["username"] = "Username should be at least four characters"
        else:
            if User.objects.filter(username=postData['username']).count()>0:
                errors["username_exists"]="This username has already been registered"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address" 
        else:
            if User.objects.filter(email=postData['email']).count()>0:
                errors["email_exists"]="This email has already been registered"
        if postData["password"]!=postData["confirm_pw"]:
            errors["confirm_pw"] = "Password did not match confirmation"
        
        return errors

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    objects = UserManager()
    
    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return '\n'.join([f"----------", f"[ID #{self.id}]", f"[Username: {self.name}]", f"[Email: {self.email}]", "***********"])


####################################
######          Hero          ######
####################################
class Hero(models.Model):
    name = models.CharField(max_length=25)
    level = models.IntegerField(MaxValueValidator(9999), default=1)
    user = models.ForeignKey(User, related_name="heroes", on_delete="models.CASCADE", blank=True, null=True)
    #inventory
    gold = models.IntegerField(MaxValueValidator(9999999), default=500)
    gems = models.IntegerField(MaxValueValidator(999999), default=60)
    #base stats
    hp_base = models.IntegerField(MaxValueValidator(99999), default=100)
    atk_base = models.IntegerField(MaxValueValidator(999), default=0)
    def_base = models.IntegerField(MaxValueValidator(999), default=0)
    int_base = models.IntegerField(MaxValueValidator(999), default=0)
    spd_base = models.IntegerField(MaxValueValidator(999), default=5)
    #equip equipment
    # wpn1 = 
    # wpn2 = 
    # armor = 

    def equip_weapon(self, weapon):
        if self.weapons.count() >= 2:
            raise Exception("Only two weapons allowed per hero")
        self.weapons.add(weapon)

    def equip_armor(self, armor):
        if self.armors.count() >= 1:
            raise Exception("Only 1 armor allowed per hero")
        self.armors.add(armor)

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return '\n'.join([f"----------", f"[ID #{self.id}]", f"[Hero: {self.name}]", f"[Level: {self.level}]", f"[User: {self.user}]", f"[HP: {self.hp_base}]", f"[ATK: {self.atk_base}]", f"[DEF: {self.def_base}]", f"[INT: {self.int_base}]", f"[SPD: {self.spd_base}]", "**********"])

####################################
######         Weapon         ######
####################################
class Weapon(models.Model):
    #info
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(Hero, related_name="weapons", on_delete=models.CASCADE, blank=True, null=True)
    level = models.IntegerField(MaxValueValidator(999), default=1)
    price = models.IntegerField(MaxValueValidator(99999), default=500)
    slots = models.IntegerField(MaxValueValidator(10), default=2)

    #stat boosts
    hp_boost = models.IntegerField(MaxValueValidator(999), default=0)
    atk_boost = models.IntegerField(MaxValueValidator(999), default=0)
    def_boost = models.IntegerField(MaxValueValidator(999), default=0)
    int_boost = models.IntegerField(MaxValueValidator(999), default=0)
    spd_boost = models.IntegerField(MaxValueValidator(999), default=0)

    def add_wpn_dice(self, wpndice):
        if self.wpn_dice.count() >= self.slots:
            raise Exception(f"This weapon only has {self.slots} dice slots")
        self.wpn_dice.add(wpndice)

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return '\n'.join([f"----------", f"[ID #{self.id}][Weapon: {self.name}][Price: {self.price}]", f"[ATK: {self.atk_boost}][DEF: {self.def_boost}][INT: {self.int_boost}][SPD: {self.spd_boost}][# of slots: {self.slots}]", "***********"])


####################################
######     Weapon Dice        ######
####################################
class WpnDice(models.Model):
    #info
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(Hero, related_name="wpn_dice", on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey(Weapon, related_name="wpn_dice", on_delete=models.CASCADE, blank=True, null=True)
    level = models.IntegerField(MaxValueValidator(999), default=1)
    price = models.IntegerField(MaxValueValidator(99999), default=1000)

    def add_wpn_dface(self, wpn_dface):
        if self.wpn_dfaces.count() >= 6:
            raise Exception(f"Cannot have more than 6 faces on a die")
        self.wpn_dfaces.add(wpn_dface)

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return '\n'.join([f"----------", f"[ID #{self.id}][WpnDice: {self.name}][Price: {self.price}][Parent: {self.parent}]", "***********"])


####################################
######       WpnDface         ######
####################################
class WpnDface(models.Model):
    #info
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(Hero, related_name="wpn_dfaces", on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey(WpnDice, related_name="wpn_dfaces", on_delete=models.CASCADE, blank=True, null=True)
    level = models.IntegerField(MaxValueValidator(999), default=1)
    price = models.IntegerField(MaxValueValidator(99999), default=50)

    #battle
    roll_value = models.IntegerField(MaxValueValidator(10), default=0)
    critical = models.CharField(max_length=5, default="False")

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return '\n'.join([f"----------", f"[ID #{self.id}][WpnDface: {self.name}][Price: {self.price}]", f"[Owner: {self.owner}][Parent: {self.parent}]",  f"[Roll Value: {self.roll_value}][Critical: {self.critical}]", "----------"])

####################################
######         Armor          ######
####################################
class Armor(models.Model):
    #info
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(Hero, related_name="armors", on_delete=models.CASCADE, blank=True, null=True)
    level = models.IntegerField(MaxValueValidator(999), default=1)
    price = models.IntegerField(MaxValueValidator(99999), default=1000)
    slots = models.IntegerField(MaxValueValidator(10), default=2)

    #stat boosts
    hp_boost = models.IntegerField(MaxValueValidator(999), default=0)
    atk_boost = models.IntegerField(MaxValueValidator(999), default=0)
    def_boost = models.IntegerField(MaxValueValidator(999), default=0)
    int_boost = models.IntegerField(MaxValueValidator(999), default=0)
    spd_boost = models.IntegerField(MaxValueValidator(999), default=0)

    def add_armor_dice(self, armordice):
        if self.armor_dice.count() >= self.slots:
            raise Exception(f"This armor only has {self.slots} dice slots")
        self.armor_dice.add(armordice)

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __repr__(self):
        return '\n'.join([f"----------", f"[ID #{self.id}][Armor: {self.name}][Owner: {self.owner}][Price: {self.price}]", f"[ATK: {self.atk_boost}][DEF: {self.def_boost}][INT: {self.int_boost}][SPD: {self.spd_boost}][# of slots: {self.slots}]", "**********"])
####################################
######      Armor Dice        ######
####################################
class ArmorDice(models.Model):
    #info
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(Hero, related_name="armor_dice", on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey(Armor, related_name="armor_dice", on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(MaxValueValidator(99999), default=2000)

    def add_armor_dface(self, armor_dface):
        if self.armor_dfaces.count() >= 6:
            raise Exception(f"Cannot have more than 6 faces on a die")
        self.armor_dfaces.add(armor_dface)

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return '\n'.join([f"----------", f"[ID #{self.id}][ArmorDice: {self.name}][Price: {self.price}]", f"[Owner: {self.owner}][Parent: {self.parent}]", "**********"])



####################################
######      ArmorDface        ######
####################################
class ArmorDface(models.Model):
    #info
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(Hero, related_name="armor_dfaces", on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey(ArmorDice, related_name="armor_dfaces", on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(MaxValueValidator(99999), default=100)

    #battle
    roll_value = models.IntegerField(MaxValueValidator(99), default=0)
    critical = models.CharField(max_length=5, default="False")

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return '\n'.join([f"----------", f"[ID #{self.id}][ArmorDface: {self.name}][Price: {self.price}]", f"[Owner: {self.owner}][Parent: {self.parent}]", f"[Roll Value: {self.roll_value}][Critical: {self.critical}]"])

# ####################################
# ######       Accessory        ######
# ####################################
# class Accessory(models.Model):
#     #info
#     name = models.CharField(max_length=25)
#     level = models.IntegerField(MaxValueValidator(99), default=1)
#     price = models.IntegerField(MaxValueValidator(9999), default=100)

#     #abilities
#     ability1 = models.ForeignKey(Ability, related_name="acc_abl_1", on_delete="models.SET_NULL", blank=True, null=True)
#     ability2 = models.ForeignKey(Ability, related_name="acc_abl_2", on_delete="models.SET_NULL", blank=True, null=True)

#     #time stamps
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __repr__(self):
#         return f"<[Accessory name: {self.name}] [Price: {self.price}] [ID: {self.id}] /// Abilities: [{self.ability1.name}][{self.ability2.name}]>"


####################################
######         Items          ######
####################################
class Item(models.Model):
    #info
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(Hero, related_name="items", on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(MaxValueValidator(9999), default=100)

    #I.e. Heal: 100
    effect = models.CharField(max_length=100)
    value = models.IntegerField(MaxValueValidator(9999), default=100)

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __repr__(self):
         return f"<[ID: {self.id}][Item name: {self.name}] /// [Effect: {self.effect}:{self.value}]>"


####################################
######        Enemies         ######
####################################
class Enemy(models.Model):
    #info
    name = models.CharField(max_length=25)
    level = models.IntegerField(MaxValueValidator(999), default=1)
    element = models.CharField(max_length=15, blank=None, null=None)
    

    #attack
    rolls = models.IntegerField(MaxValueValidator(999), default=2)
    s1 = models.IntegerField(MaxValueValidator(99), default=1)
    s2 = models.IntegerField(MaxValueValidator(99), default=1)
    s3 = models.IntegerField(MaxValueValidator(99), default=1)
    s4 = models.IntegerField(MaxValueValidator(99), default=1)
    s5 = models.IntegerField(MaxValueValidator(99), default=2)
    s6 = models.IntegerField(MaxValueValidator(99), default=0)

    #rewards
    gold = models.IntegerField(MaxValueValidator(99999), default=10)
    gems = models.IntegerField(MaxValueValidator(9999), default=1)
    items = models.ManyToManyField(Item, related_name="enemy_drop", blank=True)

    #base stats
    hp_base = models.IntegerField(MaxValueValidator(999), default=100)
    atk_base = models.IntegerField(MaxValueValidator(999), default=0)
    def_base = models.IntegerField(MaxValueValidator(999), default=0)
    int_base = models.IntegerField(MaxValueValidator(999), default=0)
    spd_base = models.IntegerField(MaxValueValidator(999), default=5)

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return '\n'.join([f"----------", f"[ID #{self.id}]", f"[Enemy: {self.name}]", f"[Level: {self.level}]", f"[HP: {self.hp_base}]", f"[ATK: {self.atk_base}]", f"[DEF: {self.def_base}]", f"[INT: {self.int_base}]", f"[SPD: {self.spd_base}]",  f"[Gold dropped: {self.gold}]",  f"[Gems given: {self.gems}]", f"[Items dropped: {self.items}]", "----------"])


####################################
######        Ability         ######
####################################
class Ability(models.Model):
    #info
    name = models.CharField(max_length=25)
    heroes = models.ManyToManyField(Hero, related_name="abilities", blank=True)
    weapons = models.ManyToManyField(Weapon, related_name="abilities", blank=True)
    armors = models.ManyToManyField(Armor, related_name="abilities", blank=True)
    wpndice = models.ManyToManyField(WpnDice, related_name="abilities", blank=True)
    armordice = models.ManyToManyField(ArmorDice, related_name="abilities", blank=True)
    price = models.IntegerField(MaxValueValidator(9999), default=10)

    #elemental
    element = models.CharField(max_length=15, blank=True, null=True, default="None")
    value = models.IntegerField(MaxValueValidator(9999), default=1)

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<[ID: {self.id}] [Ability name: {self.name}] [Price: {self.price}]>"


####################################
######        Element         ######
####################################
class Element(models.Model):
    #info
    name = models.CharField(max_length=25)
    heroes = models.ManyToManyField(Hero, related_name="elements", blank=True)
    weapons = models.ManyToManyField(Weapon, related_name="elements", blank=True)
    armors = models.ManyToManyField(Armor, related_name="elements", blank=True)
    wpn_dfaces = models.ManyToManyField(WpnDface, related_name="elements", blank=True)
    armor_dfaces = models.ManyToManyField(ArmorDface, related_name="elements", blank=True)
    enemies = models.ManyToManyField(Enemy, related_name="elements", blank=True)

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<[ID: {self.id}][Element name: {self.name}]>"




####################################
######          End           ######
####################################