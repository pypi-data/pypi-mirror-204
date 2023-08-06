import moderngl as mgl
import pygame as pg
import numpy as np
from moviepy.editor import VideoFileClip
import cv2, os, time
from threading import Thread as Th
import sounddevice as sd

class Clip:
    def __init__(self, path, end):
        self.pause = True
        self.pTime = time.time()
        self.img = pg.Surface((100, 100))
        self.end = end
        self.col = 0
        if path != 0:
            self.path = path
            self.video = VideoFileClip(path)
            self.music = self.video.audio.to_soundarray()
            self.fps = self.video.fps
            #sd.play(self.music, 48000)
        else:
            self.path = path
            self.fps = 20
        self.cap = cv2.VideoCapture(path)
        if self.cap.isOpened() == False: print(f'Не возможно открыть файл {name}')

    def run(self):
        while True:
            self.update()

    def update(self):
        if self.pause: self.pTime = time.time()
        l = time.time() - self.pTime
        n = round(l / (1/self.fps))
        fl, img = None, None
        for i in range(n):
            fl, img = self.cap.read()
            if img is None and self.path != 0: self.end(self)
        if not fl: return
        self.img = pg.image.frombuffer(img.tobytes(), img.shape[1::-1], "BGR")
        self.pTime = time.time()

    def step(self, path, end=lambda: 0):
        self.release()
        self.__init__(path, end)

    def release(self):
        self.cap.release()

class System:
    def __init__(self, app):
        self.os = os.name
        self.app = app
        self.clips = {}

    def loadClipPack(self, datas):
        for data in datas:
            texPath = ''
            if data[0] != 0:
                if self.os == 'posix': texPath = f'./accets/clips/{data[0]}'
                elif self.os == 'nt': texPath = f'accets\\clips\\{data[0]}'
            else: texPath = 0
            self.clips[data[1]] = Clip(texPath, data[2])

    def release(self):
        [clip.release() for clip in self.clips.values()]