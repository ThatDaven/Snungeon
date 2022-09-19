'''Dependencies file with constants and game classes'''


import pygame
from sys import exit
from random import choice, randint, random


pygame.init()

SCREEN_W = 720
SCREEN_H = 480
BG_COLOUR = 'grey10'
FRAME_RATE = 60

FONT = pygame.font.Font('lol font.ttf', 20)

SOUND_SELECT = pygame.mixer.Sound('audios/select.wav')
SOUND_CONFIRM = pygame.mixer.Sound('audios/confirm.ogg')
SOUND_TAKE_ITEM = pygame.mixer.Sound('audios/take_item.wav')

WEAPON_NAME = ('Sword', 'Staff', 'Shuriken', 'Broomstick', 'Knife', 'Pan', 'Glass Bottle')
WEAPON_ADJ = ('Thunderous', 'Unstoppable', 'Piercing', 'Formidable', 'Inconceivable')
WEAPON_END = ('Power', 'Vengeance', 'Strength', 'Bravery', 'Courage', 'Soul', 'Space', 'Mind', 'Time', 'Reality', 'Death', 'Life')
ARMOUR_NAME = ('Shield', 'Wall', 'Pillow', 'Turtle Shell', 'Car Door')
ARMOUR_ADJ = ('Iron', 'Unbreakable', 'Mighty', 'Unweilding', 'Defensive')
ARMOUR_END = ('Defence', 'Safety', 'Might', 'Protection', 'Prowess')
ENEMY_NAME = ('Goblin', 'Ogre', 'Pixie', 'Goomba', 'Gremlin')
ENEMY_ADJ = ('Stinky', 'Green', 'Mischievious', 'Naughty', 'Short', 'Ugly', 'Cruel', 'Slimy', 'Evil')


class Player:
    '''Player class with all player details'''

    def __init__(self):
        self.skill_points = 35
        self.atk = 1
        self.hp = 1
        self.maxhp = self.hp
        self.defence = 1
        self.weapon = None
        self.armour = None
        self.level = 0

    @property
    def hp(self):
        '''Property decorator as hp has to update maxhp'''
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        self.max_hp = self._hp

    @property
    def sum(self):
        '''Sum of all skills'''
        return self.atk + self.hp + self.defence

    def change_hp(self, change):
        '''Changes the hp'''
        self._hp += change
        if self._hp > self.max_hp: self._hp = self.max_hp


class SpriteSheet:
    '''
    Class for working with sprite sheets
    i love you <3'''

    def __init__(self, spritesheet):
        self.sheet = pygame.image.load('{}.png'.format(spritesheet)).convert_alpha()

    def get_image(self, rect):
        '''Extraction of sprite using rect as position, offset, etc...'''

        image = pygame.Surface((rect[2], rect[3])).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey('#000000')  # Make the surface transparent

        return image


BATTLE_DICTS = {
    'fight': [0, 0, 32, 32],
    'sharpen': [32, 0, 32, 32],
    'defend': [64, 0, 32, 32],
    'heal': [96, 0, 32, 32],
}
ENEMY_DICTS = {
    'Goblin': [0, 0, 64, 64],
    'Ogre': [64, 0, 64, 64],
    'Pixie': [128, 0, 64, 64],
    'Goomba': [192, 0, 64, 64],
    'Gremlin': [256, 0, 64, 64],
}
WEAPON_DICTS = {
    'Sword': [0, 0, 16, 16],
    'Staff': [16, 0, 16, 16],
    'Knife': [32, 0, 16, 16],
    'Glass Bottle': [48, 0, 16, 16],
    'Broomstick': [64, 0, 16, 16],
    'Pan': [80, 0, 16, 16],
    'Shuriken': [96, 0, 16, 16]
}
ARMOUR_DICTS = {
    'Shield': [0, 0, 16, 16],
    'Wall': [16, 0, 16, 16],
    'Pillow': [32, 0, 16, 16],
    'Turtle Shell': [48, 0, 16, 16],
    'Car Door': [64, 0, 16, 16],
}


class BlankRoom(pygame.sprite.Sprite):
    '''A blank room; only to be inherited by other rooms'''

    def __init__(self, image, pos, name, desc):
        super().__init__()
        self.image = pygame.image.load('{}.png'.format(image)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.name = name
        self.desc = desc

    def select(self):
        '''Selects the room for selection'''

        if self.image.get_height() == 128:
            pos = self.rect.center
            self.image = pygame.transform.scale(self.image, (192, 192))
            self.rect = self.image.get_rect()
            self.rect.center = pos

    def deselect(self):
        '''Deselects the room for selection'''

        if self.image.get_height() != 128:
            pos = self.rect.center
            self.image = pygame.transform.scale(self.image, (128, 128))
            self.rect = self.image.get_rect()
            self.rect.center = pos


class HealRoom(BlankRoom):
    '''Increases player health'''

    def __init__(self, pos):
        super().__init__('assets/healroom', pos, 'HEAL ROOM', 'A calming place to replenish your soul.\n\nEnter?')


class EnemyRoom(BlankRoom):
    '''Loads an enemy for the player to fight'''

    def __init__(self, pos):
        super().__init__('assets/enemyroom', pos, 'ENEMY ROOM', 'Is the risk worth the reward?\n\nEnter?')


class ChestRoom(BlankRoom):
    '''Generates a random item for the player to collect'''

    def __init__(self, pos):
        super().__init__('assets/chestroom', pos, 'CHEST ROOM', 'Where you can safely find treasure.\n\nEnter?')


class BoostRoom(BlankRoom):
    '''Increases a player skill'''

    def __init__(self, pos):
        super().__init__('assets/boostroom', pos, 'BOOST ROOM', 'A rare sight very few heros come across. Legend has it you become much stronger after entering!\n\nEnter?')


ROOMS = (HealRoom, EnemyRoom, ChestRoom)

def gen_random_rooms():
    '''Generates random tuple of three rooms'''

    rooms = (
        choice(ROOMS)((SCREEN_W/4-45, SCREEN_H/3)),
        choice(ROOMS)((SCREEN_W/4*2, SCREEN_H/3)),
        choice(ROOMS)((SCREEN_W/4*3+45, SCREEN_H/3))
    )

    if round(random(), 2) <= 1/100:
        rooms = (
            choice(ROOMS)((SCREEN_W/4-45, SCREEN_H/3)),
            BoostRoom((SCREEN_W/4*2, SCREEN_H/3)),
            choice(ROOMS)((SCREEN_W/4*3+45, SCREEN_H/3))
        )
    return rooms


class Text:
    '''Class for text animation'''

    def __init__(self, display, text, *, max_size=None, speed=0.5, pos=(60, 360)):
        if max_size is None: self.max_size = (SCREEN_W/4*3, SCREEN_H/4)
        self.display = display
        self.text = text
        self.frame = 0
        self.speed = speed
        self.pos = pos
        self.lines = [{'text': '', 'x': self.pos[0], 'y': self.pos[1]}]
        self.c_line = 0
        self.height = FONT.size('Hello, World!')[1]

    def update(self):
        '''Updates amount of text visible'''

        if self.frame == len(self.text):
            return

        if int(self.frame) == self.frame:
            # Newline if newline
            if self.text[int(self.frame)] == '\n':
                self.c_line += 1
                self.lines.append({'text': '', 'x': self.pos[0], 'y': self.pos[1]+self.height*self.c_line})

                self.frame += self.speed
                return

            self.t_text = self.lines[self.c_line]['text'] + self.text[int(self.frame)]

            # Checking if the text goes out of bounds
            if FONT.size(self.t_text)[0] > self.max_size[0]:
                split_text = self.lines[self.c_line]['text'].split(' ')
                last_word = split_text[-1]
                split_text.pop()
                self.lines[self.c_line]['text'] = ' '.join(split_text)
                self.c_line += 1
                self.lines.append({'text': last_word+self.text[int(self.frame)], 'x': self.pos[0], 'y': self.pos[1]+self.height*self.c_line})
            else:
                self.lines[self.c_line]['text'] += self.text[int(self.frame)]

        self.frame += self.speed

    def skip(self):
        '''Function for skipping the text animation'''

        # Calls update function until all text is visible
        for _ in range(len(self.text)*self.speed):
            self.update()

    def draw(self):
        '''Function for displaying the text'''

        for line in self.lines:
            self.display.blit(FONT.render(line['text'], True, 'grey95'), (line['x'], line['y']))

    def change_text(self, new_text):
        '''Function for changing the text'''

        self.text = new_text
        self.frame = 0
        self.lines = [{'text': '', 'x': self.pos[0], 'y': self.pos[1]}]
        self.c_line = 0


class Animation:
    '''
    Class for semi-okay animation
    i love you so much, you solved everything'''

    def __init__(self, frames, pixels):
        self.frames = frames
        self.int_sum = self.frames*(self.frames+1)/2
        self.ppixel = pixels/self.int_sum

    def get_move(self, frame, reverse=True):
        '''Returns the pixel movement per frame'''

        if reverse: return round((self.frames-frame)*self.ppixel)
        else: return round(frame*self.ppixel)


class Scene:
    '''Class for a basic scene able to be run'''

    def __init__(self, display, sprites, player):
        self.display = display
        self.player = player
        self.ui = pygame.sprite.Group()
        self.running = True

        for sprite in sprites:
            self.ui.add(sprite)

    def update_display(self):
        '''Draws everything in the UI group'''
        self.ui.draw(self.display)

    def get_events(self):
        '''Control all user input (events)'''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def run(self):
        '''Run each frame by the PyGame loop'''

        if not self.running:
            return True

        self.get_events()
        self.update_display()


class TitleScene(Scene):
    '''Scene for the title screen'''

    def __init__(self, display, player):
        super().__init__(display, (), player)

        self.choice = 0
        self.choices = ('Story', 'Endless', 'Controls')
        self.scene = 0

        text = 'This game only requires the keys WASD and ENTER (RETURN) to play\n' \
            '- Navigate through the UI with the WASD keys\n- Press ENTER (RETURN) to interact with buttons and confirm choices\n' \
            'Any thing that is YELLOW or has a YELLOW border means it is selected\n\n' \
            'Any text with ">>" requires the key ENTER (RETURN) to be pressed to continue\n(You can also press the X key to skip the text animation)'
        self.text = Text(self.display, text, speed=1, pos=(60, 144))

    def update_display(self):
        if self.scene == 0:
            font_size = FONT.size('DUNGEON PROJECT')
            self.display.blit(FONT.render('DUNGEON PROJECT', True, 'grey95'), (360-font_size[0]/2, 96-font_size[1]/2))

            for choice, pos in zip(self.choices, ((360, 192), (360, 288), (360, 384))):
                font_size = FONT.size(choice)

                if self.choices[self.choice] == choice:
                    self.display.blit(FONT.render(choice, True, '#FFFF00'), (pos[0]-font_size[0]/2, pos[1]-font_size[1]/2))
                else:
                    self.display.blit(FONT.render(choice, True, 'grey95'), (pos[0]-font_size[0]/2, pos[1]-font_size[1]/2))

        elif self.scene == 1:
            font_size = FONT.size('CONTROLS')
            self.display.blit(FONT.render('CONTROLS', True, 'grey95'), (360-font_size[0]/2, 96-font_size[1]/2))

            self.text.update()
            self.text.draw()

            font_size = FONT.size('Go back')
            self.display.blit(FONT.render('Go back', True, '#FFFF00'), (360-font_size[0]/2, 384-font_size[1]/2))

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if self.scene == 0:
                    # Controls the changing choices
                    if event.key == pygame.K_w:
                        pygame.mixer.Sound.play(SOUND_SELECT)
                        if self.choice != 0:
                            self.choice -= 1
                    if event.key == pygame.K_s:
                        pygame.mixer.Sound.play(SOUND_SELECT)
                        if self.choice != len(self.choices)-1:
                            self.choice += 1
                    # Next scene
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.Sound.play(SOUND_CONFIRM)
                        if self.choices[self.choice] != 'Controls':
                            self.running = False
                        else:
                            self.scene = 1
                elif self.scene == 1:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.Sound.play(SOUND_CONFIRM)
                        self.text.skip()
                        self.scene = 0
                    if event.key == pygame.K_x:
                        self.text.skip()

    def run(self):
        if not self.running:
            return self.choices[self.choice]

        self.get_events()
        self.update_display()


class NameScene(Scene):
    '''
    Scene for (useless) name selection
    This was also unreasonably hard >:(
    no but fr this was the hardest part of the whole game'''

    def __init__(self, display, player):
        super().__init__(display, (), player)

        self.y_choice = 0
        self.x_choice = 0
        self.choices = (
            tuple('ABCDEFGHIJKLMN'),
            tuple('OPQRSTUVWXYZ'),
            ('Backspace', 'Continue')
        )
        self.scene = 0
        self.name_index = 0
        self.useless_name = list('________')

        self.confirm = 0
        self.ee2 = False

    def update_display(self):
        if self.scene == 0:
            self.ee2 = False

            font_size = FONT.size(''.join(self.useless_name))
            self.display.blit(FONT.render(''.join(self.useless_name), True, 'grey95'), (360-font_size[0]/2, 96-font_size[1]/2))

            for y, row in enumerate(self.choices):
                for x, choice_ in enumerate(row):
                    if choice_ == 'Continue':
                        x = 11.25  # this gonna reduce my lifespan by 10 years

                    if self.choices[self.y_choice][self.x_choice] == choice_:
                        self.display.blit(FONT.render(choice_, True, '#FFFF00'), (90+x*48-font_size[0]/2, 192+y*48-font_size[1]/2))
                    else:
                        self.display.blit(FONT.render(choice_, True, 'grey95'), (90+x*48-font_size[0]/2, 192+y*48-font_size[1]/2))

        elif self.scene == 1:
            if not ''.join(self.useless_name).replace('_', '') and not self.ee2:
                message = ('No Name', 'Unnamed Idiot', 'Are you dumb?', 'Name?', 'Guess your parents didn\'t love you enough to give you a name', 'Can\'t read?', 'ooo who\'s this?', 'hi,     !', 'D U M B', 'y r u dumb', 'You\'re a mistake')
                self.name = choice(message)
                self.ee2 = True
            elif ''.join(self.useless_name).replace('_', ''):
                self.ee2 = False
                self.name = ''.join(self.useless_name).replace('_', '')
            font_size = FONT.size(self.name)
            self.display.blit(FONT.render(self.name, True, 'grey95'), (360-font_size[0]/2, 96-font_size[1]/2))


            if not ''.join(self.useless_name).replace('_', ''):
                font_size = FONT.size('Go back')
                self.display.blit(FONT.render('Go back', True, '#FFFF00'), (240-font_size[0]/2, 384-font_size[1]/2))
                self.confirm = 0
                return

            if self.confirm == 0:
                font_size = FONT.size('Go back')
                self.display.blit(FONT.render('Go back', True, '#FFFF00'), (240-font_size[0]/2, 384-font_size[1]/2))
                font_size = FONT.size('Continue')
                self.display.blit(FONT.render('Continue', True, 'grey95'), (480-font_size[0]/2, 384-font_size[1]/2))
            elif self.confirm == 1:
                font_size = FONT.size('Go back')
                self.display.blit(FONT.render('Go back', True, 'grey95'), (240-font_size[0]/2, 384-font_size[1]/2))
                font_size = FONT.size('Continue')
                self.display.blit(FONT.render('Continue', True, '#FFFF00'), (480-font_size[0]/2, 384-font_size[1]/2))

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if self.scene == 0:
                    # Controls the changing characters
                    if event.key == pygame.K_w:
                        pygame.mixer.Sound.play(SOUND_SELECT)
                        if self.y_choice != 0:
                            self.y_choice -= 1
                    if event.key == pygame.K_s:  # just kill me already
                        pygame.mixer.Sound.play(SOUND_SELECT)
                        if self.y_choice != len(self.choices)-1:
                            if self.x_choice > len(self.choices[self.y_choice+1])-1:
                                self.x_choice = len(self.choices[self.y_choice+1])-1
                            self.y_choice += 1
                    if event.key == pygame.K_a:
                        pygame.mixer.Sound.play(SOUND_SELECT)
                        if self.x_choice != 0:
                            self.x_choice -= 1
                        else:
                            self.x_choice = len(self.choices[self.y_choice])-1
                    if event.key == pygame.K_d:
                        pygame.mixer.Sound.play(SOUND_SELECT)
                        if self.x_choice != len(self.choices[self.y_choice])-1:
                            self.x_choice += 1
                        else:
                            self.x_choice = 0
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.Sound.play(SOUND_CONFIRM)
                        if self.choices[self.y_choice][self.x_choice] == 'Backspace':
                            self.useless_name[self.name_index-1] = '_'
                            if self.name_index != 0:
                                self.name_index -= 1
                        elif self.choices[self.y_choice][self.x_choice] == 'Continue':
                            self.scene = 1
                        else:
                            if self.name_index != 8:
                                self.useless_name[self.name_index] = self.choices[self.y_choice][self.x_choice]
                                self.name_index += 1
                elif self.scene == 1:
                    if event.key == pygame.K_a:
                        pygame.mixer.Sound.play(SOUND_SELECT)
                        if self.confirm != 0:
                            self.confirm -= 1
                        else:
                            self.confirm = 1
                    if event.key == pygame.K_d:
                        pygame.mixer.Sound.play(SOUND_SELECT)
                        if self.confirm != 1:
                            self.confirm += 1
                        else:
                            self.confirm = 0
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.Sound.play(SOUND_CONFIRM)
                        if self.confirm == 0:
                            self.scene = 0
                        elif self.confirm == 1:
                            self.running = False


class Skill:
    '''Class for player skills'''

    def __init__(self, display, player, pos, skill, image):
        self.display = display
        self.player = player
        self.pos = pos
        self.skill = skill
        self.amount = getattr(self.player, self.skill)
        self.image = pygame.image.load('{}.png'.format(image)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (180, 120))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update_display(self):
        self.amount = getattr(self.player, self.skill)
        self.display.blit(self.image, self.rect)
        font_size = FONT.size(str(self.amount))
        self.display.blit(FONT.render(str(self.amount), True, 'grey95'), (self.pos[0]-font_size[0]/2, self.pos[1]-font_size[1]/2))


class SkillScene(Scene):
    '''Scene for changing the player skills'''

    def __init__(self, display, player):
        super().__init__(display, (), player)

        self.player = player
        self.choice = 0
        self.choices = (
            Skill(self.display, self.player, (SCREEN_W/4-45, SCREEN_H/3), 'atk', 'assets/attackskill'),
            Skill(self.display, self.player, (SCREEN_W/4*2, SCREEN_H/3), 'hp', 'assets/healthskill'),
            Skill(self.display, self.player, (SCREEN_W/4*3+45, SCREEN_H/3), 'defence', 'assets/defenceskill'),
        )
        self.border = pygame.image.load('assets/skillborder.png').convert_alpha()
        self.border = pygame.transform.scale(self.border, (192, 132))
        self.border_rect = self.border.get_rect()
        self.border_rect.center = self.choices[0].rect.center

        text = 'Select your skills, make sure to use them all!\n' \
            'Navigate through the skills using the WASD keys:\n- W/S to increase/decrease\n- A/D to move left/right\n\n' \
            'Press ENTER when ready'
        self.text = Text(self.display, text, speed=1, pos=(60, 270))

        self.ee1 = False

    def update_display(self):
        for skill in self.choices:
            skill.update_display()

        # Moves the border to the current pos
        if self.border_rect.centerx > self.choices[self.choice].rect.centerx:
            self.border_rect.centerx -= 15
        elif self.border_rect.centerx < self.choices[self.choice].rect.centerx:
            self.border_rect.centerx += 15
        # self.border_rect.center = self.choices[self.choice].rect.center
        self.display.blit(self.border, self.border_rect)

        # Text business
        if not self.ee1:
            self.sp_text = 'You have {} skill points remaining'.format(self.player.skill_points-self.player.sum)
        font_size = FONT.size(self.sp_text)
        self.display.blit(FONT.render(self.sp_text, True, 'grey95'), (360-font_size[0]/2, 48-font_size[1]/2))

        self.text.update()
        self.text.draw()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.ee1 = False

                # Controls the changing of skill
                if event.key == pygame.K_a:
                    pygame.mixer.Sound.play(SOUND_SELECT)
                    if self.choice != 0:
                        self.choice -= 1
                if event.key == pygame.K_d:
                    pygame.mixer.Sound.play(SOUND_SELECT)
                    if self.choice != len(self.choices)-1:
                        self.choice += 1
                # Controls the changing of skill amount
                if event.key == pygame.K_w:
                    pygame.mixer.Sound.play(SOUND_SELECT)
                    setattr(self.player, self.choices[self.choice].skill, getattr(self.player, self.choices[self.choice].skill)+1)
                    if self.player.sum > self.player.skill_points:
                        setattr(self.player, self.choices[self.choice].skill, getattr(self.player, self.choices[self.choice].skill)-1)
                        self.sp_text = choice(('You think you have any skill points left to spend?', 'With what skill points?', 'nah', 'no.', 'Keep trying.', 'uh oh, 0 left', 'L', ':clown:', 'ZERO LOL IMAGINE', 'no skill points'))
                        self.ee1 = True
                if event.key == pygame.K_s:
                    pygame.mixer.Sound.play(SOUND_SELECT)
                    if getattr(self.player, self.choices[self.choice].skill) > 1:
                        setattr(self.player, self.choices[self.choice].skill, getattr(self.player, self.choices[self.choice].skill)-1)
                    else:
                        self.sp_text = choice(('Really?', '...', '?', 'How?', 'Keep trying.', 'how does that work, eh?'))
                        self.ee1 = True
                if event.key == pygame.K_x:
                    self.text.skip()
                # Next scene
                if event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(SOUND_CONFIRM)
                    self.running = False


class SelectionScene(Scene):
    '''Scene only for selection of multiple choices'''

    def __init__(self, display, choices, player):
        super().__init__(display, choices, player)

        self.c_choice = 0
        self.o_choice = 0
        self.choices = choices
        self.text = Text(self.display, '', speed=1, pos=(60, 320))
        self.not_loaded = True

    def update_display(self):
        o_sprite = self.choices[self.o_choice]
        c_sprite = self.choices[self.c_choice]

        # Resets old choice and sets new choice
        o_sprite.deselect()
        c_sprite.select()

        self.ui.draw(self.display)

        # Text business
        if self.not_loaded:
            self.text.change_text('{}\n{}'.format(c_sprite.name, c_sprite.desc))
            self.not_loaded = False

        self.text.update()
        self.text.draw()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Controls the changing of selection
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pygame.mixer.Sound.play(SOUND_SELECT)
                    if self.c_choice != 0:
                        self.o_choice = self.c_choice
                        self.c_choice -= 1
                        self.not_loaded = True
                if event.key == pygame.K_d:
                    pygame.mixer.Sound.play(SOUND_SELECT)
                    if self.c_choice != len(self.choices)-1:
                        self.o_choice = self.c_choice
                        self.c_choice += 1
                        self.not_loaded = True
                if event.key == pygame.K_x:
                    self.text.skip()
                # Entering a room
                if event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(SOUND_CONFIRM)
                    self.running = False

    def run(self):
        if not self.running:
            return self.choices[self.c_choice].name

        self.get_events()
        self.update_display()


class HealScene(Scene):
    '''Scene for the heal room'''

    def __init__(self, display, player):
        super().__init__(display, (), player)

        self.heal_sprite = pygame.image.load('assets/healsprite.png').convert_alpha()
        self.heal_rect = self.heal_sprite.get_rect()
        self.heal_rect.center = 360, 120

        if player.hp != player.max_hp:
            self.heal_amount = randint(int(self.player.max_hp*0.5), int(self.player.max_hp*0.75))
            self.player.change_hp(self.heal_amount)
            text = 'The peaceful pond replenishes your soul\n\nYou regain {} HP!\n({}/{})'.format(self.heal_amount, self.player.hp, self.player.maxhp)
        else:
            text = 'The sight of the peaceful pond would replenish your soul...\n' \
                'However, this sight does not satisfy your greedy soul and thus you gained nothing\n\n' \
                'You gained 0 HP!\n\n>>'

        self.text = Text(self.display, text, speed=1, pos=(60, 192))

    def update_display(self):
        self.display.blit(self.heal_sprite, self.heal_rect)

        self.text.update()
        self.text.draw()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.text.frame == len(self.text.text):
                        pygame.mixer.Sound.play(SOUND_CONFIRM)
                        self.running = False
                if event.key == pygame.K_x:
                    self.text.skip()



class FightIcon(pygame.sprite.Sprite):
    '''Icon class for battle'''

    def __init__(self, b_spritesheet, icon, pos):
        super().__init__()
        self.image = b_spritesheet.get_image(BATTLE_DICTS[icon]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def select(self):
        '''Selects the icon for selection'''

        if self.image.get_height() == 64:
            pos = self.rect.center
            self.image = pygame.transform.scale(self.image, (96, 96))
            self.rect = self.image.get_rect()
            self.rect.center = pos

    def deselect(self):
        '''Deselects the icon for selection'''

        if self.image.get_height() != 64:
            pos = self.rect.center
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.rect = self.image.get_rect()
            self.rect.center = pos


class EnemyScene(Scene):
    'Scene for enemy room'

    def __init__(self, display, player, e_spritesheet, b_spritesheet, type_=None):
        super().__init__(display, (), player)

        self.screen = pygame.Surface((SCREEN_W, SCREEN_H))

        # bruh ctrl-c and ctrl-v
        self.fight_icon = FightIcon(b_spritesheet, 'fight', (-216, 384))
        self.sharpen_icon = FightIcon(b_spritesheet, 'sharpen', (-72, 384))
        self.defend_icon = FightIcon(b_spritesheet, 'defend', (792, 384))
        self.heal_icon = FightIcon(b_spritesheet, 'heal', (936, 384))

        self.extra_atk = 1
        self.extra_def = 1
        self.heals = 5

        self.enemy = choice(ENEMY_NAME)
        self.enemy_image = e_spritesheet.get_image(ENEMY_DICTS[self.enemy]).convert_alpha()
        self.enemy_image = pygame.transform.scale(self.enemy_image, (96, 96))
        self.enemy_rect = self.enemy_image.get_rect()
        self.enemy_rect.center = 360, 120

        self.type_ = type_

        self.enemy_hp = randint(2*(self.player.level+1), 5*(self.player.level+1))
        self.enemy_def = randint(2*(self.player.level+1), 5*(self.player.level+1))
        if self.type_ == 'boss':
            self.enemy_hp *= randint(2, 5)
            self.enemy_def *= randint(2, 5)
        if self.type_ == 'final':
            # just get better smh
            self.enemy_hp *= randint(4, 7)
            self.enemy_def *= randint(4, 7)
        
        self.c_choice = 0
        self.o_choice = 0
        self.choices = [self.fight_icon, self.sharpen_icon, self.defend_icon, self.heal_icon]

        self.scene = 0

        self.anim = Animation(25, 360)
        self.frame = 0
        self.shake = 50

        self.screen_pos = [0, 0]

        if type_ == 'boss': self.text = Text(self.screen, 'BOSS BATTLE\nThe {} blocks your way!\n\n>>'.format(self.enemy), speed=1, pos=(60, 320))
        elif type_ == 'final': self.text = Text(self.screen, 'THE FINAL BOSS BATTLE\nThe {} blocks your way!\n\n>>'.format(self.enemy), speed=1, pos=(60, 320))
        else: self.text = Text(self.screen, 'The {} blocks your way!\n\n>>'.format(self.enemy), speed=1, pos=(60, 320))

    def update_display(self):
        self.screen.fill(BG_COLOUR)
        if self.scene == 0:
            self.screen.blit(self.enemy_image, self.enemy_rect)

            self.text.update()
            self.text.draw()
        elif self.scene == 0.5:
            self.fight_icon.rect.centerx += self.anim.get_move(self.frame)
            self.sharpen_icon.rect.centerx += self.anim.get_move(self.frame)
            self.defend_icon.rect.centerx -= self.anim.get_move(self.frame)
            self.heal_icon.rect.centerx -= self.anim.get_move(self.frame)

            self.screen.blit(self.enemy_image, self.enemy_rect)
            self.screen.blit(self.fight_icon.image, self.fight_icon.rect)
            self.screen.blit(self.sharpen_icon.image, self.sharpen_icon.rect)
            self.screen.blit(self.defend_icon.image, self.defend_icon.rect)
            self.screen.blit(self.heal_icon.image, self.heal_icon.rect)

            self.frame += 1
            if self.frame > 25:
                self.frame = 0
                self.scene = 1
        elif self.scene == 1:
            o_sprite = self.choices[self.o_choice]
            c_sprite = self.choices[self.c_choice]

            o_sprite.deselect()
            c_sprite.select()

            self.screen.blit(self.enemy_image, self.enemy_rect)
            self.screen.blit(self.fight_icon.image, self.fight_icon.rect)
            self.screen.blit(self.sharpen_icon.image, self.sharpen_icon.rect)
            self.screen.blit(self.defend_icon.image, self.defend_icon.rect)
            self.screen.blit(self.heal_icon.image, self.heal_icon.rect)
        elif self.scene == 2:
            self.fight_icon.rect.centerx -= self.anim.get_move(self.frame, False)
            self.sharpen_icon.rect.centerx -= self.anim.get_move(self.frame, False)
            self.defend_icon.rect.centerx += self.anim.get_move(self.frame, False)
            self.heal_icon.rect.centerx += self.anim.get_move(self.frame, False)

            self.screen.blit(self.enemy_image, self.enemy_rect)
            self.screen.blit(self.fight_icon.image, self.fight_icon.rect)
            self.screen.blit(self.sharpen_icon.image, self.sharpen_icon.rect)
            self.screen.blit(self.defend_icon.image, self.defend_icon.rect)
            self.screen.blit(self.heal_icon.image, self.heal_icon.rect)

            self.frame += 1
            if self.frame > 25:
                self.frame = 0
                self.scene += 1
        elif self.scene == 3:
            if self.c_choice == 0:
                self.enemy_image.set_alpha(50)
            
            self.text.update()
            self.text.draw()

            c_sprite = self.choices[self.c_choice]
            c_sprite.deselect()

            self.screen.blit(self.enemy_image, self.enemy_rect)

            if self.enemy_hp < 0: text = 'Enemy HP: 0'
            else: text = 'Enemy HP: {}'.format(self.enemy_hp)
            font_size = FONT.size(text)
            self.screen.blit(FONT.render(text, True, 'grey95'), (360-font_size[0]/2, 48-font_size[1]/2))

        elif self.scene == 4:
            self.screen.blit(self.enemy_image, self.enemy_rect)

            self.frame += 1
            if self.frame > 25:
                self.frame = 0
                self.state = 0
                self.scene += 1
                self.enemy_atk = randint(2*(self.player.level+1), 5*(self.player.level+1))
                if self.type_ == 'boss': self.enemy_atk *= randint(2, 5)
                if self.type_ == 'final': self.enemy_atk *= randint(4, 7)  # get  better
                if getattr(self.player, 'armour') is not None: player_def = self.player.defence + self.player.armour['def']
                else: player_def = self.player.defence
                player_def = round(player_def*self.extra_def)
                atk = round(self.enemy_atk/(player_def/self.enemy_atk+1))+1
                self.text.change_text('{} attacked for {} damage!\n\n>>'.format(self.enemy, atk))
                self.player.change_hp(-atk)
        elif self.scene == 5:
            if self.state == 0:
                self.screen_pos[0] -= self.shake
            elif self.state == 2:
                self.screen_pos[0] += self.shake
            elif self.state == 4:
                self.screen_pos[0] += self.shake
            elif self.state == 6:
                self.screen_pos[0] -= self.shake
                self.shake *= 0.95
                self.state = -2
            
            self.screen.blit(self.enemy_image, self.enemy_rect)

            self.state += 1
            self.frame += 1
            if self.frame == 20:
                self.frame = 0
                self.scene = 5.5
        elif self.scene == 5.5:
            self.screen.blit(self.enemy_image, self.enemy_rect)
            self.screen.blit(self.fight_icon.image, self.fight_icon.rect)
            self.screen.blit(self.sharpen_icon.image, self.sharpen_icon.rect)
            self.screen.blit(self.defend_icon.image, self.defend_icon.rect)
            self.screen.blit(self.heal_icon.image, self.heal_icon.rect)

            if self.player.hp < 0: text = 'Your HP: 0'
            else: text = 'Your HP: {}'.format(self.player.hp)
            font_size = FONT.size(text)
            self.screen.blit(FONT.render(text, True, 'grey95'), (360-font_size[0]/2, 48-font_size[1]/2))

            self.text.update()
            self.text.draw()
        elif self.scene == 6:
            self.text.update()
            self.text.draw()
        elif self.scene == 7:
            self.text.update()
            self.text.draw()

        self.display.blit(self.screen, self.screen_pos)

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if self.scene == 1:
                        if self.c_choice != 0:
                            pygame.mixer.Sound.play(SOUND_SELECT)
                            self.o_choice = self.c_choice
                            self.c_choice -= 1
                if event.key == pygame.K_d:
                    if self.scene == 1:
                        if self.c_choice != len(self.choices)-1:
                            pygame.mixer.Sound.play(SOUND_SELECT)
                            self.o_choice = self.c_choice
                            self.c_choice += 1
                if event.key == pygame.K_x:
                    self.text.skip()
                if event.key == pygame.K_RETURN:
                    if self.scene == 0:
                        pygame.mixer.Sound.play(SOUND_CONFIRM)
                        self.scene = 0.5
                    elif self.scene == 1:
                        pygame.mixer.Sound.play(SOUND_CONFIRM)
                        if self.c_choice == 0:
                            if getattr(self.player, 'weapon') is not None: player_atk = self.player.atk + self.player.weapon['atk']
                            else: player_atk = self.player.atk
                            player_atk = round(player_atk*self.extra_atk)
                            self.damage = round(player_atk/(self.enemy_def/player_atk+1))+1
                            self.text.change_text('You did {} damage!\n\n>>'.format(self.damage))

                            self.enemy_hp -= self.damage
                        elif self.c_choice == 1:
                            if self.extra_atk < 3:
                                self.extra_atk += 0.3
                                self.text.change_text('Your attack increased by {:.2} times!\n\n>>'.format(self.extra_atk))
                            else:
                                self.text.change_text('Your weapon is too sharp and you\'re afraid of ruining it by sharpening further!\n\n>>')
                        elif self.c_choice == 2:
                            if self.extra_def < 3:
                                self.extra_def += 0.3
                                self.text.change_text('Your defence increased by {:.2} times!\n\n>>'.format(self.extra_def))
                            else:
                                self.text.change_text('You try to raise your guard further, but you could not reach any higher!\n\n>>')
                        elif self.c_choice == 3:
                            if self.heals != 0:
                                heal = randint(25, 50)/100 * self.player.hp
                                self.text.change_text('You healed {} HP\n\n>>'.format(heal))
                                self.heals -= 1
                            else:
                                self.text.change_text('You cannot heal any fruther!\n\n>>')
                        self.scene += 1
                    elif self.scene == 3 and self.text.frame == len(self.text.text):
                        self.enemy_image.set_alpha(255)
                        if self.enemy_hp <= 0:
                            self.scene = 6
                            self.enemy_image.set_alpha(0)
                            self.text.change_text('You win!\n\n>>')
                        else:
                            self.scene += 1
                    elif self.scene == 5.5 and self.text.frame == len(self.text.text):
                        if self.player.hp <= 0:
                            self.scene = 7
                            self.enemy_image.set_alpha(0)
                            self.text.change_text('You died...\nBut at least you get more skills points!\n\nLevel: {}\n\n>>'.format(self.player.level))
                        else:
                            self.scene = 0.5
                    elif self.scene == 6 and self.text.frame == len(self.text.text):
                        self.running = False
                        if self.type_ == 'boss': self.status = 'POST ENEMY ROOM - WON - BOSS'
                        else: self.status = 'POST ENEMY ROOM - WON'
                    elif self.scene == 7 and self.text.frame == len(self.text.text):
                        self.running = False
                        self.status = 'POST ENEMY ROOM - DEAD'
        
    def run(self):
        if not self.running:
            return self.status

        self.get_events()
        self.update_display()


class ChestScene(Scene):
    'Scene for chest room'

    def __init__(self, display, player, w_spritesheet, a_spritesheet, type_=None):
        super().__init__(display, (), player)

        self.chest_c_image = pygame.image.load('assets/chest_c.png').convert_alpha()
        self.chest_c_image = pygame.transform.scale(self.chest_c_image, (128, 128))
        self.chest_c_rect = self.chest_c_image.get_rect()
        self.chest_c_rect.center = 360, 120

        self.chest_o_image = pygame.image.load('assets/chest_o.png').convert_alpha()
        self.chest_o_image = pygame.transform.scale(self.chest_o_image, (128, 128))
        self.chest_o_rect = self.chest_o_image.get_rect()
        self.chest_o_rect.center = 360, 120

        self.stage = 0
        self.timer = 0

        self.item_type = choice(('weapon', 'armour'))
        if self.item_type == 'weapon':
            item = choice(tuple(WEAPON_DICTS.keys()))
            self.item_image = w_spritesheet.get_image(WEAPON_DICTS[item]).convert_alpha()
            self.item_image = pygame.transform.scale(self.item_image, (128, 128))
            self.item_rect = self.item_image.get_rect()
            self.item_rect.center = 360, 120
            self.item_image.set_alpha(0)
            self.anim_x_vel = 30

            if type_ == 'enemy': item_atk = randint(self.player.level-1, self.player.level+3)
            elif type_ == 'boss': item_atk= randint(self.player.level+1, self.player.level+5)
            else: item_atk = randint(self.player.level-3, self.player.level+3)
            if item_atk < 1: item_atk = 1
            item_name = '{} Of {} {}'.format(item, choice(WEAPON_ADJ), choice(WEAPON_END))
            self.item = {'name': item_name, 'atk': item_atk, 'sprite': WEAPON_DICTS[item]}

            if self.player.weapon is None:
                text = 'You found a new weapon!\n' \
                    'New weapon: {}\nATK {}\n\n'.format(self.item['name'], self.item['atk']) + \
                    'As you have nothing, you decide to take the new found weapon\n\n>>'
            else:
                self.pitem_image = w_spritesheet.get_image(self.player.weapon['sprite']).convert_alpha()
                self.pitem_image = pygame.transform.scale(self.pitem_image, (128, 128))
                self.pitem_rect = self.pitem_image.get_rect()
                self.pitem_rect.center = 0, 120

                text = 'You found a new weapon!\n' \
                    'Your weapon: {}\nATK {}\n\n'.format(self.player.weapon['name'], self.player.weapon['atk']) + \
                    'New weapon: {}\nATK {}\n\n'.format(self.item['name'], self.item['atk']) + \
                    'Replace?'
        elif self.item_type == 'armour':
            item = choice(tuple(ARMOUR_DICTS.keys()))
            self.item_image = a_spritesheet.get_image(ARMOUR_DICTS[item]).convert_alpha()
            self.item_image = pygame.transform.scale(self.item_image, (128, 128))
            self.item_rect = self.item_image.get_rect()
            self.item_rect.center = 360, 120
            self.item_image.set_alpha(0)
            self.anim_x_vel = 30

            if type_ == 'enemy': item_def = randint(self.player.level-1, self.player.level+3)
            elif type_ == 'boss': item_def= randint(self.player.level+1, self.player.level+5)
            else: item_def = randint(self.player.level-3, self.player.level+3)
            if item_def < 1: item_def = 1
            item_name = '{} Of {} {}'.format(item, choice(ARMOUR_ADJ), choice(ARMOUR_END))
            self.item = {'name': item_name, 'def': item_def, 'sprite': ARMOUR_DICTS[item]}

            if self.player.armour is None:
                text = 'You found new armour!\n' \
                    'New item: {}\nDEF {}\n\n'.format(self.item['name'], self.item['def']) + \
                    'As you have nothing, you decide to take the new found armour\n\n>>'
            else:
                self.pitem_image = a_spritesheet.get_image(self.player.armour['sprite']).convert_alpha()
                self.pitem_image = pygame.transform.scale(self.pitem_image, (128, 128))
                self.pitem_rect = self.pitem_image.get_rect()
                self.pitem_rect.center = 0, 120

                text = 'You found new armour!\n' \
                    'Your armour: {}\nDEF {}\n\n'.format(self.player.armour['name'], self.player.armour['def']) + \
                    'New armour: {}\nDEF {}\n\n'.format(self.item['name'], self.item['def']) + \
                    'Replace?'

        self.text = Text(self.display, text, speed=1, pos=(60, 192))

        self.anim = Animation(20, 180)

        self.choice = 0

    def update_display(self):
        if self.stage == 0:
            self.timer += 1
            self.display.blit(self.chest_c_image, self.chest_c_rect)

            if self.timer == 25:
                self.timer = 0
                self.stage += 1
        elif self.stage == 1:
            self.timer += 1
            self.display.blit(self.chest_o_image, self.chest_o_rect)

            self.item_image.set_alpha(self.item_image.get_alpha()+5)
            self.display.blit(self.item_image, self.item_rect)

            if self.timer == 51:
                self.timer = 0
                self.stage += 1
        elif self.stage == 2:
            self.timer += 1
            self.chest_o_image.set_alpha(self.chest_o_image.get_alpha()-7)
            self.display.blit(self.chest_o_image, self.chest_o_rect)

            if getattr(self.player, self.item_type) is not None:
                self.pitem_rect.centerx += self.anim.get_move(self.timer-1)
                self.item_rect.centerx += self.anim.get_move(self.timer-1)

            if self.item_rect.centerx >= 540:
                self.item_rect.centerx = 540
                self.pitem_rect.centerx = 180
                self.timer = 0
                self.stage += 1

            self.display.blit(self.item_image, self.item_rect)
            if getattr(self.player, self.item_type) is not None:
                self.display.blit(self.pitem_image, self.pitem_rect)

            if self.timer == 25:
                self.stage = 4
                setattr(self.player, self.item_type, self.item)
        elif self.stage == 3:
            self.display.blit(self.item_image, self.item_rect)
            self.display.blit(self.pitem_image, self.pitem_rect)

            self.text.update()
            self.text.draw()

            if self.choice == 0:
                font_size = FONT.size('Yes')
                self.display.blit(FONT.render('Yes', True, '#FFFF00'), (240-font_size[0]/2, 384-font_size[1]/2))
                font_size = FONT.size('No')
                self.display.blit(FONT.render('No', True, 'grey95'), (480-font_size[0]/2, 384-font_size[1]/2))
            elif self.choice == 1:
                font_size = FONT.size('Yes')
                self.display.blit(FONT.render('Yes', True, 'grey95'), (240-font_size[0]/2, 384-font_size[1]/2))
                font_size = FONT.size('No')
                self.display.blit(FONT.render('No', True, '#FFFF00'), (480-font_size[0]/2, 384-font_size[1]/2))

        elif self.stage == 4:  # No weapon
            self.display.blit(self.item_image, self.item_rect)

            self.text.update()
            self.text.draw()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pygame.mixer.Sound.play(SOUND_SELECT)
                    if self.choice != 0:
                        self.choice -= 1
                    else:
                        self.choice = 1
                if event.key == pygame.K_d:
                    pygame.mixer.Sound.play(SOUND_SELECT)
                    if self.choice != 1:
                        self.choice += 1
                    else:
                        self.choice = 0
                if event.key == pygame.K_RETURN:
                    if self.stage == 3:
                        if self.choice == 0 and self.text.frame == len(self.text.text):
                            setattr(self.player, self.item_type, self.item)
                            pygame.mixer.Sound.play(SOUND_TAKE_ITEM)
                            self.running = False
                        elif self.text.frame == len(self.text.text):
                            pygame.mixer.Sound.play(SOUND_CONFIRM)
                            self.running = False
                    if self.stage == 4:
                        if self.text.frame == len(self.text.text):
                            pygame.mixer.Sound.play(SOUND_TAKE_ITEM)
                            self.running = False
                if event.key == pygame.K_x:
                    if self.stage >= 3:
                        self.text.skip()


class BoostScene(Scene):
    '''Scene for changing the player skills'''

    def __init__(self, display, player, type_=None):
        super().__init__(display, (), player)

        self.player = player
        self.choice = 0
        self.choices = (
            Skill(self.display, self.player, (SCREEN_W/4-45, SCREEN_H/3), 'atk', 'assets/attackskill'),
            Skill(self.display, self.player, (SCREEN_W/4*2, SCREEN_H/3), 'hp', 'assets/healthskill'),
            Skill(self.display, self.player, (SCREEN_W/4*3+45, SCREEN_H/3), 'defence', 'assets/defenceskill'),
        )
        self.border = pygame.image.load('assets/skillborder.png').convert_alpha()
        self.border = pygame.transform.scale(self.border, (192, 132))
        self.border_rect = self.border.get_rect()
        self.border_rect.center = self.choices[0].rect.center

        if type_ == 'dead':
            text = 'You died but at least you gain 5 more skills points\n\n>>'
        else:
            self.player.skill_points += 10
            text = 'The legends were right!\nYou do become stronger after entering\n\n' \
                'You gained 10 skill points!\n\n>>'
        self.text = Text(self.display, text, speed=1, pos=(60, 270))

        self.ee1 = False

    def update_display(self):
        for skill in self.choices:
            skill.update_display()

        # Moves the border to the current pos
        if self.border_rect.centerx > self.choices[self.choice].rect.centerx:
            self.border_rect.centerx -= 15
        elif self.border_rect.centerx < self.choices[self.choice].rect.centerx:
            self.border_rect.centerx += 15
        # self.border_rect.center = self.choices[self.choice].rect.center
        self.display.blit(self.border, self.border_rect)

        # Text business
        if not self.ee1:
            self.sp_text = 'You have {} skill points remaining'.format(self.player.skill_points-self.player.sum)
        font_size = FONT.size(self.sp_text)
        self.display.blit(FONT.render(self.sp_text, True, 'grey95'), (360-font_size[0]/2, 48-font_size[1]/2))

        self.text.update()
        self.text.draw()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.ee1 = False
                # Controls the changing of skill
                if event.key == pygame.K_a:
                    pygame.mixer.Sound.play(SOUND_SELECT)
                    if self.choice != 0:
                        self.choice -= 1
                if event.key == pygame.K_d:
                    pygame.mixer.Sound.play(SOUND_SELECT)
                    if self.choice != len(self.choices)-1:
                        self.choice += 1
                # Controls the changing of skill amount
                if event.key == pygame.K_w:
                    pygame.mixer.Sound.play(SOUND_SELECT)
                    setattr(self.player, self.choices[self.choice].skill, getattr(self.player, self.choices[self.choice].skill)+1)
                    if self.player.sum > self.player.skill_points:
                        setattr(self.player, self.choices[self.choice].skill, getattr(self.player, self.choices[self.choice].skill)-1)
                        self.sp_text = choice(('You think you have any skill points left to spend?', 'With what skill points?', 'nah', 'no.', 'Keep trying.', 'uh oh, 0 left', 'L', ':clown:', 'ZERO LOL IMAGINE', 'no skill points'))
                        self.ee1 = True
                if event.key == pygame.K_s:
                    pygame.mixer.Sound.play(SOUND_SELECT)
                    if getattr(self.player, self.choices[self.choice].skill) > 1:
                        setattr(self.player, self.choices[self.choice].skill, getattr(self.player, self.choices[self.choice].skill)-1)
                    else:
                        self.sp_text = choice(('Really?', '...', '?', 'How?', 'Keep trying.', 'how does that work, eh?'))
                        self.ee1 = True
                if event.key == pygame.K_x:
                    self.text.skip()
                # Next scene
                if event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(SOUND_CONFIRM)
                    self.running = False


class WonScene(Scene):
    '''Scene for the win scene'''

    def __init__(self, display, player):
        super().__init__(display, (), player)

        text = 'You have made it...\n' \
            'You won\n\n' \
            'How long did that take? Need more?\nEndless mode is endless and has a greater chance for boss fights! If you want more difficulty...\n\n>> (Game will close)'

        self.text = Text(self.display, text, speed=1, pos=(60, 192))

    def update_display(self):
        self.text.update()
        self.text.draw()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.text.frame == len(self.text.text):
                        pygame.mixer.Sound.play(SOUND_CONFIRM)
                        pygame.quit()
                        exit()
                if event.key == pygame.K_x:
                    self.text.skip()
