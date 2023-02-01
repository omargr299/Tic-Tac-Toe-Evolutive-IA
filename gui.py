import pygame as pg
from sys import exit
from time import sleep
from main import *

def DrawO(wstart,hstart):
    pg.draw.ellipse(wdn, O_COLOR, pg.Rect(wstart-WFIG, hstart-HFIG, WRECT-MARGIN*2, HRECT-MARGIN*2), FIG_WEIGHT)

def DrawX(wstart,hstart):
    pg.draw.line(wdn,X_COLOR,(wstart+MARGIN*4, hstart+MARGIN*4),(wstart+WRECT-MARGIN*2, hstart+HRECT-MARGIN*2),BRD_WEIGHT)
    pg.draw.line(wdn,X_COLOR,(wstart+WRECT-MARGIN*2, hstart+MARGIN*4),(wstart+MARGIN*4, hstart+HRECT-MARGIN*2),BRD_WEIGHT)

def DeleteFigs():
    for i in range(0,201,100):
        for j in range(0,201,100):
            pg.draw.rect(wdn,BG_COLOR, pg.Rect(i, j, i+WRECT, j+HRECT))
    DrawBoard(0)

def DrawBoard(distance):
    pg.draw.line(wdn,BRD_COLOR,(distance+WTHIRD,MARGIN),(distance+WTHIRD,H-MARGIN),BRD_WEIGHT)
    pg.draw.line(wdn,BRD_COLOR,(distance+WTHIRD*2,MARGIN),(distance+WTHIRD*2,H-MARGIN),BRD_WEIGHT)

    pg.draw.line(wdn,BRD_COLOR,(distance+MARGIN,HTHIRD),(distance+W+MARGIN,HTHIRD),BRD_WEIGHT)
    pg.draw.line(wdn,BRD_COLOR,(distance+MARGIN,HTHIRD*2),(distance+W+MARGIN,HTHIRD*2),BRD_WEIGHT)

def UpdateCells(board):
    cell = 0
    for i in range(0,201,100):
        for j in range(0,201,100):
            if board[cell]==-1: DrawO(WSIXTH+(j),HSIXTH+(i)) 
            elif board[cell]==1: DrawX(j,i)
            cell+=1

BG_COLOR = pg.Color(255,255,255,255)
BRD_COLOR = pg.Color(0,0,0,255)
O_COLOR = pg.Color(255,0,0,255)
X_COLOR =  pg.Color(0,0,255,255)

BRD_WEIGHT = 10
FIG_WEIGHT = 5

size = (300,300)
W,H = size

WHALF, HHALF = (W//2,H//2) 
WTHIRD, HTHIRD = (W//3,H//3)
WSIXTH, HSIXTH = (WTHIRD//2,HTHIRD//2)

WRECT, HRECT = (W//3-BRD_WEIGHT,H//3-BRD_WEIGHT)
MARGIN = BRD_WEIGHT//2

WFIG = WRECT//2 - MARGIN
HFIG = HRECT//2 - MARGIN

pg.init()
wdn = pg.display.set_mode(size)  
wdn.fill(BG_COLOR)

DrawBoard(0)

game = Game()
pg.display.update()

games = 0
while(games<10):
    while(len(game.board.pos)>0):

        winner = game.Move()
        UpdateCells(game.board.cells)

        pg.display.update()
        
        if winner!=0:
            game.End()
            sleep(3)
            break

        for event in pg.event.get():
            if event.type == pg.QUIT: exit()

        sleep(1)

    game = Game()
    DeleteFigs()
    UpdateCells(game.board.cells)
    pg.display.update()
    games+=1

exit()