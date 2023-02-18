from decor import *
from players import *
import tensorflow as tf


class Board():
    def __init__(self) -> None:
        self.cells = [0 for _ in range(9)]
        self.pos = [i for i in range(9)]
        self.turn = 1

    def Move(self,cell):
        print( "Turn:", "IA" if self.turn==1 else "Random",
                " | ",
                "Cell:", cell,
                " | ",
                end=" ")

        if not cell in self.pos: 
            print("*No disponible cell*")
            return (False,0)

        self.cells[cell] =  self.turn
        print("Tab:",self.cells)
        self.pos.remove(cell)
        winner = self.Win()
        self.Turn()
        decoratorLn("Turn Change")

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
        if self.cells[a] == self.cells[b] == self.cells[c] == self.turn:
            return True
        return False

    def Reset(self):
        self.cells = [0 for _ in range(9)]
        self.pos = [i for i in range(9)]
        self.turn = 1

if __name__ == "__main__":
    def transform(cells:list[int]):
        return tf.constant(cells)

    br = Board()
    j1 = AI()
    j2 = RandPlayer()
    
    inputs = transform(br.cells)
    inputs = inputs[tf.newaxis,:]
    inputs = j1.l1(inputs)
    # print(inputs)
    inputs = j1.l2(inputs)
    i2 = inputs
    # print(inputs)
    inputs = j1.l3(inputs)
    print(inputs)
    print(type(j1.weights))
    newWeights = []
    print("-----------------")

    for i,w in enumerate(j1.weights):
        print(w.shape)
        newTensor = tf.Variable(tf.random.uniform(w.shape))
        print(newTensor)
        newWeights.append(newTensor)
        print("-----------------")
    print(len(newWeights))
    j1.set_weights(newWeights)
    suma = 0
    values=list(zip(j1.l3.weights[0].numpy(),i2[0].numpy()))
    for w,i in values:
        suma+=w[0]*i
    suma+=j1.l3.bias
    print(suma)
