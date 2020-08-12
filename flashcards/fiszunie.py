# -*- coding: utf-8 -*-
import csv
import pygame
import random
import pandas as pd

pygame.init()
X = 1500
Y = 500
win = pygame.display.set_mode((X,Y))
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 128)
data = pd.read_csv('book2.txt', sep=",", header=None)
data.columns = ["niemiecki", "polski"]



def napis_wyswietl(a,b):
    win.fill(white)
    pygame.display.set_caption("Fiszki")
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(data.values[a][b], True, black, white)
    textRect = text.get_rect()
    textRect.center = (X // 2, Y // 2)
    win.blit(text, textRect)
    pygame.display.update()

a = 250
k = 0
lista = []
run = True
napis = False
while run:

    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        napis = True
    if (napis):
        napis_wyswietl(a,0)
    else:
        napis_wyswietl(a,1)

    if keys[pygame.K_UP]:
        napis = False
        if (napis):
            napis_wyswietl(a, 0)
        else:
            napis_wyswietl(a, 1)

    if keys[pygame.K_RIGHT]:
        a = a + 1
        print(a)
        '''a = a + random.randint(0,5)
        lista.append(a)
        if a in lista:
            a = a - random.randint(0,5)
        if a>200:
            a = a - random.randint(0, 10)
        if a<100:
            a = a + random.randint(0,5)
        print(lista)
        '''
        napis = False
    if keys[pygame.K_LEFT]:
        a = a - 1
        napis = False
    if keys[pygame.K_RETURN]:
        lista.append(a)
        print(lista)
    if keys[pygame.K_ESCAPE]:
        if(len(lista)>0):
                a = lista[k]
                k = k + 1



    pygame.display.update()


pygame.quit()