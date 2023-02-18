import pygame as pg
from decor import *
from players import *

PIECE_COOLORS = (pg.Color(255,255,255,0),
                 pg.Color(0,0,255,0),
                 pg.Color(255,0,0,0))

class Panel(pg.sprite.Sprite):
    def __init__(self, x,y,w,h,*groups: pg.sprite.AbstractGroup) -> None:
        super().__init__(*groups)
        self.surface = pg.Surface((w,h))
        self.surface.fill(pg.Color(255,0,0,255))
        self.rect = pg.Rect(x,y,w,h)

class Cell(Panel):
    def __init__(self,w,h,*groups: pg.sprite.AbstractGroup) -> None:
        super().__init__(0,0,w,h,*groups)
        self.surface.fill(pg.Color(255,255,255,255))
        self.font = pg.font.Font(None,50)
        self.piece = 0
    
    def GetPiece(self):
        if self.piece == 0: return " " 
        elif self.piece == 1: return "X" 
        elif self.piece == -1: return "O" 

    def Put(self,piece:str,wnd:pg.Surface):
        self.piece = piece
        self.Render(wnd)
    
    def Render(self,wnd:pg.Surface):
        piece:pg.Surface = self.font.render(self.GetPiece(), 1, PIECE_COOLORS[self.piece])
        wnd.blit(piece,
                (self.rect.centerx - piece.get_width()//2,
                 self.rect.centery - piece.get_height()//2))

class Board(Panel):
    def __init__(self,wnd:pg.Surface,x,y,*groups: pg.sprite.AbstractGroup) -> None:
        super().__init__(x,y,wnd.get_width()//3,wnd.get_height()//3,*groups)
        self.root = wnd
        self.surface.fill(pg.Color(0,255,0,255))
        self.Reset()

    def GetCells(self):
        return [cell.piece for cell in self.cells]

    def Move(self,cell):
        #print( "Turn:", "IA" if self.turn==1 else "Random",
         #       " | ",
          #      "Cell:", cell,
           #     " | ",
            #    end=" ")

        if not cell in self.pos: 
            #print("*No disponible cell*")
            return (False,0)

        self.cells[cell].Put(self.turn,self.root)
        #print("Tab:",self.GetCells())
        self.pos.remove(cell)
        winner = self.Win()
        
        self.Turn()
        #decoratorLn("Turn Change")

        return (True,winner)
    
    def Turn(self):
        self.turn *= -1

    def Win(self):
        if(self.Check(0,1,2)): return self.turn
        if(self.Check(3,4,5)): return self.turn
        if(self.Check(6,7,8)): return self.turn
        if(self.Check(0,3,6)): return self.turn
        if(self.Check(1,4,7)): return self.turn
        if(self.Check(2,5,8)): return self.turn
        if(self.Check(0,4,8)): return self.turn
        if(self.Check(2,4,6)): return self.turn
        return 0

    def Check(self,a:int,b:int,c:int) -> int:
        cells = self.GetCells()
        if cells[a] == cells[b] == cells[c] == self.turn:
            self.DrawnWinLine(self.cells[a].rect.centerx, self.cells[a].rect.centery,
                              self.cells[c].rect.centerx, self.cells[c].rect.centery)
            return True
        return False

    def Reset(self):
        self.cells = [Cell(self.rect.width//3,self.rect.height//3) for _ in range(9)]
        self.pos = [i for i in range(9)]
        self.turn = 1

    def Place(self):
        x,y=0,0
        for i,cell in enumerate(self.cells):
            self.root.blit(cell.surface,(self.rect.x+x, self.rect.y+y))
            cell.rect.x = self.rect.x+x
            cell.rect.y = self.rect.y+y
            cell.update()
            x += cell.rect.width
            if not (i+1)%3:
                y += cell.rect.height
                x = 0

    def DrawLines(self):
        x1 = self.rect.width//3
        for i in range(2):
            pg.draw.line(self.root,
                        pg.Color(0,0,0,0),
                        (self.rect.x + x1*(i+1), self.rect.y + 5),
                        (self.rect.x + x1*(i+1), self.rect.y + self.rect.height - 5),
                        5)
        y1 = self.rect.height//3
        for i in range(2):
            pg.draw.line(self.root,
                        pg.Color(0,0,0,0),
                        (self.rect.x + 5, self.rect.y + y1*(i+1)),
                        (self.rect.x + self.rect.width - 5, self.rect.y + y1*(i+1)),
                        5)

    def DrawnWinLine(self,x1,y1,x2,y2):
        pg.draw.line(self.root,
                    pg.Color(0,255,0,0),
                    (x1,y1),
                    (x2,y2),
                    3)

    def DrawnBoard(self):
        self.Place()
        self.DrawLines()

class Game():
    def __init__(self,wnd,x,y,num) -> None:
        self.num = num
        self.name = "Game " + str(num)
        self.board = Board(wnd,x,y)
        self.p1 = AI()
        self.p2 = RandPlayer()

        #decoratorLn("Tic Tac Toe")

    def Move(self):
        if self.board.turn==1:
            player = self.p1
            inputs = self.board.GetCells()
        else:
            player = self.p2
            inputs = self.board.pos

        cell = player.Select(inputs,False)
        doit,winner = self.board.Move(cell)
        
        if winner: 
            print(self.name)
            print(f"The winner is {'IA' if winner>0 else 'Random Player'}\n")
            pass

        if not doit:
            player.Train(inputs,self.board.pos,False)

        return winner

    def End(self):

        decorator(f"{self.name} Ends")

if __name__=="__main__":
    pg.init()
    w,h=450,450
    wnd = pg.display.set_mode((w,h))

    boards = []
    count = 0
    for i in range(3):
        for j in range(3):
            boards.append(Board(wnd,(w//3)*j,(h//3)*i))
            wnd.blit(boards[i+j].surface,((w//3)*j,(h//3)*i))
            boards[count].DrawnBoard()
            count+=1

    #print(boards)

    pg.display.update()

    while(True):
        for i in range(9):
            cell = int(input("Celda: "))

            boards[i].Move(cell)

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT: exit()