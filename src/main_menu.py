import sys

from settings import *
from support import transformation
from Button import Button
from settings_menu import Settings
from game import Game
from config import Configuration
from levels_window import LevelsMenu

pygame.init()
font = pygame.font.Font('../src/font/custom/HOOG0554.TTF', 30)
click_sound = '../sound/menu/click.mp3'
back_music = '../sound/menu/background.wav'
background1 = pygame.image.load('../sprites/menu/game_title.png')


class MainMenu:
    def __init__(self, surface):
        # pygame.init()
        pygame.display.set_caption('main menu')
        self.clock = pygame.time.Clock()
        self.surface = surface
        self.running = True

        self.play_bttn = Button('play', 250, 80,
                                (width // 2 - 535, height // 2 + 200), self.surface, 10, click_sound)
        self.settings_bttn = Button('settings', 250, 80,
                                    (width // 2 - 100, height // 2 + 200), self.surface, 10, click_sound)
        self.exit_bttn = Button('exit', 250, 80,
                                (width // 2 + 305, height // 2 + 200), self.surface, 10, click_sound)
        self.buttons_list = [self.play_bttn, self.settings_bttn, self.exit_bttn]

        self.config = Configuration()
        self.menu_mus_val = self.config.menu_mus_val

        self.menu_music = pygame.mixer.Sound(back_music)
        self.menu_music.set_volume(self.menu_mus_val)

    def run(self):
        chanel3.play(self.menu_music, loops=-1)
        # self.menu_music.play(loops=-1)
        while self.running:
            self.update()
            self.events()
        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            '''выход'''
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            '''нажатие на кнопки'''
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bttn in self.buttons_list:
                    bttn.click(event.pos)
            '''обработка событий после нажатия на кнопки'''
            if event.type == pygame.MOUSEBUTTONUP:
                if self.play_bttn.no_click(event.pos):
                    transformation(self.surface)
                    # chanel3.pause()
                    levels = LevelsMenu()
                    levels.run()
                elif self.settings_bttn.no_click(event.pos):
                    transformation(self.surface)
                    settings = Settings()
                    settings.run()
                elif self.exit_bttn.no_click(event.pos):
                    self.running = False
            '''обработка событий движения курсора'''
            if event.type == pygame.MOUSEMOTION:
                for bttn in self.buttons_list:
                    bttn.on_the_button(event.pos)

    def update(self):
        self.surface.fill('#FFFFFF')
        self.surface.blit(background1, (0, 0))
        for bttn in self.buttons_list:
            bttn.draw()
        self.config.update_values()
        self.menu_mus_val = self.config.menu_mus_val
        self.menu_music.set_volume(self.menu_mus_val)
        # chanel3.unpause()
        pygame.display.update()
        self.clock.tick(fps)
