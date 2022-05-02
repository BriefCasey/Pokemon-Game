# BEFORE RUNNING PLEASE BE SURE TO DO THE FOLLOWING:
# Download the 3 images attached
# place this file in a folder and create a folder within that folder called 'images'
# place the three images into that folder
# now run this program




# importing modules, pygame is the main module used to create this game
import pygame as pg
import random

# initalizing the module
pg.init()

# the 3 colors used in the game, mirroring the original gameboy colors, as tuples (R,G,B)
color = (139, 172, 15)
color_light = (155, 188, 15)
color_dark = (48, 98, 48)

# width and height of the screen displaying the screen with those sizes
width = 832
height = 704
screen = pg.display.set_mode((width, height))

# the fonts that will be used in the game, with sizes
smallfont = pg.font.SysFont('Comic Sans', 35)
bigfont = pg.font.SysFont('Comic Sans', 90)

# storing this vector creation into a short variable to use later with ease
vec = pg.math.Vector2

# creating variables that will be used later, but they need to be set to first before use
left_pkmn = None
right_pkmn = None
turn = None
score = vec(0, 0)
move_line1_rect = pg.Rect(0, 0, 1, 1)
move_line1_surf = pg.Surface((5, 5))
move_line1_surf.fill(color_light)
move_line2_rect = pg.Rect(0, 0, 1, 1)
move_line2_surf = pg.Surface((5, 5))
move_line2_surf.fill(color_light)
cooldown=1500
last_played=0


# setting all images to variables, using pygame to load them in

# pokemon 1
venusaur_img = pg.image.load('images/venusaur2.jpg').convert()
venusaur_img = pg.transform.scale(venusaur_img, (100, 100))
venusaur_img.set_colorkey((128, 128, 128))
venusaur_fight_R = pg.transform.scale(venusaur_img, (300, 300))
venusaur_fight_L=pg.transform.flip(venusaur_fight_R,True,False)

#pokemon 2
charizard_img = pg.image.load('images/charizard2.jpg').convert()
charizard_img = pg.transform.scale(charizard_img, (120, 80))
charizard_img.set_colorkey((128, 128, 128))
charizard_fight_R = pg.transform.scale(charizard_img, (360, 240))
charizard_fight_L=pg.transform.flip(charizard_fight_R,True,False)

#pokemon 3
blastoise_img = pg.image.load('images/blastoise.jpg').convert()
blastoise_img = pg.transform.scale(blastoise_img, (100, 100))
blastoise_img.set_colorkey((128, 128, 128))
blastoise_fight_L = pg.transform.scale(blastoise_img, (300, 300))
blastoise_fight_R=pg.transform.flip(blastoise_fight_L,True,False)

# created classes to store all the stats of the each pokemon
class Blastoise:
    def __init__(self):
        self.image = blastoise_img
        self.pkmntype = 'water'
        self.defense_stage = 0
        self.HP = 362
        self.attack = 291
        self.defense = 328 * (0.5 * self.defense_stage + 1)
        self.spatk = 295
        self.spdef = 339
        self.speed = 280
        self.defense_type = None
        self.max_hp = 362
        self.status=None

    # defining moves and setting a variable of text to the name of the move
    # did this for each of the four moves
    def move1(self, p2):
        global move_line1_surf, move_line1_rect, move_line2_surf, move_line2_rect
        self.power = 110 # power is for the damage calculation
        self.type = 'water' # move type to check effectiveness later
        self.atk_dam = self.spatk # type of attack damage for damage calculation
        global move_line1_surf, move_line1_rect, move_line2_surf, move_line2_rect
        move_line1_surf, move_line1_rect = text_objects('Blastoise used', smallfont)
        move_line2_surf, move_line2_rect = text_objects('Hydro Pump!', smallfont)
        p2.defense_type = p2.spdef # match the type of attack damage to the defense type for opposing pokemon

    def move2(self, p2):
        self.HP += 328 * 0.0625
        self.type = 'status'
        global move_line1_surf, move_line1_rect, move_line2_surf, move_line2_rect
        move_line1_surf, move_line1_rect = text_objects('Blastoise used', smallfont)
        move_line2_surf, move_line2_rect = text_objects('Aqua Ring!', smallfont)

    def move3(self, p2):
        self.defense_stage += 1
        self.type = 'status'
        global move_line1_surf, move_line1_rect, move_line2_surf, move_line2_rect
        move_line1_surf, move_line1_rect = text_objects('Blastoise used', smallfont)
        move_line2_surf, move_line2_rect = text_objects('Withdraw!   ', smallfont)

    def move4(self, p2):
        self.power = 60
        self.type = 'dark'
        self.atk_dam = self.attack
        self.acc = 100
        p2.defense_type = p2.defense
        global move_line1_surf, move_line1_rect, move_line2_surf, move_line2_rect
        move_line1_surf, move_line1_rect = text_objects('Blastoise used', smallfont)
        move_line2_surf, move_line2_rect = text_objects('Bite!    ', smallfont)

# same as above, but with Charizard
class Charizard:
    def __init__(self):
        self.pkmntype = 'fire'
        self.HP = 360
        self.attack = 293
        self.defense = 280
        self.spatk = 348
        self.spdef = 295
        self.speed = 328
        self.defense_type = None
        self.max_hp = 360
        self.status=None
    # same thing of defining moves
    def move1(self, p2):
        self.power = 90
        self.type = 'fire'
        self.atk_dam = self.spatk
        self.acc = 100
        p2.defense_type = p2.spdef
        global move_line1_surf, move_line1_rect, move_line2_surf, move_line2_rect
        move_line1_surf, move_line1_rect = text_objects('Charizard used', smallfont)
        move_line2_surf, move_line2_rect = text_objects('Flamethrower!', smallfont)

    def move2(self, p2):
        self.power = 80
        self.type = 'dragon'
        self.atk_dam = self.attack
        self.acc = 100
        p2.defense_type = p2.defense
        global move_line1_surf, move_line1_rect, move_line2_surf, move_line2_rect
        move_line1_surf, move_line1_rect = text_objects('Charizard used', smallfont)
        move_line2_surf, move_line2_rect = text_objects('Dragon Claw!', smallfont)

    def move3(self, p2):
        self.power = 100
        self.type = 'steel'
        self.atk_dam = self.attack
        self.acc = 75
        p2.defense_type = p2.defense
        global move_line1_surf, move_line1_rect, move_line2_surf, move_line2_rect
        move_line1_surf, move_line1_rect = text_objects('Charizard used', smallfont)
        move_line2_surf, move_line2_rect = text_objects('Iron Tail!', smallfont)

    def move4(self, p2):
        self.power = 60
        self.type = 'flying'
        self.atk_dam = self.attack
        self.acc = 100
        p2.defense_type = p2.defense
        global move_line1_surf, move_line1_rect, move_line2_surf, move_line2_rect
        move_line1_surf, move_line1_rect = text_objects('Charizard used', smallfont)
        move_line2_surf, move_line2_rect = text_objects('Wing Attack!', smallfont)

# third pokemon class, same as above
class Venusaur:
    def __init__(self):
        self.pkmntype = 'grass'
        self.HP = 364
        self.attack = 289
        self.defense = 291
        self.spatk = 328
        self.spdef = 328
        self.speed = 284
        self.defense_type = None
        self.recharge = False
        self.max_hp = 364
        self.status=None
    # same thing of defining four moves
    def move1(self, p2):
        self.power = 120
        self.type = 'grass'
        self.atk_dam = self.spatk
        self.acc = 100
        p2.defense_type = p2.defense
        self.recharge = True
        global move_line1_surf, move_line1_rect, move_line2_surf, move_line2_rect
        move_line1_surf, move_line1_rect = text_objects('Venusaur used', smallfont)
        move_line2_surf, move_line2_rect = text_objects('Solar Beam!', smallfont)

    def move2(self, p2):
        self.type = 'ground'
        self.power = 100
        self.atk_dam = self.attack
        self.acc = 100
        p2.defense_type = p2.defense
        global move_line1_surf, move_line1_rect, move_line2_surf, move_line2_rect
        move_line1_surf, move_line1_rect = text_objects('Venusaur used', smallfont)
        move_line2_surf, move_line2_rect = text_objects('Earthquake!', smallfont)

    def move3(self, p2):
        self.power = 75
        self.type = 'grass'
        self.atk_dam = self.spatk
        self.acc = 100
        p2.defense_type = p2.defense
        self.HP += self.max_hp*0.0625
        global move_line1_surf, move_line1_rect, move_line2_surf, move_line2_rect
        move_line1_surf, move_line1_rect = text_objects('Venusaur used', smallfont)
        move_line2_surf, move_line2_rect = text_objects('Giga Drain!', smallfont)

    def move4(self, p2):
        self.type = 'status'
        self.acc = 75
        p2.status = 'poison'
        global move_line1_surf, move_line1_rect, move_line2_surf, move_line2_rect
        move_line1_surf, move_line1_rect = text_objects('Venusaur used', smallfont)
        move_line2_surf, move_line2_rect = text_objects('Poison Powder!', smallfont)



# creating a class to store the position and size of the cursor, using vector positions
class Cursor():
    def __init__(self):
        self.pos = vec(0, 0)
        self.image = pg.cursors.tri_left

    def cursor_pos(self):
        # depending on the screen, the position of the vector will be different
        if title_screen_on:
            if self.pos == vec(0, 0):
                pg.draw.rect(screen, color, pg.Rect(315, 285, 200, 30))
            if self.pos == vec(0, -1):
                pg.draw.rect(screen, color, pg.Rect(350, 335, 130, 30))
        elif one_player_on:
            if self.pos == vec(0, 0):
                pg.draw.rect(screen, color, pg.Rect(width / 2 - 60, height / 2 + 85, 120, 30))
            if self.pos == vec(-1, 0):
                pg.draw.rect(screen, color, pg.Rect(width / 2 - 260, height / 2 + 85, 120, 30))
            if self.pos == vec(1, 0):
                pg.draw.rect(screen, color, pg.Rect(width / 2 + 140, height / 2 + 85, 120, 30))
        elif one_battle_on:
            if self.pos == vec(0, 0):
                pg.draw.rect(screen, color, pg.Rect(15, 535, 170, 30))
            if self.pos == vec(1, 0):
                pg.draw.rect(screen, color, pg.Rect(275, 535, 160, 30))
            if self.pos == vec(0, 1):
                pg.draw.rect(screen, color, pg.Rect(40, 585, 120, 30))
            if self.pos == vec(1, 1):
                pg.draw.rect(screen, color, pg.Rect(275, 585, 160, 30))
        elif two_player_on:
            if left_pkmn is None:
                if self.pos == vec(0, 0):
                    pg.draw.rect(screen, color, pg.Rect(width / 2 - 60, height / 2 + 85, 120, 30))
                if self.pos == vec(-1, 0):
                    pg.draw.rect(screen, color, pg.Rect(width / 2 - 260, height / 2 + 85, 120, 30))
                if self.pos == vec(1, 0):
                    pg.draw.rect(screen, color, pg.Rect(width / 2 + 140, height / 2 + 85, 120, 30))
            else:
                if left_pkmn !=charizard and self.pos == vec(0, 0):
                    pg.draw.rect(screen, color, pg.Rect(width / 2 - 60, height / 2 + 85, 120, 30))
                if left_pkmn != blastoise and self.pos == vec(-1, 0):
                    pg.draw.rect(screen, color, pg.Rect(width / 2 - 260, height / 2 + 85, 120, 30))
                if left_pkmn != venusaur and self.pos == vec(1, 0):
                    pg.draw.rect(screen, color, pg.Rect(width / 2 + 140, height / 2 + 85, 120, 30))

        elif two_battle_on:
            if self.pos == vec(0, 0):
                pg.draw.rect(screen, color, pg.Rect(15, 535, 170, 30))
            if self.pos == vec(1, 0):
                pg.draw.rect(screen, color, pg.Rect(275, 535, 160, 30))
            if self.pos == vec(0, 1):
                pg.draw.rect(screen, color, pg.Rect(40, 585, 120, 30))
            if self.pos == vec(1, 1):
                pg.draw.rect(screen, color, pg.Rect(275, 585, 160, 30))
        elif result_screen_on:
            if self.pos == vec(0, 0):
                pg.draw.rect(screen, color, pg.Rect(350, 335, 130, 30))
            if self.pos == vec(0, -1):
                pg.draw.rect(screen, color, pg.Rect(325, 385, 180, 30))
            if self.pos == vec(0, -2):
                pg.draw.rect(screen, color, pg.Rect(340, 435, 150, 30))

# probably the most important part of the code, being able to register and compute all button presses
def get_buttons():
    global run, title_screen_on, two_player_on, one_player_on, left_pkmn, right_pkmn, one_battle_on, two_battle_on, turn, result_screen_on,last_move
    for event in pg.event.get():
        if event.type == pg.QUIT: # closing game if quit or if the x is pressed
            run = False
            title_screen_on = False
            two_player_on = False
            one_player_on = False
            two_battle_on = False
            result_screen_on = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a: # moving cursor to the left if applicable to the  screen
                if title_screen_on:
                    pass
                if (one_player_on or two_player_on) and cursor.pos.x > -1:
                    cursor.pos.x -= 1
                if (two_battle_on or one_battle_on) and cursor.pos.x > 0:
                    cursor.pos.x -= 1
                if result_screen_on:
                    pass
            if event.key == pg.K_d: # moving cursor to the right if applicable to the  screen
                if title_screen_on:
                    pass
                if (one_player_on or two_player_on) and cursor.pos.x < 1:
                    cursor.pos.x += 1
                if (two_battle_on or one_battle_on) and cursor.pos.x < 1:
                    cursor.pos.x += 1
                if result_screen_on:
                    pass
            if event.key == pg.K_w: # moving cursor up if applicable to the  screen
                if title_screen_on and cursor.pos.y < 0:
                    cursor.pos.y += 1
                if one_player_on:
                    pass
                if (two_battle_on or one_battle_on) and cursor.pos.y > 0:
                    cursor.pos.y -= 1
                if result_screen_on and cursor.pos.y < 0:
                    cursor.pos.y += 1
            if event.key == pg.K_s: # moving cursor down if applicable to the  screen
                if title_screen_on and cursor.pos.y > -1:
                    cursor.pos.y -= 1
                if one_player_on:
                    pass
                if (two_battle_on or one_battle_on) and cursor.pos.y < 1:
                    cursor.pos.y += 1
                if result_screen_on and cursor.pos.y > -2:
                    cursor.pos.y -= 1
            if event.key == pg.K_SPACE: # spacebar is the confirming button, computing what to do if space is pressed
                # depending on the screen and position
                if title_screen_on:
                    if cursor.pos == vec(0, 0):
                        one_player_on = True
                        title_screen_on = False
                        cursor.pos = vec(0, 0)
                    if cursor.pos == vec(0, -1):
                        two_player_on = True
                        title_screen_on = False
                        cursor.pos = vec(0, 0)
                elif one_player_on:
                    if cursor.pos == vec(0, 0):
                        left_pkmn = charizard
                        right_pkmn = random.randint(0, 1)
                        if right_pkmn == 1:
                            right_pkmn = blastoise
                        else:
                            right_pkmn = venusaur
                    if cursor.pos == vec(1, 0):
                        left_pkmn = venusaur
                        right_pkmn = random.randint(0, 1)
                        if right_pkmn == 1:
                            right_pkmn = charizard
                        else:
                            right_pkmn = blastoise
                    if cursor.pos == vec(-1, 0):
                        left_pkmn = blastoise
                        right_pkmn = random.randint(0, 1)
                        if right_pkmn == 1:
                            right_pkmn = venusaur
                        else:
                            right_pkmn = venusaur
                    one_battle_on = True
                    one_player_on = False
                    cursor.pos = vec(0, 0)
                elif one_battle_on and turn == left_pkmn:
                    if cursor.pos == vec(0, 0):
                        move(left_pkmn, right_pkmn, 1)
                        turn = right_pkmn
                        last_move = pg.time.get_ticks()
                    if cursor.pos == vec(1, 0):
                        move(left_pkmn, right_pkmn, 2)
                        turn = right_pkmn
                        last_move = pg.time.get_ticks()
                    if cursor.pos == vec(0, 1):
                        move(left_pkmn, right_pkmn, 3)
                        turn = right_pkmn
                        last_move = pg.time.get_ticks()
                    if cursor.pos == vec(1, 1):
                        move(left_pkmn, right_pkmn, 4)
                        turn = right_pkmn
                        last_move = pg.time.get_ticks()
                elif two_player_on:
                    if left_pkmn is None:
                        if cursor.pos == vec(0, 0):
                            left_pkmn = charizard
                        if cursor.pos == vec(1, 0):
                            left_pkmn = venusaur
                        if cursor.pos == vec(-1, 0):
                            left_pkmn = blastoise
                    else:
                        if cursor.pos == vec(0, 0) and left_pkmn != charizard:
                            right_pkmn = charizard
                            two_battle_on = True
                            two_player_on = False
                        if cursor.pos == vec(1, 0) and left_pkmn != venusaur:
                            right_pkmn = venusaur
                            two_battle_on = True
                            two_player_on = False
                        if cursor.pos == vec(-1, 0) and left_pkmn != blastoise:
                            right_pkmn = blastoise
                            two_battle_on = True
                            two_player_on = False
                        cursor.pos = vec(0, 0)
                elif two_battle_on and turn == left_pkmn:
                    if cursor.pos == vec(0, 0):
                        move(left_pkmn, right_pkmn, 1)
                        turn = right_pkmn
                    if cursor.pos == vec(1, 0):
                        move(left_pkmn, right_pkmn, 2)
                        turn = right_pkmn
                    if cursor.pos == vec(0, 1):
                        move(left_pkmn, right_pkmn, 3)
                        turn = right_pkmn
                    if cursor.pos == vec(1, 1):
                        move(left_pkmn, right_pkmn, 4)
                        turn = right_pkmn
                elif two_battle_on and turn == right_pkmn:
                    if cursor.pos == vec(0, 0):
                        move(right_pkmn, left_pkmn, 1)
                        turn = left_pkmn
                    if cursor.pos == vec(1, 0):
                        move(right_pkmn, left_pkmn, 2)
                        turn = left_pkmn
                    if cursor.pos == vec(0, 1):
                        move(right_pkmn, left_pkmn, 3)
                        turn = left_pkmn
                    if cursor.pos == vec(1, 1):
                        move(right_pkmn, left_pkmn, 4)
                        turn = left_pkmn
                elif result_screen_on:
                    if cursor.pos == vec(0, 0):
                        left_pkmn.HP = left_pkmn.max_hp
                        right_pkmn.HP = right_pkmn.max_hp
                        result_screen_on = False
                        if last_played==2:
                            two_player_on = True
                        else:
                            one_player_on=True
                        cursor.pos = vec(0, 0)
                    if cursor.pos == vec(0, -1):
                        left_pkmn.HP = left_pkmn.max_hp
                        right_pkmn.HP = right_pkmn.max_hp
                        title_screen_on = True
                        result_screen_on = False
                        cursor.pos = vec(0, 0)
                    if cursor.pos == vec(0, -2):
                        result_screen_on = False
                        pg.quit()

# small function to be able to input a string and output it to the screen
def text_objects(text, font):
    textSurface = font.render(text, True, color_dark)
    return textSurface, textSurface.get_rect()

# function to find out which pokemon used a move and which pokemon to take health from
def move(pkmn1, pkmn2, movenum):
    if pkmn1.status == 'poison' and (7 * (pkmn1.max_hp // 8)) < pkmn1.HP:
        pkmn1.HP -= (1 / 8) * pkmn1.max_hp


    if movenum == 1:
        pkmn1.move1(pkmn2)
    if movenum == 2:
        pkmn1.move2(pkmn2)
    if movenum == 3:
        pkmn1.move3(pkmn2)
    if movenum == 4:
        pkmn1.move4(pkmn2)
    if pkmn1.type == 'status':
        pass

    else: # finding if a move is super effective or not very effective, will effect damage
        if pkmn2.pkmntype == "fire":
            if pkmn1.type == 'water':
                effectiveness = 2
            elif pkmn1.type == 'grass':
                effectiveness = 0.5
            else:
                effectiveness = 1
        elif pkmn2.pkmntype == "grass":
            if pkmn1.type == 'fire':
                effectiveness = 2
            elif pkmn1.type == 'water':
                effectiveness = 0.5
            else:
                effectiveness = 1
        elif pkmn2.pkmntype == "water":
            if pkmn1.type == 'grass':
                effectiveness = 2
            elif pkmn1.type == 'fire':
                effectiveness = 0.5
            else:
                effectiveness = 1
        else: # damage calculation, taken from the pokemon games
            effectiveness = 1
        pkmn2.HP -= int((((((200 / 5) + 2) * pkmn1.power * (pkmn1.atk_dam / pkmn2.defense_type)) / 50) + 2) * (
            random.randint(217, 255)) / 255) * effectiveness

# function of the title screen, with text and cursor and everything defined above
def title_screen():
    while title_screen_on:
        screen.fill(color_light)
        get_buttons()
        cursor.cursor_pos()
        titlesurf, titlerect = text_objects('Pokémon Game', bigfont)
        titlerect.center = ((width / 2), (height / 2 - 200))
        one_playersurf, one_playerrect = text_objects('1 Player(vs CPU)', smallfont)
        one_playerrect.center = ((width / 2), (height / 2 - 50))
        screen.blit(one_playersurf, one_playerrect)
        two_playersurf, two_playerrect = text_objects('2 Players', smallfont)
        two_playerrect.center = ((width / 2), (height / 2))
        screen.blit(two_playersurf, two_playerrect)
        screen.blit(titlesurf, titlerect)

        pg.display.update()

# function of the two player select screen
def two_player():
    global left_pkmn, right_pkmn
    while two_player_on:
        screen.fill(color_light)
        get_buttons()
        cursor.cursor_pos()

        if left_pkmn is None:
            titlesurf, titlerect = text_objects('P1 choose your Pokémon', bigfont)
            titlerect.center = ((width / 2), (height / 2 - 200))
            screen.blit(titlesurf, titlerect)

            Charizardsurf, Charizardrect = text_objects('Charizard', smallfont)
            Charizardrect.center = ((width / 2), (height / 2 + 100))
            charizard_img_rect = ((width / 2 - 60), (height / 2))
            screen.blit(charizard_img, charizard_img_rect)
            screen.blit(Charizardsurf, Charizardrect)

            Venusaursurf, Venusaurrect = text_objects('Venusaur', smallfont)
            Venusaurrect.center = ((width / 2 + 200), (height / 2 + 100))
            venusaur_img_rect = ((width / 2 + 165), (height / 2))
            screen.blit(venusaur_img, venusaur_img_rect)
            screen.blit(Venusaursurf, Venusaurrect)

            Blastoisesurf, Blastoiserect = text_objects('Blastoise', smallfont)
            Blastoiserect.center = ((width / 2 - 200), (height / 2 + 100))
            blastoise_img_rect = ((width / 2 - 235), (height / 2))
            screen.blit(Blastoisesurf, Blastoiserect)
            screen.blit(blastoise_img, blastoise_img_rect)
        else:
            titlesurf, titlerect = text_objects('P2 choose your Pokémon', bigfont)
            titlerect.center = ((width / 2), (height / 2 - 200))
            screen.blit(titlesurf, titlerect)
            if left_pkmn != charizard:
                Charizardsurf, Charizardrect = text_objects('Charizard', smallfont)
                Charizardrect.center = ((width / 2), (height / 2 + 100))
                charizard_img_rect = ((width / 2 - 60), (height / 2))
                screen.blit(charizard_img, charizard_img_rect)
                screen.blit(Charizardsurf, Charizardrect)
            if left_pkmn != venusaur:
                Venusaursurf, Venusaurrect = text_objects('Venusaur', smallfont)
                Venusaurrect.center = ((width / 2 + 200), (height / 2 + 100))
                venusaur_img_rect = ((width / 2 + 165), (height / 2))
                screen.blit(venusaur_img, venusaur_img_rect)
                screen.blit(Venusaursurf, Venusaurrect)
            if left_pkmn != blastoise:
                Blastoisesurf, Blastoiserect = text_objects('Blastoise', smallfont)
                Blastoiserect.center = ((width / 2 - 200), (height / 2 + 100))
                blastoise_img_rect = ((width / 2 - 235), (height / 2))
                screen.blit(Blastoisesurf, Blastoiserect)
                screen.blit(blastoise_img, blastoise_img_rect)


        pg.display.update()

# function for one player select pokemon screen
def one_player():
    while one_player_on:
        screen.fill(color_light)
        get_buttons()
        cursor.cursor_pos()
        titlesurf, titlerect = text_objects('Choose your Pokémon', bigfont)
        titlerect.center = ((width / 2), (height / 2 - 200))
        screen.blit(titlesurf, titlerect)

        Charizardsurf, Charizardrect = text_objects('Charizard', smallfont)
        Charizardrect.center = ((width / 2), (height / 2 + 100))
        charizard_img_rect = ((width / 2 - 60), (height / 2))
        screen.blit(charizard_img, charizard_img_rect)
        screen.blit(Charizardsurf, Charizardrect)

        Venusaursurf, Venusaurrect = text_objects('Venusaur', smallfont)
        Venusaurrect.center = ((width / 2 + 200), (height / 2 + 100))
        venusaur_img_rect = ((width / 2 + 165), (height / 2))
        screen.blit(venusaur_img, venusaur_img_rect)
        screen.blit(Venusaursurf, Venusaurrect)

        Blastoisesurf, Blastoiserect = text_objects('Blastoise', smallfont)
        Blastoiserect.center = ((width / 2 - 200), (height / 2 + 100))
        blastoise_img_rect = ((width / 2 - 235), (height / 2))
        screen.blit(Blastoisesurf, Blastoiserect)
        screen.blit(blastoise_img, blastoise_img_rect)
        pg.display.update()



# function for the one player battle screen
def one_player_battle():
    global turn, left_pkmn, right_pkmn, result_screen_on, one_battle_on, move_line1_rect, move_line1_surf, score
    while one_battle_on:
        now=pg.time.get_ticks()
        get_buttons()
        screen.fill(color_light)
        cursor.cursor_pos()
        pg.draw.rect(screen, color, (550, 30, 200, 25))
        pg.draw.rect(screen, color, (50, 30, 200, 25))
        if turn is None:
            turn = left_pkmn
        if left_pkmn.HP < 1: # win conditions, if health is 0
            result_screen_on = True
            one_battle_on = False
            turn = None
            score.y += 1
            last_played=1
        if right_pkmn.HP < 1:
            result_screen_on = True
            one_battle_on = False
            turn = None
            score.x += 1
            last_played=1
        if left_pkmn == blastoise:
            screen.blit(blastoise_fight_L, (100, 150))
            pg.draw.rect(screen, color_dark, (50, 30, 200 * blastoise.HP // blastoise.max_hp, 25))
        elif left_pkmn == charizard:
            screen.blit(charizard_fight_L, (25, 150))
            pg.draw.rect(screen, color_dark, (50, 30, 200 * charizard.HP // charizard.max_hp, 25))
        elif left_pkmn == venusaur:
            screen.blit(venusaur_fight_L, (100, 150))
            pg.draw.rect(screen, color_dark, (50, 30, 200 * venusaur.HP // venusaur.max_hp, 25))
        if right_pkmn == blastoise:
            screen.blit(blastoise_fight_R, (500, 150))
            pg.draw.rect(screen, color_dark, (550, 30, 200 * blastoise.HP // blastoise.max_hp, 25))
        if right_pkmn == venusaur:
            screen.blit(venusaur_fight_R, (500, 150))
            pg.draw.rect(screen, color_dark, (550, 30, 200 * venusaur.HP // venusaur.max_hp, 25))
        if right_pkmn == charizard:
            screen.blit(charizard_fight_R, (500, 150))
            pg.draw.rect(screen, color_dark, (550, 30, 200 * charizard.HP // charizard.max_hp, 25))
        if turn == left_pkmn:
            if left_pkmn == blastoise:
                move1surf, move1rect = text_objects('Hydro Pump', smallfont)
                move2surf, move2rect = text_objects('Aqua Ring', smallfont)
                move3surf, move3rect = text_objects('Withdraw', smallfont)
                move4surf, move4rect = text_objects('Bite', smallfont)


            elif left_pkmn == charizard:
                move1surf, move1rect = text_objects('Flamethrower', smallfont)
                move2surf, move2rect = text_objects('Dragon Claw', smallfont)
                move3surf, move3rect = text_objects('Iron Tail', smallfont)
                move4surf, move4rect = text_objects('Wing Attack', smallfont)


            elif left_pkmn == venusaur:
                move1surf, move1rect = text_objects('Solar Beam', smallfont)
                move2surf, move2rect = text_objects('Earthquake', smallfont)
                move3surf, move3rect = text_objects('Giga Drain', smallfont)
                move4surf, move4rect = text_objects('Poison Powder', smallfont)
            turnsurf, turnrect = text_objects('Player 1 Turn', smallfont)

        elif turn == right_pkmn and now-last_move>= cooldown: # giving a delay to the cpu's moves as to
            # give game a smoother feel
            # this is the computer brains, depending on the pokemon, it will act in certain ways
            if (right_pkmn.status == 'poison') and ((7 * (right_pkmn.max_hp // 8)) < right_pkmn.HP):
                right_pkmn.HP -= (1 / 8) * right_pkmn.max_hp
            if right_pkmn==charizard: # if charizard then be agressive, randomly choose attacking moves
                x=random.choice((1,2,3,4))
                move(right_pkmn, left_pkmn, x)
                turn = left_pkmn
            if right_pkmn==blastoise: # if blastoise then heal if low health
                if right_pkmn.HP/right_pkmn.max_hp <.4:
                    move(right_pkmn, left_pkmn, 2)
                    turn = left_pkmn
                elif left_pkmn==charizard: # if blastoise fighting charizard, use hydro pump always
                    move(right_pkmn, left_pkmn, 1)
                    turn = left_pkmn
                elif left_pkmn==venusaur: # if blastoise fighting venusaur, dont choose hydro pump, choose other moves
                    x=random.choice((3,4))
                    move(right_pkmn, left_pkmn, x)
                    turn = left_pkmn
                else:
                    x = random.choice((1,3, 4)) # else then randomly choose a move, not healing
                    move(right_pkmn, left_pkmn, x)
                    turn = left_pkmn
            if right_pkmn==venusaur:# if computer is venusaur then poison oppenent if not poisoned
                if right_pkmn.recharge is True:
                    right_pkmn.recharge=False
                    turn=left_pkmn
                elif left_pkmn.status != 'poison':
                    move(right_pkmn, left_pkmn, 4)
                    turn = left_pkmn
                else: # if opponent is poisoned then randomly choose a move
                    x=random.randint(1,3)
                    move(right_pkmn, left_pkmn, x)
                    turn = left_pkmn
            turnsurf, turnrect = text_objects('CPU Turn', smallfont)

        # displaying the name of each move depending on pokemon
        move1rect.center = (100, 550)
        screen.blit(move1surf, move1rect)

        move2rect.center = (350, 550)
        screen.blit(move2surf, move2rect)

        move3rect.center = (100, 600)
        screen.blit(move3surf, move3rect)

        move4rect.center = (350, 600)
        screen.blit(move4surf, move4rect)

        # displaying whose turn it is
        turnrect.center = (width // 2, 50)
        screen.blit(turnsurf, turnrect)

        # drawing the boxes around the text to give it a better look
        move_line1_rect.center = (650, 550)
        screen.blit(move_line1_surf, move_line1_rect)
        move_line2_rect.center = (650, 600)
        screen.blit(move_line2_surf, move_line2_rect)
        pg.draw.lines(screen, color_dark, True,
                      ((10, 495), (width - 10, 495), (width - 10, height - 10), (10, height - 10)), 5)
        pg.draw.lines(screen, color_dark, True, ((width // 2 + 50, 495), (width // 2 + 50, height - 10)), 5)
        pg.display.update()




# function for two player battle
def two_player_battle():
    global turn, left_pkmn, right_pkmn, result_screen_on, two_battle_on, move_line1_rect, move_line1_surf, score,last_played
    while two_battle_on:
        screen.fill(color_light)
        pg.draw.rect(screen, color, (550, 30, 200, 25))
        pg.draw.rect(screen, color, (50, 30, 200, 25))
        get_buttons()
        cursor.cursor_pos()
        if turn is None:
            turn = left_pkmn
        if left_pkmn.HP < 1: # win conditions, if health is 0
            result_screen_on = True
            two_battle_on = False
            turn = None
            last_played=2
            score.y += 1
        if right_pkmn.HP < 1:
            result_screen_on = True
            two_battle_on = False
            turn = None
            last_played = 2
            score.x += 1

            # displaying pokemon to the screen, facing certain directions depending on if on left or right
        if left_pkmn == blastoise:
            screen.blit(blastoise_fight_L, (100, 150))
            pg.draw.rect(screen, color_dark, (50, 30, 200 * blastoise.HP // blastoise.max_hp, 25))
        elif left_pkmn == charizard:
            screen.blit(charizard_fight_L, (25, 150))
            pg.draw.rect(screen, color_dark, (50, 30, 200 * charizard.HP // charizard.max_hp, 25))
        elif left_pkmn == venusaur:
            screen.blit(venusaur_fight_L, (100, 150))
            pg.draw.rect(screen, color_dark, (50, 30, 200 * venusaur.HP // venusaur.max_hp, 25))
        if right_pkmn == blastoise:
            screen.blit(blastoise_fight_R, (500, 150))
            pg.draw.rect(screen, color_dark, (550, 30, 200 * blastoise.HP // blastoise.max_hp, 25))
        if right_pkmn == venusaur:
            screen.blit(venusaur_fight_R, (500, 150))
            pg.draw.rect(screen, color_dark, (550, 30, 200 * venusaur.HP // venusaur.max_hp, 25))
        if right_pkmn == charizard:
            screen.blit(charizard_fight_R, (500, 150))
            pg.draw.rect(screen, color_dark, (550, 30, 200 * charizard.HP // charizard.max_hp, 25))

        #displaying moves depending on whose turn it is at that moment
        if turn == left_pkmn:
            if left_pkmn == blastoise:
                move1surf, move1rect = text_objects('Hydro Pump', smallfont)
                move2surf, move2rect = text_objects('Aqua Ring', smallfont)
                move3surf, move3rect = text_objects('Withdraw', smallfont)
                move4surf, move4rect = text_objects('Bite', smallfont)


            elif left_pkmn == charizard:
                move1surf, move1rect = text_objects('Flamethrower', smallfont)
                move2surf, move2rect = text_objects('Dragon Claw', smallfont)
                move3surf, move3rect = text_objects('Iron Tail', smallfont)
                move4surf, move4rect = text_objects('Wing Attack', smallfont)


            elif left_pkmn == venusaur:
                move1surf, move1rect = text_objects('Solar Beam', smallfont)
                move2surf, move2rect = text_objects('Earthquake', smallfont)
                move3surf, move3rect = text_objects('Giga Drain', smallfont)
                move4surf, move4rect = text_objects('Poison Powder', smallfont)
            turnsurf, turnrect = text_objects('Player 1 Turn', smallfont)

        elif turn == right_pkmn:
            if right_pkmn == blastoise:
                move1surf, move1rect = text_objects('Hydro Pump', smallfont)
                move2surf, move2rect = text_objects('Aqua Ring', smallfont)
                move3surf, move3rect = text_objects('Withdraw', smallfont)
                move4surf, move4rect = text_objects('Bite', smallfont)


            elif right_pkmn == charizard:
                move1surf, move1rect = text_objects('Flamethrower', smallfont)
                move2surf, move2rect = text_objects('Dragon Claw', smallfont)
                move3surf, move3rect = text_objects('Iron Tail', smallfont)
                move4surf, move4rect = text_objects('Wing Attack', smallfont)


            elif right_pkmn == venusaur:
                move1surf, move1rect = text_objects('Solar Beam', smallfont)
                move2surf, move2rect = text_objects('Earthquake', smallfont)
                move3surf, move3rect = text_objects('Giga Drain', smallfont)
                move4surf, move4rect = text_objects('Poison Powder', smallfont)
            turnsurf, turnrect = text_objects('Player 2 Turn', smallfont)


        move1rect.center = (100, 550)
        screen.blit(move1surf, move1rect)

        move2rect.center = (350, 550)
        screen.blit(move2surf, move2rect)

        move3rect.center = (100, 600)
        screen.blit(move3surf, move3rect)

        move4rect.center = (350, 600)
        screen.blit(move4surf, move4rect)

        # displaying whose turn it is
        turnrect.center = (width // 2, 50)
        screen.blit(turnsurf, turnrect)

        # displaying what move was used last
        move_line1_rect.center = (650, 550)
        screen.blit(move_line1_surf, move_line1_rect)
        move_line2_rect.center = (650, 600)
        screen.blit(move_line2_surf, move_line2_rect)

        # drawing boxes around moves to make screen look better
        pg.draw.lines(screen, color_dark, True,
                      ((10, 495), (width - 10, 495), (width - 10, height - 10), (10, height - 10)), 5)
        pg.draw.lines(screen, color_dark, True, ((width // 2 + 50, 495), (width // 2 + 50, height - 10)), 5)
        pg.display.update()

# result screen for when win condition is met
def result_screen():
    global result_screen_on, score, left_pkmn, right_pkmn
    cursor.pos=vec(0,0)
    while result_screen_on:
        get_buttons()
        screen.fill(color_light)
        cursor.cursor_pos()
        if left_pkmn.HP < 1:
            if right_pkmn == charizard:
                winsurf, winrect = text_objects(f'P2 Charizard won!!', bigfont)
            elif right_pkmn == blastoise:
                winsurf, winrect = text_objects(f'P2 Blastoise won!!', bigfont)
            elif right_pkmn == venusaur:
                winsurf, winrect = text_objects('P2 Venusaur won!!', bigfont)


        elif right_pkmn.HP < 1:

            if left_pkmn == charizard:
                winsurf, winrect = text_objects(f'P1 Charizard won!!', bigfont)
            elif left_pkmn == blastoise:
                winsurf, winrect = text_objects(f'P1 Blastoise won!!', bigfont)
            elif left_pkmn == venusaur:
                winsurf, winrect = text_objects('P1 Venusaur won!!', bigfont)
        winrect.center = ((width // 2), (height // 2 - 200))
        screen.blit(winsurf, winrect)

        # displaying the score
        scoresurf, scorerect = text_objects(f'{int(score.x)}-{int(score.y)}', bigfont)
        scorerect.center = ((width // 2), (height // 2 - 100))
        screen.blit(scoresurf, scorerect)

        #displaying buttons
        againsurf, againrect = text_objects('Play Again', smallfont)
        againrect.center = ((width // 2), (height // 2))
        screen.blit(againsurf, againrect)
        modesurf, moderect = text_objects('Change Modes', smallfont)
        moderect.center = ((width // 2), (height // 2 + 50))
        screen.blit(modesurf, moderect)
        quitsurf, quitrect = text_objects('Quit Game', smallfont)
        quitrect.center = ((width // 2), (height // 2 + 100))
        screen.blit(quitsurf, quitrect)
        pg.display.update()

    # resetting which pokemon is which
    left_pkmn = None
    right_pkmn = None

# some more variables to control which screen to display
run = True
title_screen_on = True
two_player_on = False
one_player_on = False
one_battle_on = False
two_battle_on = False
result_screen_on = False

# naming classes
cursor = Cursor()
blastoise = Blastoise()
charizard = Charizard()
venusaur = Venusaur()
# main while loop that runs all code above... a lot of work for this lol
while run:
    title_screen()
    two_player()
    one_player()
    two_player_battle()
    one_player_battle()
    result_screen()
