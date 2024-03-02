import random
import math

########## CREATING GAME OBJECTS/CLASSES ##########

class Character:

    def __init__(self, name: str, level: int = 1, dice: int = 1):
        self.name = name
        self.level = level
        self.dice = dice
    
    def __str__(self):
        return(f'Name: {self.name}\n'
              + f'Level: {self.level}\n'
              + f'Health: {self.health}\n' 
              + f'Attack: {self.attack}\n' 
              + f'Defense: {self.defense}')

    # Add more dice to a character; Dice help determine attacks, more dice, higher attacks
    def add_dice(self, dice: int):
        self.dice = self.dice + dice
    
    # Determines the dice roll of a character
    def dice_roll(self, dice: int, handicap: int = 1, sides: int = 6):
        dice_roll_total = 0
        for dice in range(1, dice + 1):
            dice_roll_number = random.randrange(handicap, sides + 1)
            dice_roll_total += dice_roll_number
        
        return dice_roll_total

class Player(Character):

    def __init__(self, name: str):
        super().__init__(name)
        self.stat_points = 0
        self.xp = 0
        self.xp_threshold = self.level * 10
        self.weapon = None
        self.shield = None
        self.armor = None
        self.items = []

    # Determine players base stats for the game    
    def roll_player_stats(self):
        self.health = self.dice_roll(self.dice, 50, 60)
        self.attack = self.dice_roll(self.dice)
        self.defense = self.dice_roll(self.dice)

    # This will calculate the attack a player generates on their turn 
    def player_attack(self):
        float_attack_amount = ((self.dice_roll(self.dice) * (self.level / 2)) + self.attack)
        attack_amount = math.floor(float_attack_amount)
        attack_crit = False
        crit_roll = random.randrange(1, 100) + 1
        
        # Currently set to a 15% crit chance
        if crit_roll <= 15:
            attack_crit = True
            crit_attack_amount = round((((self.dice * 6) * (self.level / 2)) + self.attack) * 1.5)
            return (attack_crit, crit_attack_amount)
        else:
            return (attack_crit, attack_amount)
    
    # Increase player stats on level up, as well as give them 2 points to increase stats of their choice
    def level_up(self):

        health_roll = self.dice_roll(1, 4, 5)
        attack_roll = self.dice_roll(1, 1, 2)
        defense_roll = self.dice_roll(1, 1, 2)

        print(f"\n{self.name}'s health has increased by {health_roll}\n"
             + f"{self.name}'s attack has increased by {attack_roll}\n"
             + f"{self.name}'s defense has increased by {defense_roll}\n")

        self.level = self.level + 1
        self.health = self.health + health_roll
        self.attack = self.attack + attack_roll
        self.defense = self.defense + defense_roll
        self.stat_points = self.stat_points + 2
        self.xp_threshold = self.level * 10
    
    # Allows player to increase their stats for each point gained
    def set_stat_points(self):
        for point in range(self.stat_points):

            player_stat_choice = input('\nWhere would you like to assign an attribute point?\n'
                               + "[H] for health\n"
                               + "[A] for attack\n"
                               + "[D] for defense\n")

            if player_stat_choice.lower() == "h":
                self.health = self.health + 3
                print(f"\nHealth has been increased by 3\n")
            elif player_stat_choice.lower() == "a":
                self.attack = self.attack + 1
                print(f"\nAttack has been increased by 1\n")
            elif player_stat_choice.lower() == "d":
                self.defense = self.defense + 1
                print(f"\nDefense has been increased by 1\n")
            else:
                print("\nNo stats increased and lost a point...\n")

            self.stat_points = self.stat_points - 1
    
    # Determine new stats of a player after equipping an item
    def equip_equipment(self, equipment: object):
        if equipment.classification == "Armor":
            self.armor = equipment
            self.health = self.health + self.armor.health
        elif equipment.classification == "Weapon":
            self.weapon = equipment
            self.attack = self.attack + self.weapon.attack
        elif equipment.classification == "Shield":
            self.shield = equipment
            self.defense = self.defense + self.shield.defense

    # Return players stats back to base after removing an equipped item
    def unequip_equipment(self, classification: str):
        if classification == "Armor":
            self.health = self.health - self.armor.health
            self.armor = None
        elif classification == "Weapon":
            self.attack = self.attack - self.weapon.attack
            self.weapon = None
        elif classification == "Shield":
            self.defense = self.defense - self.shield.defense
            self.shield = None
        else:
            pass
        
class Enemy(Character):

    def __init__(self, name: str, level: int, health: int, attack: int, defense: int):
        super().__init__(name)
        self.level = level
        self.health = health
        self.attack = attack
        self.defense = defense
        self.xp = self.level * 2
        self.loot = None

        
    def enemy_attack(self):
        float_attack_amount = ((self.dice_roll(self.dice) * (self.level / 2)) + self.attack)
        attack_amount = math.floor(float_attack_amount)
        return attack_amount

    # Creates loot that an enemy will drop after being defeated in battle
    def enemy_create_loot(self, matrix):

        equipment_pool = 0
        equipment_slot = 0

        if self.level == 1:
            equipment_pool_check = random.randrange(60 + 1)
        elif self.level == 2:
            equipment_pool_check = random.randrange(90 + 1)
        else:
            equipment_pool_check = random.randrange(100 + 1)

        # Common loot roll 60% chance
        if equipment_pool_check <= 60:
            equipment_pool = 0
            equipment_slot = random.randrange(len(matrix[0]))
        # Uncommon loot roll 30% chance
        elif equipment_pool_check > 60 and equipment_pool_check < 90:
            equipment_pool = 1
            equipment_slot = random.randrange(len(matrix[1]))
        # Rare loot roll 10% chance
        else:
            equipment_pool = 2
            equipment_slot = random.randrange(len(matrix[2]))

        matrix_coordinates = (equipment_pool, equipment_slot)
        p, s = matrix_coordinates
        equipment = matrix[p][s]

        if equipment['classification'] == 'Armor':
            created_equipment = Armor(equipment['name'], equipment['quality'], equipment['classification'], equipment['description'], equipment['health'])
        elif equipment['classification'] == 'Weapon':
            created_equipment = Weapon(equipment['name'], equipment['quality'], equipment['classification'], equipment['description'], equipment['attack'])
        elif equipment['classification'] == 'Shield':
            created_equipment = Shield(equipment['name'], equipment['quality'], equipment['classification'], equipment['description'], equipment['defense'])
        
        self.loot = created_equipment

        return

    
class Equipment:

    def __init__(self, name: str, quality: str, classification: str, description: str):
        self.name = name
        self.quality = quality
        self.classification = classification
        self.description = description
    
class Weapon(Equipment):

    def __init__(self, name: str, quality: str, classification: str, description:str, attack: int ):
        super().__init__(name, quality, classification, description)
        self.attack = attack
        
    def __str__(self):
        return(f'Name: {self.name}\n'
              + f'Quality: {self.quality}\n'
              + f'Attack: {self.attack}\n' 
              + f'Description: {self.description}\n')

class Shield(Equipment):

    def __init__(self, name: str, quality: str, classification: str, description:str, defense: int):
        super().__init__(name, quality, classification, description)
        self.defense = defense
        
    def __str__(self):
        return(f'Name: {self.name}\n'
              + f'Quality: {self.quality}\n'
              + f'Defense: {self.defense}\n' 
              + f'Description: {self.description}\n')
        
class Armor(Equipment):

    def __init__(self, name: str, quality: str, classification: str, description:str, health: int):
        super().__init__(name, quality, classification, description)
        self.health = health
    
    def __str__(self):
        return(f'Name: {self.name}\n'
              + f'Quality: {self.quality}\n'
              + f'Health: {self.health}\n' 
              + f'Description: {self.description}\n')
    
# class EnemyDeck(Enemy):
#     def __init__(self, enemies: list):
        
#         self.all_enemies = []
        
#         for enemy in enemies:
#             created_enemy = (
#                             Enemy(enemy['name'],
#                             enemy['level'], 
#                             enemy['health'], 
#                             enemy['attack'],
#                             enemy['defense'])
#                             )
#             self.all_enemies.append(created_enemy)
        
class Stage:

    def __init__(self, world: str, level: int, enemies: list):
        self.world = world
        self.level = level
        self.spawned_enemy = (
                            Enemy(enemies[self.level -1]['name'],
                            enemies[self.level -1]['level'],
                            enemies[self.level -1]['health'],
                            enemies[self.level -1]['attack'],
                            enemies[self.level -1]['defense'])
                            )
        
    def __str__(self):
        return f"World {self.world}: Level {self.level}"