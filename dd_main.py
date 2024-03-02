import math
import dd_classes
import dd_game_lists
#import pygame

########## Font Colors ##########
blue_font = '\033[1;34;40m'
red_font = '\033[1;31;40m'
green_font = '\033[1;32;40m'
yellow_font = '\033[1;33;40m'
white_font = '\033[1;37;40m'

########## Creating the Battle Phases ##########
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
        print(f"{enemy.name} is now at {enemy.health} health\n")
        input(f"Press enter to continue...")
        return
    else:
        print(f"{player.name} has defeated {enemy.name}")
        player.xp = player.xp + enemy.xp
        print(f"\n{player.name} has obtained {enemy.xp} exp points\n")

        if player.xp >= player.xp_threshold:
            player.level_up()
            print(f"\n{player.name} has leveled up to level {player.level}",
            f"and obtained {player.stat_points} attribute points\n")
            player.set_stat_points()
        
        enemy.enemy_create_loot(equipment_matrix)
        print(f"{enemy.name} dropped {enemy.loot.name}")

        equip_check = input("\nWould you like to equip? [Y] or [N]?\n")

        if equip_check.lower() == 'y':
            loot_classification = enemy.loot.classification
            if getattr(player, loot_classification.lower()) is not None:
                player.unequip_equipment(loot_classification)
                player.equip_equipment(enemy.loot)
                print(f"\n{player.name} has equipped {getattr(player, loot_classification.lower()).name}")
            else:
                player.equip_equipment(enemy.loot)
                print(f"\n{player.name} has equipped {getattr(player, loot_classification.lower()).name}")
            
        else:
            print(f"\n{enemy.loot.name} has been added to inventory")
            player.items.append(enemy.loot)
        return

def enemy_turn(player, enemy):
    
    enemy_attack = enemy.enemy_attack()
    player_defense_reduction = math.floor((player.defense / 4))

    if player.shield is not None:
        player_shield_defense = player.shield.defense
    else:
        player_shield_defense = 0

    enemy_attack_actual = enemy_attack - (player_defense_reduction + player_shield_defense)
    
    if enemy_attack_actual <= 0:
        enemy_attack_actual = 0
        player.health = player.health - enemy_attack_actual
    else:
        player.health = player.health - enemy_attack_actual
        
    print(f"\n{enemy.name} hits {player.name} for {enemy_attack_actual} damage")
    if player.health > 0:
        print(f"{player.name} is now at {player.health} health\n")
        input("Press enter to continue...")

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


########## Create item pools #########

def create_equipment_matrix(*args):

    common_pool = []
    uncommon_pool = []
    rare_pool = []

    all_equipment = []

    matrix = []

    for arg in args:
        all_equipment.extend(arg)

    for equipment in all_equipment:
        if equipment['quality'] == 'Common':
            common_pool.append(equipment)
        elif equipment['quality'] == 'Uncommon':
            uncommon_pool.append(equipment)
        else:
            rare_pool.append(equipment)
    
    matrix.append(common_pool)
    matrix.append(uncommon_pool)
    matrix.append(rare_pool)

    return matrix


########## Create the Game Loop #########
game_on = True

player_name = input("\nPlease enter hero name\n")

hero = dd_classes.Player(player_name)
hero.roll_player_stats()
hero.add_dice(3)

current_world = 1
current_stage = 1

equipment_matrix = create_equipment_matrix(dd_game_lists.weapons, dd_game_lists.shields, dd_game_lists.armors)

print(f"\nHero has been created...\n{hero}")

while game_on:
    
    if hero.health <= 0:
        game_on = False
        break
    elif current_stage > 4:
        game_on = False
        break
    else:
        created_stage = dd_classes.Stage(current_world, current_stage, dd_game_lists.enemy_list)
        created_enemy = created_stage.spawned_enemy
        print("\n---------------------------")
        print(f"Entering {created_stage}")
        print("---------------------------\n")
        print(f"Enemy has been created...\n{created_enemy}")
        battle(hero, created_enemy)
        current_stage = current_stage + 1

exit()

# Initiate Python Script
if __name__ == '__main__':
    main()
