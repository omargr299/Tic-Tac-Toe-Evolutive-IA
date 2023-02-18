from elements import *
from players import *
from time import sleep
from decor import *

class Game():
    def __init__(self) -> None:
        self.board = Board()
        self.p1 = AI()
        self.p2 = RandPlayer()

        decoratorLn("Tic Tac Toe")

    def Move(self):
        if self.board.turn==1:
            player = self.p1
            inputs = self.board.cells
        else:
            player = self.p2
            inputs = self.board.pos

        cell = player.Select(inputs)
        doit,winner = self.board.Move(cell)
        
        if winner: print(f"The winner is {'IA' if winner>0 else 'Random Player'}\n")

        if not doit:
            player.Train(inputs,self.board.pos)

        return winner

    def End(self):
        decorator("Game Ends")

if __name__=="__main__":
    game = Game()
    game2 = Game()
    game.Move()

    while(len(game.board.pos)>0):
        game.Move()
        sleep(1)
        
    game.End()