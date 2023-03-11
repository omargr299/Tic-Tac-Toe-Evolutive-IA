from elements2 import *
from time import sleep
import threading as th
from sys import exit
from os import path

childs = []
loop  = True

def Main(game:Game):
    global childs, loop
    rounds  = 20
    for i in range(rounds):
        print(f"---- {game.name} Start {i+1} ----")
        while(len(game.board.pos)>0 and loop):
            winner = game.Move()

            if(loop): pg.display.update()
            else: exit()

            if winner!=0:

                if winner==1: 
                    game.p1.victories+=1
                    childs.append(game.p1.weights)
                    childs.append(game.p1.weights)

                game.End()
                break
            else:
                childs.append(game.p1.weights)

        sleep(0.5)
        game.board.Reset()
        game.board.DrawnBoard()

        victories = game.p1.victories
        print("<<<<<<<",f"{game.name} wins: ",game.p1.victories,">>>>>>>")
        game.p1 = AI()
        inputs = tf.constant(game.board.GetCells())
        game.p1(inputs,False)
        if childs:
            game.p1.set_weights(childs[0])
            childs.pop(0)
            game.p1.victories = victories
    print(f"************ {game.name} wins%: {(game.p1.victories/rounds)*100}% ************ ")
        

def Save():
    gamessorted = sorted(games,key=lambda x: x.p1.victories,reverse=True)
    gamessorted[0].p1.save("best.h5")
    
        
pg.init()

w,h=450,450
wnd = pg.display.set_mode((w,h))

games:list[Game] = []
count = 0
for i in range(3):
    for j in range(3):
        games.append(Game(wnd,(w//3)*j,(h//3)*i,count))
        if(path.exists('best.index')): 
            print(f"Loading weights to game {count}...")
            games[count].p1.load_weights('best')
        wnd.blit(games[i+j].board.surface,((w//3)*j,(h//3)*i))
        games[count].board.DrawnBoard()
        count+=1

#print(games)

pg.display.update()

for i in range(9):
    t = th.Thread(target=Main,args=(games[i],))
    t.start()

while(loop):
    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            loop = False
            break


print("Saving...")
best = max(games,key=lambda x: x.p1.victories)
best.p1.save_weights("best",save_format="tf")

    