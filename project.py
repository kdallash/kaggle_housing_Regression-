import pygame
import sys
import random
import math
from script.entities import physicsEntity, Player
from script.tilemap import Tilemap
from script.cloud import Clouds
from script.utilies import load_image, load_images, Animation
from script.particles import Particles

class Game:
    def __init__(self) -> None:
        pygame.init()
        # set game name
        pygame.display.set_caption("gameName")
        # game screen size
        self.screen = pygame.display.set_mode((640, 480))
        # create a small surface to render in
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        # adding image to code

        self.movement = [False, False]
        # self.assets is a dic that contain load all the images for later use
        self.assets = {
            "decor": load_images("tiles/decor"),
            "grass": load_images("tiles/grass"),
            "large_decor": load_images("tiles/large_decor"),
            "stone": load_images("tiles/stone"),
            "player": load_image("entities/player.png"),
            "background": load_image("background.png"),
            "clouds": load_images("clouds"),
            "player/idle": Animation(load_images("entities/player/idle"), image_dur=6),
            "player/run": Animation(load_images("entities/player/run"), image_dur=4),
            "player/jump": Animation(load_images("entities/player/jump"), image_dur=5),
            "player/slided": Animation(load_images("entities/player/slide"), image_dur=5),
            "player/wall_slide": Animation(load_images("entities/player/wall_slide"), image_dur=5),
            "particles/leaf":Animation(load_images("particles/leaf"),image_dur=20,loop=False),
            "particles/particle":Animation(load_images("particles/particle"),image_dur=6,loop=False),

        }
        self.cloud = Clouds(self.assets["clouds"], count=16)
        # create an object of the physics entity class
        self.player = Player(self, (50, 50), (8, 15))
        # WHEN YOU PASS SELF IT ALLOW FOR FULL ACCESS ALL ENTITY IN GAME (CLASS)
        self.tile_map = Tilemap(self, 16)
        self.tile_map.load("map.json")
        self.scroll = [0, 0]  # for the  illusion of camera movment
        for spawner in self.tile_map.extract([("spawners", 0),("spawners", 1)]):
            if spawner["variant"] == 0:
                self.player.pos = spawner["pos"]
            else:
                print(spawner["pos"] , "enemy")
        self.particles=[]
        self.leaf_spawner=[]
        for tree in self.tile_map.extract([("large_decor",2)],keep=True):
             self.leaf_spawner.append(pygame.Rect(4+tree["pos"][0],4+tree["pos"][1],23,13))
        
    def run(self):
        while True:
            self.display.blit(self.assets["background"], (0, 0))
            self.scroll[0] += (
                self.player.rect().centerx
                - self.display.get_width() / 2
                - self.scroll[0]
            ) / 30  # to get focus at midle of screen self.display.get_width()/2
            self.scroll[1] += (
                self.player.rect().centery
                - self.display.get_height() / 2
                - self.scroll[1]
            ) / 30
            self.render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            for rec in self.leaf_spawner:
                if random.random()*49950<rec.width*rec.height:
                    pos=(rec.x+random.random()*rec.width,rec.y+random.random()*rec.height)
                    self.particles.append(Particles(self,"leaf",pos,velocity=[-0.1,0.3],frame=random.randint(0,20)))
            self.cloud.update()
            self.cloud.render(self.display, offset=self.render_scroll)
            self.tile_map.render(self.display, offset=self.render_scroll)
            # update position of character
            self.player.update(self.tile_map, (self.movement[1] - self.movement[0], 0))
            # print chracter on the screen
            self.player.render(self.display, offset=self.render_scroll)
            for particle in self.particles.copy():
                kill=particle.update()
                particle.render(self.display,offset=self.render_scroll)
                if particle.type=="leaf":
                    particle.pos[0]+=math.sin(particle.animation.frame*0.035)*0.3
                if kill:
                    self.particles.remove(particle)
            # catch any event
            for event in pygame.event.get():
                # if statment for close butten
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit

                # cheak if key LEFT OR WRITE is prised
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.player.jump()
                # cheak if key LEFT OR RIGHT is unprised
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_q:
                        self.player.dash()
            # render game on small screen then stretch it to the big one to get pixle art
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            # frame cap
            self.clock.tick(60)


Game().run()
