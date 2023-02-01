from elements2 import *
from time import sleep
import threading as th

def Main(game):
    while(len(game.board.pos)>0):
        winner = game.Move()

        pg.display.update()

        if winner!=0:
                game.End()
                sleep(3)
                break

    for event in pg.event.get():
        if event.type == pg.QUIT: exit()

    sleep(1)
        
pg.init()

w,h=450,450
wnd = pg.display.set_mode((w,h))

games:list[Game] = []
count = 0
for i in range(3):
    for j in range(3):
        games.append(Game(wnd,(w//3)*j,(h//3)*i))
        wnd.blit(games[i+j].board.surface,((w//3)*j,(h//3)*i))
        games[count].board.DrawnBoard()
        count+=1

print(games)

pg.display.update()

for i in range(9):
    t = th.Thread(target=Main,args=(games[i],))
    t.start()
""" while(True):
    for i in range(9):
        winner = games[i].Move()

        pg.display.update()

        if winner!=0:
                games[i].End()
                sleep(3)
                break

    for event in pg.event.get():
        if event.type == pg.QUIT: exit()

    sleep(1)

games[0].board.Reset()
pg.display.update() """

    