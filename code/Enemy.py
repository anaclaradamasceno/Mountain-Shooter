#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.EnemyShot import EnemyShot
from code.Entity import Entity
from code.Const import ENTITY_SPEED, ENTITY_SHOT_DELAY, WIN_HEIGHT


class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.moving_up = False

    def move(self):
        if self.name == "Enemy3":
            self.move_enemy3()
        else:
            self.rect.centerx -= ENTITY_SPEED[self.name]

    def move_enemy3(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]

        if self.moving_up:
            self.rect.centery -= ENTITY_SPEED[self.name]
            if self.rect.top <= 0:
                self.moving_up = False
        else:
            self.rect.centery += 2 * ENTITY_SPEED[self.name]
            if self.rect.bottom >= WIN_HEIGHT:
                self.moving_up = True

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
