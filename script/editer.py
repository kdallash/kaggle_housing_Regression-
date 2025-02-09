import pygame
import sys
from script.tilemap import Tilemap
from script.utilies import load_images

RENDER_SCALE = 2.0


class Editor:
    def __init__(self) -> None:
        pygame.init()
        # set game name
        pygame.display.set_caption("editor")
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
            "spawner": load_images("tiles/spawners"),
        }
        self.movement = [False, False, False, False]

        # create an object of the physics entity class

        # WHEN YOU PASS SELF IT ALLOW FOR FULL ACCESS ALL ENTITY IN GAME (CLASS)
        self.tile_map = Tilemap(self, 16)
        try:
            self.tile_map.load("map.json")
        except FileNotFoundError:
            pass
        self.scroll = [0, 0]  # for the  illusion of camera movment
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

    def run(self):
        while True:
            self.display.fill((0, 0, 0))
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tile_map.render(self.display, offset=render_scroll)
            current_tile_img = self.assets[self.tile_list[self.tile_group]][
                self.tile_variant
            ].copy()
            current_tile_img.set_alpha(100)
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (
                int((mpos[0] + self.scroll[0]) // self.tile_map.tile_size),
                int((mpos[1] + self.scroll[1]) // self.tile_map.tile_size),
            )
            if self.ongrid:
                self.display.blit(
                    current_tile_img,
                    (
                        tile_pos[0] * self.tile_map.tile_size - self.scroll[1],
                        tile_pos[1] * self.tile_map.tile_size - self.scroll[1],
                    ),
                )
            else:
                self.display.blit(
                    current_tile_img, (mpos)
                )  # EDITING VDNSLDVNLNVNLSVNLLSNVSND
            self.display.blit(current_tile_img, (10, 10))
            if self.clicking & self.ongrid:
                self.tile_map.tile_map[str(tile_pos[0]) + ";" + str(tile_pos[1])] = {
                    "type": self.tile_list[self.tile_group],
                    "variant": self.tile_variant,
                    "pos": tile_pos,
                }
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ";" + str(tile_pos[1])
                if tile_loc in self.tile_map.tile_map:
                    del self.tile_map.tile_map[tile_loc]
                for tile in self.tile_map.offgrid_tile.copy():
                    tile_img = self.assets[tile["type"]][tile["variant"]]
                    tile_r = pygame.Rect(
                        tile["pos"][0] - self.scroll[0],
                        tile["pos"][1] - self.scroll[1],
                        tile_img.get_width(),
                        tile_img.get_height(),
                    )
                    if tile_r.collidepoint(mpos):
                        self.tile_map.offgrid_tile.remove(tile)
            # catch any event
            for event in pygame.event.get():
                # if statment for close butten

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tile_map.offgrid_tile.append(
                                {
                                    "type": self.tile_list[self.tile_group],
                                    "variant": self.tile_variant,
                                    "pos": (
                                        mpos[0] + self.scroll[0],
                                        mpos[1] + self.scroll[1],
                                    ),
                                }
                            )
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:  # mouse wheel up
                            self.tile_variant = (self.tile_variant - 1) % len(
                                self.assets[self.tile_list[self.tile_group]]
                            )
                        if (
                            event.button == 5 | event.button == 1024
                        ):  # down ::1024 place holder
                            self.tile_variant = (self.tile_variant + 1) % len(
                                self.tile_list[self.tile_list[self.tile_group]]
                            )
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(
                                self.tile_list
                            )
                            self.tile_variant = 0
                        if event.button == 5 | event.button == 1024:
                            self.tile_group = (self.tile_group + 1) % len(
                                self.tile_list
                            )
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                # cheak if key LEFT OR WRITE is prised
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tile_map.save("map.json")
                    if event.key == pygame.K_t:
                        self.tile_map.auto_tile()

                # cheak if key LEFT OR RIGHT is unprised
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            # render game on small screen then stretch it to the big one to get pixle art
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            # frame cap
            self.clock.tick(60)


Editor().run()
"""offgrid"""
