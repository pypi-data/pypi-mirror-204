import moderngl as mgl
import pygame as pg
import numpy as np
import os

class Texture:
    def __init__(self, app):
        self.os = os.name
        self.app = app
        self.ctx = app.ctx
        self.textures = {'default':self.get_texture('default.png'), 'dt':self.get_depth_texture()}
        self.skyBoxes = {'default':self.get_texture_cube('default')}

    def loadTexPack(self, names):
        for name in names:
            self.textures[name] = self.get_texture(name)

    def loadSkyPack(self, names):
        for name in names:
            self.skyBoxes[name] = self.get_texture_cube(name)

    def get_depth_texture(self):
        tex = self.ctx.depth_texture(self.app.size)
        tex.repeat_x = False
        tex.repeat_y = False
        return tex

    def get_texture_cube(self, name):
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        textures = []
        for face in faces:
            texPath = ''
            if self.os == 'posix':
                texPath = f'./accets/skyboxes/{name}/{face}.png'
            elif self.os == 'nt':
                texPath = f'accets\\skyboxes\\{name}\\{face}.png'
            texture = pg.image.load(texPath).convert_alpha()
            if face in ['right', 'left', 'front', 'back']:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)
        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)
        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)
        return texture_cube

    def get_texture(self, name):
        texPath = ''
        if self.os == 'posix':
            texPath = f'./accets/textures/{name}'
        elif self.os == 'nt':
            texPath = f'accets\\textures\\{name}'
        img = pg.image.load(texPath).convert_alpha()
        return self.create_texture(img)

    def create_texture(self, img):
        img = pg.transform.flip(img, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=img.get_size(), components=4, data=pg.image.tostring(img, 'RGBA'))
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.swizzle = 'RGBA'
        texture.build_mipmaps()
        texture.anisotropy = 32.0
        return texture

    def gt(self, name):
        if name in self.textures.keys(): return self.textures[name]
        else: return self.textures['default']

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
