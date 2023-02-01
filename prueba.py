import pygame as pg

class Panel(pg.sprite.Sprite):
    def __init__(self, w,h,*groups: pg.sprite.AbstractGroup) -> None:
        super().__init__(*groups)
        self.surface = pg.Surface((w,h))
        self.surface.fill(pg.Color(255,0,0,255))
        self.rect = pg.Rect(0,0,w,h)

class Cell(Panel):
    def __init__(self,w,h,*groups: pg.sprite.AbstractGroup) -> None:
        super().__init__(w,h,*groups)
        self.surface.fill(pg.Color(255,0,0,255))
        self.font = pg.font.Font(None,50)

    def Put(self,piece:str,wnd):
        piece:pg.Surface = self.font.render(piece, 1, (0,0,0))
        print(self.rect.centerx )
        print(self.rect.centerx - piece.get_width())
        wnd.blit(piece,
                (self.rect.centerx - piece.get_width()//2,
                 self.rect.centery - piece.get_height()//2))


class Board(Panel):
    def __init__(self,wnd:pg.Surface,*groups: pg.sprite.AbstractGroup) -> None:
        super().__init__(wnd.get_width()//3,wnd.get_height()//3,*groups)
        self.root = wnd
        self.surface.fill(pg.Color(255,255,255,255))
        self.cells:list[Cell] = [Cell(self.rect.width//3,self.rect.height//3) for _ in range(9)]

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
    
    def Move(self,piece:str,cell:int):
        self.cells[cell].Put(piece,self.root)


    def DrawLines(self,wdn:pg.Surface):
        pg.draw.line()

pg.init()
w,h=450,450
wnd = pg.display.set_mode((w,h))

br = Board(wnd)
wnd.blit(br.surface,(0,0))
br.Place()

for i in range(9):
    br.Move("X",i)


# wnd.blit(br.cells[0].surface,(0,0))

while(True):

    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT: exit()