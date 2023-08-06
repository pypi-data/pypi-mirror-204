import glm
import pygame as pg


class Camera:
    def __init__(self, app, position=(0,0,4), yaw=-90, pitch=0):
        self.app = app
        self.rotMouse = [0, 0]
        self.visible = True
        self.cinematog = False
        self.pcm = {True:[0.02, 0.94], False:[0.15, 0.5]}
        self.aspect_ratio = app.size[0] / app.size[1]
        self.FOV = 60
        self.NEAR = 0.1
        self.FAR = 1000
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        self.px, self.pn = 90, -90
        self.view = 300
        self.gvm()
        self.gpm()

    def rot(self, rel):
        self.rotMouse[0] += rel[0] * self.pcm[self.cinematog][0]
        self.rotMouse[1] += rel[1] * self.pcm[self.cinematog][0]

    def ucv(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)
        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)
        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0,1,0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        self.ucv()
        self.gvm()
        self.gpm()
        self.yaw += self.rotMouse[0]
        self.pitch -= self.rotMouse[1]
        self.pitch = max(self.pn, min(self.px, self.pitch))
        self.rotMouse = [i * self.pcm[self.cinematog][1] for i in self.rotMouse]

    def vis(self): self.visible = not self.visible; pg.mouse.set_visible(self.visible); pg.event.set_grab(not(self.visible));
    def cin(self): self.cinematog = not self.cinematog
    def gvm(self): self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)
    def gpm(self): self.m_proj = glm.perspective(glm.radians(self.FOV), self.aspect_ratio, self.NEAR, self.FAR)
