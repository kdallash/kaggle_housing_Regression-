import pygame
import json

NEIGHBOR_OFSET = [
    (0, 0),
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (-1, 1),
    (-1, -1),
    (1, -1),
    (1, 1),
]
AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}
physics_tile = {"grass", "stone"}  # set faster to look data in
AUTOTILE_type = {"grass", "stone"}


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        # using dictinaary so you could put tile in anyspace m4 wra b3d
        self.tile_map = {}
        self.offgrid_tile = []
    def extract(self,id_pairs,keep=False):
        matches=[]
        for tile in self.offgrid_tile.copy():
            if (tile["type"],tile["variant"])in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tile.remove(tile)
        for loc in self.tile_map:
            tile=self.tile_map[loc]
            if (tile["type"],tile["variant"])in id_pairs:
                matches.append(tile.copy())
                matches[-1]["pos"]=matches[-1]["pos"].copy()
                matches[-1]["pos"][0]*=self.tile_size
                matches[-1]["pos"][1]*=self.tile_size
                if not keep :
                    del self.tile_map[loc]
        return matches
    def tiles_around(self, pos):
        tiles = []
        # convert pixle position int gred position
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFSET:
            check_loc = (
                str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1])
            )

            if check_loc in self.tile_map:
                tiles.append(self.tile_map[check_loc])
        return tiles

    def physic_rect_around(self, pos):
        rect = []
        for tile in self.tiles_around(pos):
            if tile['type'] in physics_tile:
                rect.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))

        return rect

    
    def save(self, path):
        f = open(path, "w")
        json.dump(
            {
                "tile_map": self.tile_map,
                "tile_size": self.tile_size,
                "offgrid_tile": self.offgrid_tile,
            },
            f,
        )
        f.close()

    def load(self, path):
        f = open(path, "r")
        map_date = json.load(f)
        f.close()

        self.tile_map = map_date["tile_map"]
        self.tile_size = map_date["tile_size"]
        self.offgrid_tile = map_date["offgrid_tile"]

    def auto_tile(self):
        for loc in self.tile_map:
            tile = self.tile_map[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = (
                    str(tile["pos"][0] + shift[0])
                    + ";"
                    + str(tile["pos"][1] + shift[1])
                )
                if check_loc in self.tile_map:
                    if self.tile_map[check_loc]["type"] == tile["type"]:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile["type"] in AUTOTILE_type) and (neighbors in AUTOTILE_MAP):
                tile["variant"] = AUTOTILE_MAP[neighbors]
    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tile:
            # offset in minus as camera move one way screen appear like it move the other
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]),
            )
        for x in range(
            offset[0] // self.tile_size,
            (offset[0] + surf.get_width()) // self.tile_size + 1,
        ):
            for y in range(
                offset[1] // self.tile_size,
                (offset[1] + surf.get_height()) // self.tile_size + 1,
            ):
                loc = str(x) + ";" + str(y)
                if loc in self.tile_map:
                    tile = self.tile_map[loc]
                    surf.blit(
                        self.game.assets[tile["type"]][tile["variant"]],
                        (
                            tile["pos"][0] * self.tile_size - offset[0],
                            tile["pos"][1] * self.tile_size - offset[1],
                        ),
                    )
