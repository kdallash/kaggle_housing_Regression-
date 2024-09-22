import pygame
from script.particles import Particles
import math
import random
class physicsEntity:
    # game paremeter is to access entity in game????? look into it
    # we pass self to it so most likly yes put not sure
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collision = {"up": False, "down": False, "right": False, "left": False}
        self.action = ""
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action("idle")
        self.last_movment = [0,0]
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + "/" + self.action].copy()

    def update(self, tilemap, movement=(0, 0)):
        self.collision = {"up": False, "down": False, "right": False, "left": False}
        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        )
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physic_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:  # move right 
                    entity_rect.right = rect.left # set right of entiity to left of rect
                    self.collision["right"] = True
                if frame_movement[0] < 0:  # move left
                    entity_rect.left = rect.right
                    self.collision["left"] = True
                self.pos[0] = entity_rect.x
            

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physic_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:  # move bottom
                    entity_rect.bottom = rect.top
                    self.collision["down"] = True

                if frame_movement[1] < 0:  # move top
                    entity_rect.top = rect.bottom
                    self.collision["up"] = True
                self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
        self.last_movment=movement
        
        # min act as an if statment it return the lower value so if self.velocity[1]+0.1 is lowwer than 5 it will return it
        # if not velocity cap at 5
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        if self.collision["down"] or self.collision["up"]:
            self.velocity[1] = 0
        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(
            pygame.transform.flip(self.animation.img(), self.flip, False),
            (
                self.pos[0] - offset[0] + self.anim_offset[0],
                self.pos[1] - offset[1] + self.anim_offset[1],
            ),
        )


class Player(physicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_jump = False
        self.dashing = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        self.air_time += 1

        if self.collision["down"]:
            self.air_time = 0
            self.jumps = 1
        self.wall_jump = False
        if (self.collision["right"] or self.collision["left"]) and self.air_time > 4 :
            self.wall_jump=True
            self.velocity[1] = min (self.velocity[1],0.5)
            if self.collision["right"]:
                self.flip = False
            else:
                self.flip = True
            self.set_action("wall_slide")
        if not self.wall_jump:    
            if self.air_time > 4:
                self.set_action("jump")
            elif movement[0] != 0:
                self.set_action("run")
            else:
                self.set_action("idle")
        if abs(self.dashing) in {60, 50}:
            for i in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particles(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1

            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particles(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
                

        
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.2, 0)
        elif self.velocity[0] < 0:
            self.velocity[0] = min(self.velocity[0] + 0.2, 0)
    
    def render(self, surf, offset=(0, 0)):
        if abs(self.dashing) <= 50:
            super().render(surf, offset=offset)



    def jump(self):
        if self.wall_jump:
            if self.flip and self.last_movment[0] < 0:
                self.velocity[0] = 3
                self.velocity[1] = -2.5
                self.air_time = 5 
                self.jumps = max (self.jumps - 1, 0)
                return True
            elif not self.flip and self.last_movment[0] > 0:
                self.velocity[0] = -3
                self.velocity[1] = -2.5
                self.air_time = 5 
                self.jumps = max (self.jumps - 1, 0)
                return True
        elif self.jumps:
            self.velocity[1] = -3
            self.jumps = 0
            self.air_time = 5
            return True
    def dash(self):
        if not self.dashing:
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60