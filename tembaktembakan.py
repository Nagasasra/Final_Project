import pygame
import Karakter# a python file created containing custom created classes and its subclasses (if any) with its methods and attributes, most of the functions in the game uses methods/attributes from this
import csv

# this function is for displaying characters/weapon types and its attributes
# used to display available characters/weapon types from the database.csv file
def print_option(list_option, title):
    print(title)
    for count, i in enumerate(list_option):
        print(str(count) + ". " + str(i))
    print("---------------------------------")

# characters list and its attributes are stored in this char_database.csv file
data1 = open("char_database.csv")
data1_read = csv.DictReader(data1)
# those information from the database will be stored in this variable below by using loop
chars = []
for each_row in data1_read:
    images1 = [each_row["filepath1"], each_row["filepath1move1"], each_row["filepath1move2"]]
    images2 = [each_row["filepath2"], each_row["filepath2move1"], each_row["filepath2move2"]]
    new_char = Karakter.Karakter(each_row["name"], int(each_row["jumping"]), images1, images2, int(each_row["speed"]), int(each_row["falling"]), int(each_row["height"]), int(each_row["width"]), int(each_row["health"]))
    chars.append(new_char)

# attacks type list and its attributes are stored in this weap_database.csv file
data2 = open("weap_database.csv")
data2_read = csv.DictReader(data2)
# those information from the database will be stored in this variable below by using loop
weapons = []
for each_row1 in data2_read:
    if each_row1["y_speed"] == "0" and each_row1["consecutive"] == "0":
        new_weapon = Karakter.Weapon(each_row1["Fire-type"], int(each_row1["damage"]), float(each_row1["interval"]), float(each_row1["x_speed"]), float(each_row1["y_speed"]))
    elif each_row1["y_speed"] == "0" and each_row1["consecutive"] == "2":
        new_weapon = Karakter.Doublefire(each_row1["Fire-type"], int(each_row1["damage"]), float(each_row1["interval"]), float(each_row1["x_speed"]), float(each_row1["y_speed"]))
    elif each_row1["y_speed"] == "0" and each_row1["consecutive"] == "4":
        new_weapon = Karakter.Quadruplefire(each_row1["Fire-type"], int(each_row1["damage"]), float(each_row1["interval"]), float(each_row1["x_speed"]), float(each_row1["y_speed"]))
    else:
        new_weapon = Karakter.Threeway(each_row1["Fire-type"], int(each_row1["damage"]), float(each_row1["interval"]), float(each_row1["x_speed"]), float(each_row1["y_speed"]))
    weapons.append(new_weapon)

# this function displays characters that are available, which is from 'chars' list, taken from the char_database.csv file
print_option(chars, "-------CHARACTER OPTIONS---------")
# player 1 then chose which available character to play as, each has different attributes such as how many health it has
p1 = input("Select index number of your character (Player 1): ")
# if the chosen character can't be found the program will displays this, and asks the player to input again
while not p1.isnumeric() or int(p1) not in range(len(chars)):
    print("Requested Character not Found")
    p1 = input("Select index number of your character (Player 1): ")

# this function displays weapon types that are available, which is from 'weapons' list, taken from the weap_database.csv file
print_option(weapons, "-------WEAPON OPTIONS------------")
# player 1 then chose which available weapon type to use, each has different attributes such as how many bullets per fire or how fast the bullets travel
p1_w = input("Select index number of your weapon (Player 1): ")
# if the chosen weapon can't be found the program will displays this, and asks the player to input again
while not p1_w.isnumeric() or int(p1_w) not in range(len(weapons)):
    print("Requested Weapon not Found")
    p1_w = input("Select index number of your weapon (Player 1): ")

# the chosen character and weapon for player 1 are removed from the list, which means player 2 won't have the same character/weapon type
p1 = chars.pop(int(p1))
p1.init_direction('RIGHT')
p1.set_weapon(weapons.pop(int(p1_w)))

print_option(chars, "-------CHARACTER OPTIONS---------")
# now it's player 2's turn to pick a character
p2 = input("Select index number of your character (Player 2): ")
while not p2.isnumeric() or int(p2) not in range(len(chars)):
    print("Requested Character not Found")
    p2 = input("Select index number of your character (Player 2): ")

print_option(weapons, "-------WEAPON OPTIONS------------")
# now it's player 2's turn to pick a weapon type
p2_w = input("Select index number of your weapon (Player 2): ")
while not p2_w.isnumeric() or int(p2_w) not in range(len(weapons)):
    print("Requested Weapon not Found")
    p2_w = input("Select index number of your weapon (Player 2): ")

# the chosen character and weapon for player 2 are also removed from the list
p2 = chars.pop(int(p2))
p2.init_direction('LEFT')
p2.set_weapon(weapons.pop(int(p2_w)))

print("\n"+"Players:")
print("Player 1: " + str(p1))
print("Player 2: " + str(p2))

data1.close()
data2.close()
########################################################################################################################
# setting the window resolution and the players' starting point
screen_width = 900
screen_height = 600
p1.init_coordinate(screen_width//4 - p1.width, screen_height//2)
p2.init_coordinate(3*screen_width//4, screen_height//2)

# background taken from https://opengameart.org/content/country-field
background_image = "images/background2.png"
tutorial_image = "images/tutorial.png"
clock = pygame.time.Clock()

pygame.init()

# texts that might appear on screen
font = pygame.font.SysFont("comicsansms", 30)
big_font = pygame.font.SysFont("comicsansms", 60)
game_over = big_font.render("GAME OVER..", True, (150, 0, 0))
p1_wins = big_font.render("P1 WINS!", True, (0, 128, 0))
p2_wins = big_font.render("P2 WINS!", True, (0, 128, 0))
pause = big_font.render("PAUSED", True, (255, 255, 255))
yes = font.render("YES", True, (0, 75, 150))
no = font.render("NO", True, (150, 0, 0))
ok = font.render("OK", True, (0, 0, 0))
quitting = font.render("EXIT", True, (150, 0, 0))
resume = font.render("RESUME", True, (0, 75, 150))
how_to_play = font.render("INSTRUCTIONS", True, (75, 150, 0))
rematch = font.render("TRY AGAIN?", True, (255, 255, 255))
restart = font.render("RESTART", True, (150, 150, 0))

# buttons that might appear on screen to be clicked
yes_button = yes.get_rect(topleft=(screen_width // 2 - yes.get_width() - yes.get_width() // 4, screen_height // 8 - yes.get_height() // 2))
no_button = no.get_rect(topleft=(screen_width // 2 + yes.get_width() // 2, screen_height // 8 - yes.get_height() // 2))
resume_button = resume.get_rect(topleft=(screen_width // 2 - resume.get_width() // 2, screen_height // 3 + resume.get_height() + resume.get_height() // 2))
restart_button = restart.get_rect(topleft=(screen_width // 2 - restart.get_width() // 2, screen_height // 3 + resume.get_height() + restart.get_height() + restart.get_height() // 2))
how_to_play_button = how_to_play.get_rect(topleft=(screen_width // 2 - how_to_play.get_width() // 2, screen_height // 3 + resume.get_height() + restart.get_height() + how_to_play.get_height() + how_to_play.get_height() // 2))
quitting_button = quitting.get_rect(topleft=(screen_width // 2 - quitting.get_width() // 2, screen_height // 3 + resume.get_height() + restart.get_height() + how_to_play.get_height() + quitting.get_height() + quitting.get_height() // 2))
ok_button = ok.get_rect(topleft=(screen_width // 2 - ok.get_width(), screen_height - screen_height // 10))

# displays the screen while also loading png files for the characters and background and put it into variables
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load(background_image).convert_alpha()
tutorial = pygame.image.load(tutorial_image).convert_alpha()

# default standing image
p1_standing = pygame.image.load(p1.get_image1()[0]).convert_alpha()
p2_standing = pygame.image.load(p2.get_image2()[0]).convert_alpha()

# standing image if facing the opposite direction of original starting direction
p1_standing_reversed = pygame.image.load(p1.get_image2()[0]).convert_alpha()
p2_standing_reversed = pygame.image.load(p2.get_image1()[0]).convert_alpha()

# default movement images
p1_movement = [pygame.image.load(p1.get_image1()[1]).convert_alpha(), pygame.image.load(p1.get_image1()[0]).convert_alpha(), pygame.image.load(p1.get_image1()[2]).convert_alpha()]
p2_movement = [pygame.image.load(p2.get_image2()[1]).convert_alpha(), pygame.image.load(p2.get_image2()[0]).convert_alpha(), pygame.image.load(p2.get_image2()[2]).convert_alpha()]

# movement images if facing the opposite direction of original starting direction
p1_movement_reversed = [pygame.image.load(p1.get_image2()[1]).convert_alpha(), pygame.image.load(p1.get_image2()[0]).convert_alpha(), pygame.image.load(p1.get_image2()[2]).convert_alpha()]
p2_movement_reversed = [pygame.image.load(p2.get_image1()[1]).convert_alpha(), pygame.image.load(p2.get_image1()[0]).convert_alpha(), pygame.image.load(p2.get_image1()[2]).convert_alpha()]

# conditions that would trigger different things if set true
exiting = False
win = False
paused = True
how_to = True
reversed1 = False# player 1 starts with its default direction which is right
reversed2 = False# player 2 starts with its default direction which is left

# this runs as long as the game is not exited/closed
while not exiting:
    # displays basic tutorial how to play before the game starts
    if paused is True and how_to is True:
        screen.blit(background, (0, 0))
        screen.blit(tutorial, (screen_width // 6, screen_height // 8))
        # by clicking ok button, the game will start
        screen.blit(ok, ok_button)

    moving1 = False# player 1 isn't moving not until you press the key
    moving2 = False# player 2 isn't moving not until you press the key

    # as long as the game isn't paused and no one's health has reached zero, the game continues
    if p1.get_health() > 0 and p2.get_health() > 0 and paused is False:

        # players always fall down because of gravity (which is why a button/key for going down isn't needed)
        # might also land on another player if it's located right below
        down_limit = screen_height - screen_height // 10
        if p2.get_coordinate()[1] >= p1.get_coordinate()[1] + p1.height and p2.get_coordinate()[0] + p2.width // 2 >= p1.get_coordinate()[0] and p2.get_coordinate()[0] + p2.width // 2 <= p1.get_coordinate()[0] + p1.width:
            down_limit = p2.get_coordinate()[1]
        p1.movement("DOWN", screen_width, 0, down_limit)
        down_limit = screen_height - screen_height // 10
        if p1.get_coordinate()[1] >= p2.get_coordinate()[1] + p2.height and p1.get_coordinate()[0] + p1.width // 2 >= p2.get_coordinate()[0] and p1.get_coordinate()[0] + p1.width // 2 <= p2.get_coordinate()[0] + p2.width:
            down_limit = p1.get_coordinate()[1]
        p2.movement("DOWN", screen_width, 0, down_limit)

        # to get initial coordinates for the bullets
        p1.get_weapon().coordinate = p1.get_coordinate()
        p2.get_weapon().coordinate = p2.get_coordinate()

        # getting rid of projectiles that are out of the screen already, also the ones that hit the target
        p1.get_weapon().update_bullets_list(p2, screen_width)
        p2.get_weapon().update_bullets_list(p1, screen_width)

        # movements of characters on screen when holding the key
        # player can move left or right even when airborne as long as it remains on screen
        # players may pushes each other when colliding
        hold = pygame.key.get_pressed()
        # this key is for the right movement of player 1
        if hold[pygame.K_d]:
            moving1 = True
            # when going right if there is another player on your right, it may pushes it further to the right when colliding if in the same level
            if p1.get_coordinate()[0] + p1.width >= p2.get_coordinate()[0] - 5 and p1.get_coordinate()[0] + p1.width <= p2.get_coordinate()[0] + 5:
                if p1.get_coordinate()[1] + p1.height in range(p2.get_coordinate()[1], p2.get_coordinate()[1] + p2.height + 1):
                    moving2 = True
                    p2.movement("RIGHT", screen_width, p1.get_coordinate()[0] + p1.width, screen_height)
                    p1.movement("RIGHT", p2.get_coordinate()[0], 0, screen_height)
                else:
                    p1.movement("RIGHT", screen_width, 0, screen_height)
            else:
                p1.movement("RIGHT", screen_width, 0, screen_height)

        # this key is for the left movement of player 1
        elif hold[pygame.K_a]:
            moving1 = True
            # when going left if there is another player on your left, it may pushes it further to the left when colliding if in the same level
            if p1.get_coordinate()[0] >= p2.get_coordinate()[0] + p2.width - 5 and p1.get_coordinate()[0] <= p2.get_coordinate()[0] + p2.width + 5:
                if p1.get_coordinate()[1] + p1.height in range(p2.get_coordinate()[1], p2.get_coordinate()[1] + p2.height + 1):
                    moving2 = True
                    p2.movement("LEFT", p1.get_coordinate()[0], 0, screen_height)
                    p1.movement("LEFT", screen_width, p2.get_coordinate()[0] + p2.width, screen_height)
                else:
                    p1.movement("LEFT", screen_width, 0, screen_height)
            else:
                p1.movement("LEFT", screen_width, 0, screen_height)

        # this key is for the right movement of player 2
        if hold[pygame.K_RIGHT]:
            moving2 = True
            # when going right if there is another player on your right, it may pushes it further to the right when colliding if in the same level
            if p2.get_coordinate()[0] + p2.width >= p1.get_coordinate()[0] - 5 and p2.get_coordinate()[0] + p2.width <= p1.get_coordinate()[0] + 5:
                if p2.get_coordinate()[1] + p2.height in range(p1.get_coordinate()[1], p1.get_coordinate()[1] + p1.height + 1):
                    moving1 = True
                    p1.movement("RIGHT", screen_width, p2.get_coordinate()[0], screen_height)
                    p2.movement("RIGHT", p1.get_coordinate()[0], 0, screen_height)
                else:
                    p2.movement("RIGHT", screen_width, 0, screen_height)
            else:
                p2.movement("RIGHT", screen_width, 0, screen_height)

        # this key is for the left movement of player 2
        elif hold[pygame.K_LEFT]:
            moving2 = True
            # when going left if there is another player on your left, it may pushes it further to the left when colliding if in the same level
            if p2.get_coordinate()[0] >= p1.get_coordinate()[0] + p1.width - 5 and p2.get_coordinate()[0] <= p1.get_coordinate()[0] + p1.width + 5:
                if p2.get_coordinate()[1] + p2.height in range(p1.get_coordinate()[1] - 1, p1.get_coordinate()[1] + p1.height + 2):
                    moving1 = True
                    p1.movement("LEFT", p2.get_coordinate()[0], 0, screen_height)
                    p2.movement("LEFT", screen_width, p1.get_coordinate()[0] + p1.width, screen_height)
                else:
                    p2.movement("LEFT", screen_width, 0, screen_height)
            else:
                p2.movement("LEFT", screen_width, 0, screen_height)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exiting = True
        if event.type == pygame.KEYDOWN:
            # if the game isn't paused all these buttons could be clicked
            if paused is False:

                # players can jump infinitely as high as possible as long as it remains on the screen
                # if there is another player sitting right above you, you can not jump at all
                # if the other player is right above you but not touching you, you could still jump but you would bump into that other player
                # this key is for jumping for player 1
                if event.key == pygame.K_w:
                    up_limit = 0
                    if p1.get_coordinate()[1] >= p2.get_coordinate()[1] + p2.height and p1.get_coordinate()[0] + p1.width // 2 >= p2.get_coordinate()[0] and p1.get_coordinate()[0] + p1.width // 2 <= p2.get_coordinate()[0] + p2.width:
                        up_limit = p2.get_coordinate()[1] + p2.height
                    p1.movement("UP", screen_width, 0, screen_height, up_limit)

                # this key is for jumping for player 2
                if event.key == pygame.K_UP:
                    up_limit = 0
                    if p2.get_coordinate()[1] >= p1.get_coordinate()[1] + p1.height and p2.get_coordinate()[0] + p2.width // 2 >= p1.get_coordinate()[0] and p2.get_coordinate()[0] + p2.width // 2 <= p1.get_coordinate()[0] + p1.width:
                        up_limit = p1.get_coordinate()[1] + p1.height
                    p2.movement("UP", screen_width, 0, screen_height, up_limit)

                # players will fire to inflict damage upon another by pressing this button. however you can only fire again once the reloading interval is over
                # each weapon type including the one that you chose earlier has an attribute called "interval", which is basically how long you have to wait before you could fire again in seconds
                # if you try pressing this button when the reloading interval isn't over yet then nothing happens
                # this button is for firing for player 1
                if event.key == pygame.K_r:
                    p1.fire()
                # this button is for firing for player 2
                if event.key == pygame.K_SLASH:
                    p2.fire()

                # this is to change the direction where your character's facing in case you want to fire the opposite direction
                # this would be very useful if the enemy somehow ended up behind you
                # there can only be two directions: right or left
                if event.key == pygame.K_t:
                    if reversed1 is False:
                        p1.set_direction("LEFT")
                        reversed1 = True
                    elif reversed1 is True:
                        p1.set_direction("RIGHT")
                        reversed1 = False
                    p1.walk_count = 0
                if event.key == pygame.K_PERIOD:
                    if reversed2 is False:
                        p2.set_direction("RIGHT")
                        reversed2 = True
                    elif reversed2 is True:
                        p2.set_direction("LEFT")
                        reversed2 = False
                    p2.walk_count = 0

            # pressing escape key will pause the game
            # pressing it again will unpause it, resuming the game
            if event.key == pygame.K_ESCAPE:
                if win is False:# game can only be paused when the game hasn't ended yet (when no one's won yet)
                    if paused is False:
                        paused = True
                    elif paused is True:
                        paused = False
                        how_to = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # when someone has already won the game, the text "TRY AGAIN?", "NO" button and "YES" button will appear on screen
            # clicking "YES" button with your mouse will result in a rematch, resetting everything to its initial value
            # clicking restart when the game is paused will also result in a rematch
            if win is True and yes_button.collidepoint(event.pos) or paused is True and how_to is False and restart_button.collidepoint(event.pos):
                p1.init_coordinate(screen_width//4 - p1.width, screen_height//2)
                p2.init_coordinate(3 * screen_width // 4, screen_height // 2)
                p1.set_health(p1.max_health)
                p2.set_health(p2.max_health)
                p1.set_direction('RIGHT')
                p2.set_direction('LEFT')
                p1.get_weapon().reset_bullets()
                p2.get_weapon().reset_bullets()
                reversed1 = False
                reversed2 = False
                win = False
                paused = False
            # clicking "NO" will close the game for good, also clicking exit when the game is paused
            if win is True and no_button.collidepoint(event.pos) or win is False and paused is True and how_to is False and quitting_button.collidepoint(event.pos):
                exiting = True
            # clicking resume when the game is paused or ok when looking for instructions will unpause the game
            if win is False and paused is True and how_to is False and resume_button.collidepoint(event.pos) or ok_button.collidepoint(event.pos):
                paused = False
                how_to = False
            # this is for showing the tutorial by clicking instructions when the game is paused
            if win is False and paused is True and how_to_play_button.collidepoint(event.pos):
                screen.blit(background, (0, 0))
                how_to = True

    # if no one's won the game yet, the game will keep going
    if win is False and paused is False:
        # displays the background for updating object locations and others
        screen.blit(background, (0, 0))

        # these loops are for displaying the projectiles across the screen after being fired, they are drawn circles with the color black to make it recognizable
        # how fasts it travels depends on the speed of the weapon type that you chose, each weapon type has an attribute called "x_speed"
        # note that this only displays it when it's still visible on screen, if the bullet has reached outside the boundary of the screen it will be removed by different function
        for coord in p1.get_weapon().fired_bullets:
            pygame.draw.circle(screen, (0, 0, 0), (int(coord[0]), int(coord[1])), 5)
        for coord in p2.get_weapon().fired_bullets:
            pygame.draw.circle(screen, (0, 0, 0), (int(coord[0]), int(coord[1])), 5)

        # showing the walking animations for the player1, else if it's not moving then he'll be just standing there
        if moving1 is True:
            if p1.walk_count > len(p1_movement) - 1:
                p1.walk_count = 0
            if reversed1 is False:
                screen.blit(p1_movement[p1.walk_count], (p1.get_coordinate()[0], p1.get_coordinate()[1]))
            else:
                screen.blit(p1_movement_reversed[p1.walk_count], (p1.get_coordinate()[0], p1.get_coordinate()[1]))
            p1.walk_count += 1
        else:
            if reversed1 is False:
                screen.blit(p1_standing, (p1.get_coordinate()[0], p1.get_coordinate()[1]))
            else:
                screen.blit(p1_standing_reversed, (p1.get_coordinate()[0], p1.get_coordinate()[1]))

        # showing the walking animations for the player2, else if it's not moving then he'll be just standing there
        if moving2 is True:
            if p2.walk_count > len(p2_movement) - 1:
                p2.walk_count = 0
            if reversed2 is False:
                screen.blit(p2_movement[p2.walk_count], (p2.get_coordinate()[0], p2.get_coordinate()[1]))
            else:
                screen.blit(p2_movement_reversed[p2.walk_count], (p2.get_coordinate()[0], p2.get_coordinate()[1]))
            p2.walk_count += 1
        else:
            if reversed2 is False:
                screen.blit(p2_standing, (p2.get_coordinate()[0], p2.get_coordinate()[1]))
            else:
                screen.blit(p2_standing_reversed, (p2.get_coordinate()[0], p2.get_coordinate()[1]))

        # these drawn rectangles down below are for the health bar for player1 and player2, with player1's bar positioned on the top left while player2's bar on the top right
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(screen_width // 30, screen_height // 20, screen_width // 4, screen_height // 20))
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(screen_width - screen_width // 4 - 30, 30, screen_width // 4, screen_height // 20))
        pygame.draw.rect(screen, (255, 102, 102), pygame.Rect(screen_width // 30, screen_height // 20, screen_width // 4 * p1.get_health() // p1.max_health, screen_height // 20))
        pygame.draw.rect(screen, (255, 102, 102), pygame.Rect(screen_width - screen_width // 4 - 30, screen_height // 20, screen_width // 4 * p2.get_health() // p2.max_health, screen_height // 20))

        # these are for displaying the corresponding health in numbers located right below its respective bars
        p1_health = font.render(str(p1.get_health()) + "/" + str(p1.max_health), True, (255, 0, 0))
        p2_health = font.render(str(p2.get_health()) + "/" + str(p2.max_health), True, (255, 0, 0))
        screen.blit(p1_health, (screen_width // 30, screen_height // 10))
        screen.blit(p2_health, (screen_width - 30 - p2_health.get_width(), screen_height // 10))

    # during a pause the program will displays various buttons such as resume, restart, instructions, and exit
    # clicking resume will unpause it, clicking restart will reset everything and start the game all over again
    # an image containing the controls and the objectives of the game will show up if instructions is clicked, clicking exit will close the game for good
    # the game will be halted when paused, you can't move or fire or anything
    # press esc key again to unpause to resume the game
    if paused is True and how_to is False:
        screen.blit(pause, (screen_width // 2 - pause.get_width() // 2, screen_height // 3 - pause.get_height() // 2))
        screen.blit(resume, resume_button)
        screen.blit(how_to_play, how_to_play_button)
        screen.blit(restart, restart_button)
        screen.blit(quitting, quitting_button)

    # if player2's health reaches zero, the game ends and it will display the text "P1 WINS!" (which is player1)
    if p1.get_health() > 0 and p2.get_health() == 0:
        screen.blit(p1_wins, (screen_width // 2 - p1_wins.get_width() // 2, screen_height // 2 - p1_wins.get_height() // 2))
        win = True

    # else if player1's health reaches zero, the game ends and it will display the text "P2 WINS!" (which is player2)
    elif p1.get_health() == 0 and p2.get_health() > 0:
        screen.blit(p2_wins, (screen_width // 2 - p2_wins.get_width() // 2, screen_height // 2 - p2_wins.get_height() // 2))
        win = True

    # else if somehow you managed to kill each other in the exact same time within that split second (nearly impossible to achieve this)
    # it will display the text "GAME OVER"
    elif p1.get_health() == 0 and p2.get_health() == 0:
        screen.blit(game_over, (screen_width // 2 - game_over.get_width() // 2, screen_height // 2 - game_over.get_height() // 2))
        win = True

    # when either or both of the player's health reaches zero the game'll end and displays the text "TRY AGAIN?" on the top of the screen, also displaying "NO" button and "YES" button
    # player may choose to either quit the game by clicking the button 'NO' with mouse that appears on screen, or 'YES' which is basically a rematch
    if win is True and paused is False:
        screen.blit(rematch, (screen_width // 2 - rematch.get_width() // 2, screen_height // 20 - rematch.get_height() // 2))
        screen.blit(yes, yes_button)
        screen.blit(no, no_button)

    # mouse is set to be visible since there may be buttons to click on screen
    pygame.mouse.set_visible(True)
    pygame.display.flip()

    # these clock tick is to reduce lag. Note that if this value is changed then many other values such as speed in the database.csv might need to be readjusted to maintain the same velocity
    clock.tick(240)
