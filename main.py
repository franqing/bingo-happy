import pygame
from pygame.locals import *
import sys
import manager

'''brick : 218*218
   animal : 40*40
   bg : 850*600
'''

pygame.init()
pygame.mixer.init()


def show_start_screen():
    start_screen = manager.StartScreen()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            result = start_screen.handle_event(event)
            if result == "start":
                return True
            elif result == "exit":
                pygame.quit()
                sys.exit()

        start_screen.draw(manager.ManagerTree.screen)
        pygame.display.flip()


def main():
    # Show start screen
    if not show_start_screen():
        return

    tree = manager.ManagerTree()
    m = manager.Manager(0, 0)
    sound_sign = 0
    world_bgm = pygame.mixer.Sound(manager.SoundPlay.world_bgm)
    game_bgm = pygame.mixer.Sound(manager.SoundPlay.game_bgm)

    while True:
        if m.level == 0:
            if sound_sign == 0:
                game_bgm.stop()
                world_bgm.play(-1)
                sound_sign = 1
        else:
            if sound_sign == 1:
                world_bgm.stop()
                game_bgm.play(-1)
                sound_sign = 0

        if m.level == 0:
            tree.draw_tree(m.energy_num, m.money)
        else:
            m.set_level_mode(m.level)
            sprite_group = m.draw()
            if m.type == 0:
                m.eliminate_animal()
                m.death_map()
                m.exchange(sprite_group)
            m.judge_level()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    exit()
            if event.type == QUIT:
                sys.exit()
            m.level, m.energy_num, m.money = tree.mouse_select(event, m.level, m.energy_num, m.money)
            m.mouse_select(event)

        m.mouse_image()
        pygame.display.flip()


if __name__ == "__main__":
    main()