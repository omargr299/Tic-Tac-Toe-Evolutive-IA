from elements2 import *
from time import sleep
import threading as th

childs = []
def Main(game:Game):
    global childs
    rounds  = 30
    for i in range(rounds):
        print(f"---- {game.name} Start {i+1} ----")
        while(len(game.board.pos)>0):
            winner = game.Move()

            pg.display.update()

            if winner!=0:

                if winner==1: 
                    game.p1.victories+=1
                    childs.append(game.p1.weights)
                    childs.append(game.p1.weights)

                game.End()
                break
            else:
                childs.append(game.p1.weights)

            for event in pg.event.get():
                if event.type == pg.QUIT: exit()

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

    print(f"************ {game.name} wins%: {game.p1.victories/rounds}% ************ ")
    Save()
        

def Save():
    gamessorted = sorted(games,key=lambda x: x.p1.victories,reverse=True)
    gamessorted[0].p1.Save("best.h5")
    
        
pg.init()

w,h=450,450
wnd = pg.display.set_mode((w,h))

games:list[Game] = []
count = 0
for i in range(3):
    for j in range(3):
        games.append(Game(wnd,(w//3)*j,(h//3)*i,count))
        wnd.blit(games[i+j].board.surface,((w//3)*j,(h//3)*i))
        games[count].board.DrawnBoard()
        count+=1

#print(games)

pg.display.update()

for i in range(9):
    t = th.Thread(target=Main,args=(games[i],))
    t.start()

print("Done")
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

    