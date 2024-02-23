########## CREATING GAME OBJECTS/CLASSES ##########

class Character:
    def __init__(self, name: str, level: int = 1, dice: int = 1):
        self.name = name
        self.level = level
        self.items = []
        self.dice = dice
    
    def __str__(self):
        return(f'Name: {self.name}\n'
              + f'Level: {self.level}\n'
              + f'Health: {self.health}\n' 
              + f'Attack: {self.attack}\n' 
              + f'Defense: {self.defense}')
    
    def dice_roll(self, dice):
        dice_roll_total = 0
        for dice in range(1, dice + 1):
            dice_roll_number = random.randrange(1, 6) + 1
            dice_roll_total += dice_roll_number
        
        return dice_roll_total

class Player(Character):
    def __init__(self, name):
        super().__init__(name)
        self.stat_points = 0
        self.xp = 0
        self.xp_threshold = self.level * 10
        
    def roll_player_stats(self):
        self.health = (random.randrange(50, 60) + 1)
        self.attack = (random.randrange(2, 6) + 1)
        self.defense = (random.randrange(2, 6) + 1)
    
    def add_dice(self, dice):
        self.dice = self.dice + dice
    
    def player_attack(self):
        float_attack_amount = ((self.dice_roll(self.dice) * (self.level / 2)) + self.attack)
        attack_amount = math.floor(float_attack_amount)
        attack_crit = False
        crit_roll = random.randrange(1, 100) + 1 # 15% crit chance
        
        if crit_roll <= 15:
            attack_crit = True
            attack_crit_amount = round((((self.dice * 6) * (self.level / 2)) + self.attack) * 1.5)
            return (attack_crit, attack_crit_amount)
        else:
            return (attack_crit, attack_amount)
    
    def level_up(self):
        self.level = self.level + 1
        self.health = self.health + (random.randrange(5, 10) + 1)
        self.attack = self.attack + (random.randrange(1, 2) + 1)
        self.defense = self.defense + (random.randrange(1, 2) + 1)
        self.stat_points = self.stat_points + 2
        self.xp_threshold = self.level * 10
    
    def set_stat_points(self):
        
        for point in range(self.stat_points):
            player_stat_choice = input('\nWhere would you like to assign an attribute point?\n' +
                               "'H' for health\n" +
                               "'A' for attack\n" +
                               "'D' for defense\n")

            if player_stat_choice.lower() == "h":
                self.health = self.health + 5
            elif player_stat_choice.lower() == "a":
                self.attack = self.attack + 1
            elif player_stat_choice.lower() == "d":
                self.defense = self.defense + 1

            self.stat_points = self.stat_points - 1
        
class Enemy(Character):
    def __init__(self, name: str, level: int, health: int, attack: int, defense: int):
        super().__init__(name)
        self.level = level
        self.health = health
        self.attack = attack
        self.defense = defense
        self.xp = self.level * 2
        
    def enemy_attack(self):
        float_attack_amount = ((self.dice_roll(self.dice) * (self.level / 2)) + self.attack)
        attack_amount = math.floor(float_attack_amount)
        return attack_amount
    
class Equipment:
    def __init__(self, name, quality, description):
        self.name = name
        self.quality = quality
        self.description = description
    
class Weapon(Equipment):
    def __init__(self, name: str, quality: str, description:str, attack: int ):
        super().__init__(name, quality, description)
        self.attack = attack
        
    def __str__(self):
        return(f'Name: {self.name}\n'
              + f'Quality: {self.quality}\n'
              + f'Attack: {self.attack}\n' 
              + f'Description: {self.description}\n')

class Shield(Equipment):
    def __init__(self, name: str, quality: str, description:str, defense: int):
        super().__init__(name, quality, description)
        self.defense = defense
        
    def __str__(self):
        return(f'Name: {self.name}\n'
              + f'Quality: {self.quality}\n'
              + f'Defense: {self.defense}\n' 
              + f'Description: {self.description}\n')
        
class Armor(Equipment):
    def __init__(self, name: str, quality: str, description:str, health: int):
        super().__init__(name, quality, description)
        self.health = health
    
    def __str__(self):
        return(f'Name: {self.name}\n'
              + f'Quality: {self.quality}\n'
              + f'Health: {self.health}\n' 
              + f'Description: {self.description}\n')
    
class EnemyDeck(Enemy):
    
    def __init__(self, enemies: list):
        
        self.all_enemies = []
        
        for enemy in enemies:
            created_enemy = (
                            Enemy(enemy['name'],
                            enemy['level'], 
                            enemy['health'], 
                            enemy['attack'],
                            enemy['defense'])
                            )
            self.all_enemies.append(created_enemy)
        
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
        return f"Level {self.level}, world {self.world}"