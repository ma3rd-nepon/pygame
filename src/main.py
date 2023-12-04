import pygame

from map import *
from player import *
from settings import *
from imgs import *
from tool import *
from ui import *
from console import convert


class Game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        super().__init__()
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("alone marshmallow")

        self.game = False  # если она фолс то игра не будет работать (запустится сама после загрузочного экрана)
        self.title_image = pygame.transform.rotozoom(tilte_base, 0, 1)  # пикча загрузочного экрана
        self.current_title = tilte_base  # текущая пикча загрузочного экрана
        self.title_hb = self.title_image.get_rect(center=(w//2, h//2))
        self.title_i = 0  # индекс анимации загрузочного экрана
        self.zahotel = True  # если тру то скипается загрузочный чорний экран
        self.title()  # функция которая этот загрузочный экран воспроизводит
        if self.zahotel:
            self.title_i = len(im_title) + 1

        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.cross_im = crosshair  # картинка прицела
        self.cross = self.cross_im.get_rect()
        pygame.mouse.set_visible(False)
        self.start_game()
        self.last = pygame.time.get_ticks()

        self.spawn = False  # флаг для создания блоков в рандом месте

        self.pause = False  # если тру то игра на паузе
        self.pause_image = pygame.image.load('../sprites/title/presents_1.png').convert_alpha()  # пикча паузы
        self.pause_hb = self.pause_image.get_rect(center=(w // 2, h // 2))

        self.console = False
        self.com = []

        # self.instruct()  # пишет в консоль клавиши

        self.ui.hb_things.append(self.tool.current_pic)

    def start_game(self):
        """Определение всех классов"""
        self.map = Map(self)
        self.player = Player(self)
        self.tool = Tool(self)
        self.ui = Player_UI(self)

    def update(self):
        """Обновление всех штук изображаемых на экране"""
        if self.game:
            if not self.pause:
                self.player.update()
                self.tool.update()
                self.ui.update()
        else:
            self.title()
        pygame.display.flip()
        self.delta_time = self.clock.tick(fps)
        # pygame.display.set_caption(f"{self.clock.get_fps() :.1f}")

        if self.tool.remove_en_perc:
            self.ui.percentage -= 1
            self.tool.remove_en_perc = False

    def draw(self):
        """Отрисовка всех штук на экране"""
        if not self.pause:
            self.screen.fill('#337bc8')
            self.map.draw()
            if self.player.tx:
                self.player.draw_particles(pon[0] + 40, pon[1] + 70)
            else:
                self.player.draw_particles(pon[0] - 20, pon[1] + 70)
            self.player.draw()
            self.tool.draw()
            self.ui.draw()

            # draw crosshair
            mx, my = pygame.mouse.get_pos()  # координаты мыши
            self.cross.x = mx - 15
            self.cross.y = my - 15
            self.screen.blit(self.cross_im, self.cross)

            rect = pygame.rect.Rect(0, 0, 300, h)
            if pygame.Rect.colliderect(rect, self.player.hitbox_rect):
                print('плеер ходит там где ненадо')
        else:
            pygame.draw.line(self.screen, 'white', (0, h // 2), (w, h // 2))
            if self.console:
                pygame.draw.rect(self.screen, 'white', (0, 40, 40, 40))
            else:
                pygame.draw.rect(self.screen, 'black', (0, 40, 40, 40))

    def eventss(self):
        """Обработка событий игры"""
        for e in pygame.event.get():
            m_pos = pygame.mouse.get_pos()
            if e.type == pygame.QUIT or e.type == pygame.K_ESCAPE:
                quit()
            if e.type == 768:
                if e.key == 109:
                    if not self.pause:
                        self.spawn = not self.spawn
                        self.map.rechoice()
                        if self.spawn:
                            print('random blocks spawned!')
                        else:
                            print('random blocks removed!')

                if e.key == pygame.K_SPACE:
                    if not self.pause:
                        self.player.dash()

                if e.key in [97, 100, 115, 119]:
                    self.player.draw_particles(pon[0] - 20, pon[1] + 75)

                if e.key == 92:
                    self.console = True

                # skip title
                if e.key == 13:
                    self.title_i = len(im_title) + 1
                if e.key == pygame.K_ESCAPE:
                    if self.game:
                        self.pause = not self.pause
                        if self.pause:
                            pause_font = pygame.font.Font(font, 30)
                            conf_font = pygame.font.Font(font, 15)
                            pause_text = pause_font.render('Game paused', False, 'white')
                            keys_text = conf_font.render('''
Configuration
  WASD - movement
  SPACE - dash
  M - create blocks (test)
  N - hit
  ESC - pause
  ENTER - title skip
  +/- - +/- coin (test)
  0 - set energy 100''', False, 'white')
                            self.screen.blit(self.pause_image.convert_alpha(), self.pause_hb)
                            self.screen.blit(pause_text, (w / 2 - 150, 20))
                            self.screen.blit(keys_text, (20, h // 2 + 20))
                        else:
                            pass

    def run(self):
        """Запуск игры и её главный цикл"""
        while True:
            self.command()
            self.eventss()
            self.update()
            if self.game:
                self.draw()
                if self.spawn:
                    self.map.spawn_blocks()

    def instruct(self):
        """Вывод всех используемых клавиш и их назначение"""
        print('WASD - ходить')
        print('SPACE - рывок')
        print('M - создать блоки')
        print('N - удар киркой')
        print('ESC - пауза')
        print('ENTER - скип титла')
        print('+/- - плюс/минус монета (тест)')
        print('0 - энергия 100')

    def title(self):
        """Экран 'представляет' вначале запуска программы"""
        self.title_i += 0.01

        if self.title_i > len(im_title):
            self.title_i = 0
            self.current_title = pygame.transform.rotozoom(im_title[-1], 0, 1)
            self.title_image = pygame.transform.flip(self.current_title.convert_alpha(), False, False)
            self.game = True
            return

        self.current_title = pygame.transform.rotozoom(im_title[int(self.title_i)].convert_alpha(), 0, 1)
        self.title_image = pygame.transform.flip(self.current_title, False, False)

        self.screen.blit(self.title_image, self.title_hb)
        self.title_hb.x = 0
        self.title_hb.y = 0

    def command(self):
        if self.pause:
            if self.console:
                key = pygame.key.get_pressed()
                if key[13]:
                    command = convert(self.com)
                    print('command: ' + command)
                    if command == 'help':
                        self.instruct()

                    if 'money' in command:
                        command = command.replace('money ', '')
                        try:
                            self.ui.coin_count += int(command)
                        except ValueError:
                            print('wrong written command')

                    if command == 'crash game':
                        raise WindowsError('idk what happened')

                    if 'energy' in command:
                        command = command.replace('energy ', '')
                        try:
                            self.ui.percentage = int(command)
                        except ValueError:
                            print('wrong written command')
                    else:
                        pass
                    self.console = False
                    self.com.clear()
                for i in pygame.event.get():
                    if i.type == 768:
                        self.com.append(i.key)
                        if i.key == 8:
                            self.com.remove(self.com[-1])


if __name__ == '__main__':
    try:
        game = Game()
        game.run()
    except pygame.error as e:
        print('game off')
    except KeyboardInterrupt as e:
        print('game off by killing process')
