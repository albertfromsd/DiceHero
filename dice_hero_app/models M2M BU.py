from django.db import models
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
# from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

####################################
######          User          ######
####################################
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    
    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<[User name: {self.first_name} {self.last_name} ID: #{self.id}] [Email: {self.email}] [Heroes: {self.heroes.all()}]>"


####################################
######          Hero          ######
####################################
class Hero(models.Model):
    name = models.CharField(max_length=255)
    level = models.IntegerField(MaxValueValidator(99), default=1)
    user = models.ForeignKey(User, related_name="heroes", on_delete=models.CASCADE, blank=True, null=True)
    #inventory
    gold = models.IntegerField(MaxValueValidator(999999), default=100)
    gems = models.IntegerField(MaxValueValidator(99999), default=10)
    #base stats
    hp_base = models.IntegerField(MaxValueValidator(999), default=100)
    atk_base = models.IntegerField(MaxValueValidator(99), default=0)
    def_base = models.IntegerField(MaxValueValidator(99), default=0)
    int_base = models.IntegerField(MaxValueValidator(99), default=0)
    spd_base = models.IntegerField(MaxValueValidator(99), default=0)

    def add_weapon(self, weapon):
        if self.weapons.count() >= 2:
            raise Exception("Only two weapons allowed per hero")
        self.weapons.add(weapon)

    def add_armor(self, armor):
        if self.armors.count() >= 1:
            raise Exception("Only 1 armor allowed per hero")
        self.armors.add(armor)

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<[ID: {self.id}][Hero name: {self.name}] [User: {self.user}]  /// [HP: {self.hp_base}] [ATK: {self.atk_base}] [DEF: {self.def_base}] [INT: {self.int_base}] [SPD: {self.spd_base}]>"

####################################
######         Weapon         ######
####################################
class Weapon(models.Model):
    #info
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(Hero, related_name="weapons", on_delete=models.CASCADE, blank=True, null=True)
    level = models.IntegerField(MaxValueValidator(99), default=1)
    price = models.IntegerField(MaxValueValidator(9999), default=100)
    attack = models.IntegerField(MaxValueValidator(99), default=1)
    slots = models.IntegerField(MaxValueValidator(10), default=2)

    def add_wpn_dice(self, wpndice):
        if self.wpn_dice.count() >= self.slots:
            raise Exception(f"This weapon only has {self.slots} dice slots")
        self.wpn_dice.add(wpndice)

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"< [ID: {self.id}][Weapon name: {self.name}] /// [ATK: {self.attack}] [# of slots: {self.slots}] ***** [Dice: {self.wpn_dice.all()}]>"


####################################
######     Weapon Dice        ######
####################################
class WpnDice(models.Model):
    #info
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(Hero, related_name="wpn_dice", on_delete=models.CASCADE, blank=True, null=True)
    parent_wpn = models.ForeignKey(Weapon, related_name="wpn_dice", on_delete=models.CASCADE, blank=True, null=True)
    level = models.IntegerField(MaxValueValidator(99), default=1)
    price = models.IntegerField(MaxValueValidator(9999), default=10)

    def add_wpn_dface(self, wpn_dface):
        if self.wpn_dfaces.count() >= 6:
            raise Exception(f"Cannot have more than 6 faces on a die")
        self.wpn_dfaces.add(wpn_dface)

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<[ID: {self.id}][WpnDice Name: {self.name}] [Owner: {self.owner}] [Price: {self.price}] ***** [Dfaces: {self.wpn_dfaces.all()}]>"


####################################
######       WpnDface         ######
####################################
class WpnDface(models.Model):
    #info
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(Hero, related_name="wpn_dfaces", on_delete=models.CASCADE, blank=True, null=True)
    parent_die = models.ManyToManyField(WpnDice, related_name="wpn_dfaces", blank=True)
    level = models.IntegerField(MaxValueValidator(99), default=1)
    price = models.IntegerField(MaxValueValidator(9999), default=10)

    #battle
    roll_value = models.IntegerField(MaxValueValidator(10), default=0)
    critical = models.CharField(max_length=5, default="False")


    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"< [ID: {self.id}][WpnDFace name: {self.name}] [Owner: {self.owner}] [Price: {self.price}] /// Roll Value: [{self.roll_value}]>"

####################################
######         Armor          ######
####################################
class Armor(models.Model):
    #info
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(Hero, related_name="armors", on_delete=models.CASCADE, blank=True, null=True)
    level = models.IntegerField(MaxValueValidator(99), default=1)
    price = models.IntegerField(MaxValueValidator(9999), default=100)
    defense = models.IntegerField(MaxValueValidator(99), default=1)
    slots = models.IntegerField(MaxValueValidator(10), default=2)

    def add_armor_dice(self, armordice):
        if self.armor_dice.count() >= self.slots:
            raise Exception(f"This armor only has {self.slots} dice slots")
        self.armor_dice.add(armordice)

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __repr__(self):
        return f"< [ID: {self.id}][Armor name: {self.name}] [Owner: {self.owner}] /// [DEF: {self.defense}] [# of slots: {self.slots}] *****  [Dice: {self.armor_dice.all()}] >"

####################################
######      Armor Dice        ######
####################################
class ArmorDice(models.Model):
    #info
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(Hero, related_name="armor_dice", on_delete=models.CASCADE, blank=True, null=True)
    parent_armor = models.ForeignKey(Armor, related_name="armor_dice", on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(MaxValueValidator(9999), default=10)

    def add_armor_dface(self, armor_dface):
        if self.armor_dfaces.count() >= 6:
            raise Exception(f"Cannot have more than 6 faces on a die")
        self.armor_dfaces.add(armor_dface)

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<[ID: {self.id}][ArmorDice name: {self.name}] [Owner: {self.owner}]  ***** [Dfaces: {self.armor_dfaces.all()}]>"



####################################
######      ArmorDface        ######
####################################
class ArmorDface(models.Model):
    #info
    name = models.CharField(max_length=25)
    parent_die = models.ManyToManyField(ArmorDice, related_name="armor_dfaces", blank=True)
    price = models.IntegerField(MaxValueValidator(9999), default=10)

    #battle
    roll_value = models.IntegerField(MaxValueValidator(10), default=0)
    critical = models.CharField(max_length=5, default="False")

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"< [ID: {self.id}][ArmorDFace name: {self.name}] /// Roll Value: [{self.roll_value}]>"


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
    name = models.CharField(max_length=255)
    level = models.IntegerField(MaxValueValidator(99), default=1)
    element = models.CharField(max_length=15, blank=None, null=None)

    #rewards
    gold = models.IntegerField(MaxValueValidator(9999), default=10)
    gems = models.IntegerField(MaxValueValidator(999), default=1)
    items = models.ManyToManyField(Item, related_name="enemy_drop", blank=True)

    #base stats
    hp = models.IntegerField(MaxValueValidator(99), default=100)
    atk = models.IntegerField(MaxValueValidator(99), default=0)
    defense = models.IntegerField(MaxValueValidator(99), default=0)
    spd = models.IntegerField(MaxValueValidator(99), default=0)

    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<[ID: {self.id}][Enemy name: {self.name}]  /// [HP: {self.hp}] [ATK: {self.atk}] [DEF: {self.defense}] [SPD: {self.spd}]>"


####################################
######        Ability         ######
####################################
class Ability(models.Model):
    #info
    name = models.CharField(max_length=25)
    heroes = models.ManyToManyField(Hero, related_name="abilities", blank=True)
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