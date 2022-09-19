import pygame

from dependencies import *


class Manager:
    '''Game manager, controls what the user sees and oversees the entire game'''

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption('Snungeon by David Nguyen')
        iconicon = pygame.image.load('assets/iconicon.png')
        pygame.display.set_icon(iconicon)

        self.player = Player()

        self.scene = 0
        self.current_scene = TitleScene(self.screen, self.player)

        self.weapon_sheet = SpriteSheet('assets/weapons')
        self.armour_sheet = SpriteSheet('assets/armour')
        self.battleicon_sheet = SpriteSheet('assets/battleicons')
        self.enemies_sheet = SpriteSheet('assets/enemies')

        self.status = 0

    def story_loop(self):
        '''Loop manager for story mode'''

        run_scene = self.current_scene.run()

        if run_scene == 'HEAL ROOM':
            self.current_scene = HealScene(self.screen, self.player)
        elif run_scene == 'BOOST ROOM':
            self.current_scene = BoostScene(self.screen, self.player)
        elif run_scene == 'ENEMY ROOM':
            if round(random(), 2) <= 1/25: self.current_scene = EnemyScene(self.screen, self.player, self.enemies_sheet, self.battleicon_sheet, 'boss')
            else: self.current_scene = EnemyScene(self.screen, self.player, self.enemies_sheet, self.battleicon_sheet)
        elif run_scene == 'CHEST ROOM':
            self.current_scene = ChestScene(self.screen, self.player, self.weapon_sheet, self.armour_sheet)
        elif run_scene == 'POST ENEMY ROOM - WON':
            self.current_scene = ChestScene(self.screen, self.player, self.weapon_sheet, self.armour_sheet, 'enemy')
        elif run_scene == 'POST ENEMY ROOM - WON - BOSS':
            self.current_scene = ChestScene(self.screen, self.player, self.weapon_sheet, self.armour_sheet, 'boss')
        elif run_scene == 'POST ENEMY ROOM - DEAD':
            sp = self.player.level
            if sp > 5: sp = 5
            self.player.skill_points += sp
            self.player.level = 0
            self.player.atk = 1
            self.player.hp = 1
            self.player.defence = 1
            self.player.weapon = None
            self.player.armour = None
            self.current_scene = BoostScene(self.screen, self.player, 'dead')
        elif run_scene:
            self.player.level += 1
            self.current_scene = SelectionScene(self.screen, gen_random_rooms(), self.player)

            if self.player.level >= 99 and self.status == 0:
                self.current_scene = EnemyScene(self.screen, self.player, self.enemies_sheet, self.battleicon_sheet, 'final')
                self.status = 1
                self.player.level += 1
            elif self.player.level >= 100 and self.status == 1:
                self.current_scene = WonScene(self.screen, self.player)
                self.status = 2

    def endless_loop(self):
        '''Loop manager for endless mode'''

        run_scene = self.current_scene.run()

        if run_scene == 'HEAL ROOM':
            self.current_scene = HealScene(self.screen, self.player)
        elif run_scene == 'BOOST ROOM':
            self.current_scene = BoostScene(self.screen, self.player)
        elif run_scene == 'ENEMY ROOM':
            if round(random(), 2) <= 1/2: self.current_scene = EnemyScene(self.screen, self.player, self.enemies_sheet, self.battleicon_sheet, 'boss')
            else: self.current_scene = EnemyScene(self.screen, self.player, self.enemies_sheet, self.battleicon_sheet)
        elif run_scene == 'CHEST ROOM':
            self.current_scene = ChestScene(self.screen, self.player, self.weapon_sheet, self.armour_sheet)
        elif run_scene == 'POST ENEMY ROOM - WON':
            self.current_scene = ChestScene(self.screen, self.player, self.weapon_sheet, self.armour_sheet, 'enemy')
        elif run_scene == 'POST ENEMY ROOM - WON - BOSS':
            self.current_scene = ChestScene(self.screen, self.player, self.weapon_sheet, self.armour_sheet, 'boss')
        elif run_scene == 'POST ENEMY ROOM - DEAD':
            sp = self.player.level
            if sp > 5: sp = 5
            self.player.skill_points += sp
            self.player.level = 0
            self.player.atk = 1
            self.player.hp = 1
            self.player.defence = 1
            self.player.weapon = None
            self.player.armour = None
            self.current_scene = BoostScene(self.screen, self.player, 'dead')
        elif run_scene:
            self.player.level += 1
            self.current_scene = SelectionScene(self.screen, gen_random_rooms(), self.player)

    def loop_manager(self):
        '''Loop manager that runs that current scene'''

        self.screen.fill(BG_COLOUR)

        if self.scene == 0:
            if self.current_scene.run():
                self.level_type = self.current_scene.run()
                self.current_scene = NameScene(self.screen, self.player)
                self.scene += 1
        elif self.scene == 1:
            if self.current_scene.run():
                self.current_scene = SkillScene(self.screen, self.player)
                self.scene += 1
        elif self.scene == 2:
            if self.current_scene.run():
                self.scene += 1
        elif self.scene == 3:
            if self.level_type == 'Story':
                self.player.level += 1
                self.current_scene = SelectionScene(self.screen, gen_random_rooms(), self.player)
                self.scene += 1
            if self.level_type == 'Endless':
                self.player.level += 1
                self.current_scene = SelectionScene(self.screen, gen_random_rooms(), self.player)
                self.scene = 5
        elif self.scene == 4:
            self.story_loop()
        elif self.scene == 5:
            self.endless_loop()

    def run(self):
        '''PyGame loop'''

        while True:
            self.loop_manager()

            pygame.display.update()
            self.clock.tick(FRAME_RATE)


if __name__ == '__main__':
    mgr = Manager()
    mgr.run()
