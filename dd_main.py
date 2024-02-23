import random
import math
#import pygame

########## CREATING BATTLE PHASE ##########
def player_turn(player, enemy):
    
    crit_check, player_attack = player.player_attack()
    enemy_defense_reduction = math.floor((enemy.defense / 4))
    player_attack_actual = player_attack - enemy_defense_reduction
    
    if player_attack_actual <= 0:
        player_attack_actual = 0
        crit_check = False
        enemy.health = enemy.health - player_attack_actual
    else:
        enemy.health = enemy.health - player_attack_actual
        
    if crit_check:
        print(f"\n{player.name} CRIT hits {enemy.name} for {player_attack_actual} damage!!!")
    else:
        print(f"\n{player.name} hits {enemy.name} for {player_attack_actual} damage")
        
    if enemy.health > 0:
        print(f"{enemy.name} is now at {enemy.health} health")
        return
    else:
        print(f"{player.name} has defeated {enemy.name}")
        player.xp = player.xp + enemy.xp
        print(f"\n{player.name} has obtained {enemy.xp} exp points")
        if player.xp >= player.xp_threshold:
            player.level_up()
            print(f"{player.name} has leveled up to level {player.level}",
            f"and obtained {player.stat_points} attribute points")
            player.set_stat_points()
        return

def enemy_turn(player, enemy):
    
    enemy_attack = enemy.enemy_attack()
    player_defense_reduction = math.floor((player.defense / 4))
    enemy_attack_actual = enemy_attack - player_defense_reduction
    
    if enemy_attack_actual <= 0:
        enemy_attack_actual = 0
        player.health = player.health - enemy_attack_actual
    else:
        player.health = player.health - enemy_attack_actual
        
    print(f"\n{enemy.name} hits {player.name} for {enemy_attack_actual} damage")
    if player.health > 0:
        print(f"{player.name} is now at {player.health} health")
        return
    else:
        print(f"{enemy.name} has defeated {player.name}")
        return
    
def battle(player, enemy):
    print('\nBATTLE BEGINS!')
    
    battle_switch = True
    while battle_switch:
        
        if player.health <= 0 or enemy.health <= 0:
            battle_switch = False
            break
        else:
            player_turn(player, enemy)
            
        if player.health <= 0 or enemy.health <= 0:
            battle_switch = False
            break
        else:
            enemy_turn(player, enemy)


########## Create the Game Loop #########
game_on = True

hero = Player('Lonnie')
hero.roll_player_stats()
hero.add_dice(6)

current_world = 1
current_stage = 1

print(f"Hero has been created...\n{hero}")

while game_on:
    
    if hero.health <= 0:
        game_on = False
        break
    elif current_stage > 4:
        game_on = False
        break
    else:
        created_stage = Stage(current_world, current_stage, enemy_list)
        created_enemy = created_stage.spawned_enemy
        print(f"\n{created_stage}\n")
        print(f"\nEnemy has been created...\n{created_enemy}")
        battle(hero, created_enemy)
        current_stage = current_stage + 1
