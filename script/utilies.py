import pygame
import os

BAS_IMG_PATH = "data/images/"


def load_image(path):
    # .convert hellp in preformance do with images
    img = pygame.image.load(BAS_IMG_PATH + path)
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path):
    images = []
    for image_name in os.listdir(BAS_IMG_PATH + path):
        images.append(load_image(path + "/" + image_name))
    return images


class Animation:
    def __init__(self, images, image_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.image_duration = image_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.image_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (
                self.image_duration * len(self.images)
            )  #::(self.frame+1):: for total number of frames
            #::(self.image_duration*len(self.images):: for max frame of animation ::%create a loop
        else:
            self.frame = min(self.frame + 1, self.image_duration * len(self.images) - 1)
            if self.frame >= self.image_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.image_duration)]
