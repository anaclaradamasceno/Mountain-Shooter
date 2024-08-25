import sys
from datetime import datetime
import pygame
from pygame import Surface, K_BACKSPACE
from pygame.font import Font
from pygame.locals import Rect, KEYDOWN, K_RETURN, K_ESCAPE
from code.Const import C_YELLOW, SCORE_POS, MENU_OPTION, C_WHITE
from code.DBProxy import DBProxy


class Score:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('C:/Users/55219/PycharmProjects/Jogo/asset/ScoreBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def get_formatted_date(self):
        current_datetime = datetime.now()
        current_time = current_datetime.strftime("%H:%M")
        current_date = current_datetime.strftime("%d/%m/%y")
        return f"{current_time} - {current_date}"

    def save(self, game_mode: str, player_score: list[int]):
        pygame.mixer_music.load('C:/Users/55219/PycharmProjects/Jogo/asset/Score.mp3')
        pygame.mixer_music.play(-1)
        db_proxy = DBProxy('DBScore')
        name = ""
        while True:
            self.window.blit(self.surf, self.rect)
            self.score_text(48, 'YOU WIN!!!', C_YELLOW, SCORE_POS['Title'])

            if game_mode == MENU_OPTION[0]:
                score = player_score[0]
                text = 'Player 1 enter your name (4 characters): '
            elif game_mode == MENU_OPTION[1]:
                score = (player_score[0] + player_score[1]) / 2
                text = 'Enter team name (4 characters): '
            elif game_mode == MENU_OPTION[2]:
                if player_score[0] >= player_score[1]:
                    score = player_score[0]
                    text = 'Player 1 enter your name (4 characters): '
                else:
                    score = player_score[1]
                    text = 'Player 2 enter your name (4 characters): '

            self.score_text(20, text, C_WHITE, SCORE_POS['EnterName'])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN and len(name) == 4:
                        db_proxy.save({'name': name, 'score': score, 'date': self.get_formatted_date()})
                        self.show()
                        return
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    elif event.unicode.isalpha() and len(name) < 4:
                        name += event.unicode

            self.score_text(20, name, C_WHITE, SCORE_POS['Name'])
            pygame.display.flip()

    def score_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)

    def show(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.surf, self.rect)
        self.score_text(text_size=25, text="TOP 10 SCORE", text_color=C_YELLOW, text_center_pos=SCORE_POS['Title'])
        self.score_text(text_size=20, text="NAME   SCORE               DATE", text_color=C_YELLOW,
                        text_center_pos=SCORE_POS['Label'])

        db_proxy = DBProxy('DBScore')
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        for i, player_score in enumerate(list_score):
            id_, name, score, date = player_score
            self.score_text(20, f'{name}     {score: 05d}       {date}', C_YELLOW,
                            SCORE_POS.get(i, (400, 300 + 20 * i)))  # Default position if index not found

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
            pygame.display.flip()
