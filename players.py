import tensorflow as tf
from tensorflow import Tensor,constant,GradientTape,optimizers,losses,random,nn,newaxis
from keras import Model
from keras.layers import Dense
from random import choice,uniform
from decor import *

class IA(Model):
    def __init__(self):
        super(IA,self).__init__()
        self.l1 = Dense(9,
                        nn.relu,
                        kernel_initializer=random.uniform,
                        bias_initializer=random.uniform)
        
        self.l2  = Dense(16,
                        nn.relu,
                        kernel_initializer=random.uniform,
                        bias_initializer=random.uniform)

        self.l3 = Dense(1,
                        nn.relu,
                        kernel_initializer=random.uniform,
                        bias_initializer=random.uniform)
        
        self.opt =  optimizers.Adam(0.05)
        self.mse = losses.MeanSquaredError()

    def call(self, inputs) -> Tensor:
        inputs = inputs[newaxis,:]
        y = self.l1(inputs)
        y = self.l2(y)
        y = self.l3(y)
        print("IA prediction:",y[0][0].numpy()," ~ ",round(y[0][0].numpy()))
        return y

    def Select(self,inputs: list[int]) -> int:
        inputs = constant(inputs)
        outputs = self.call(inputs)
        return round(float(outputs[0][0]))

    def VarWeights(self):
        newWeights = []

        for i,w in enumerate(self.weights):
            print(w.shape)
            newTensor = tf.Variable(tf.random.uniform(w.shape))
            print(newTensor)
            newWeights.append(newTensor)

        self.set_weights(newWeights)

    def fit(self,inputs:Tensor,pos:int):
        print(f"Expedted output: {pos}",end=" | ")
        with GradientTape() as tape:
            print("  trainning",end=" ")
            pred = self(inputs)
            err = self.mse(pos,pred)
        
        grad = tape.gradient(err,self.trainable_variables)

        if(self.check(grad)):
            print("todos son 0")
            self.VarWeights()
            
        self.opt.apply_gradients(zip(grad,self.trainable_variables))
    
    
    def Train(self,inputs: list[int], pos:list[int]) -> int:
        inputs = constant(inputs)
        decoratorLn("Trainning..")
        cell = choice(pos)

        for _ in range(10):
            self.fit(inputs,cell)
        print()


    def check(self,grads):
        counts = 0

        for g in grads:
            if not tf.reduce_sum(g):
                counts+=1
        
        if counts == len(grads): return True

        return False

    
class RandPlayer():

    def Select(self,pos):
        return choice(pos)


