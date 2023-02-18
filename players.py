import tensorflow as tf
from tensorflow import Tensor,constant,GradientTape,optimizers,losses,random,nn,newaxis
from keras import Model
from keras.layers import Dense
from random import choice,uniform
from decor import *

class AI(Model):
    def __init__(self,victories=0):
        super(AI,self).__init__()
        self.victories = victories


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

        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            try:
                # Currently, memory growth needs to be the same across GPUs
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                logical_gpus = tf.config.list_logical_devices('GPU')
                print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
            except RuntimeError as e:
                # Memory growth must be set before GPUs have been initialized
                print(e)

    def call(self, inputs,verbose) -> Tensor:
        inputs = inputs[newaxis,:]
        y = self.l1(inputs)
        y = self.l2(y)
        y = self.l3(y)
        if verbose: print("AI prediction:",y[0][0].numpy()," ~ ",round(y[0][0].numpy()))
        return y

    def Select(self,inputs: list[int],verbose=True) -> int:
        inputs = constant(inputs)
        outputs = self.call(inputs,verbose)
        return round(float(outputs[0][0]))

    def VarWeights(self):
        newWeights = []

        for i,w in enumerate(self.weights):
            newTensor = tf.Variable(tf.random.uniform(w.shape))
            newTensor.assign_add(newTensor+w)
            newWeights.append(newTensor)

        self.set_weights(newWeights)

    def fit(self,inputs:Tensor,pos:int,verbose:bool):
        if verbose: print(f"Expedted output: {pos}",end=" | ")
        with GradientTape() as tape:
            if verbose: print("  trainning",end=" ")
            pred = self(inputs,verbose)
            err = self.mse(pos,pred)
        
        grad = tape.gradient(err,self.trainable_variables)

        if(self.check(grad)):
            if verbose: print("todos son 0")
            self.VarWeights()
            
        self.opt.apply_gradients(zip(grad,self.trainable_variables))
    
    
    def Train(self,inputs: list[int], pos:list[int],verbose=True) -> int:
        inputs = constant(inputs)
        if verbose: decoratorLn("Trainning..")
        cell = choice(pos)

        for _ in range(10):
            self.fit(inputs,cell,verbose)
        if verbose: print()


    def check(self,grads):
        counts = 0

        for g in grads:
            if not tf.reduce_sum(g):
                counts+=1
        
        if counts == len(grads): return True

        return False

    
class RandPlayer():

    def Select(self,pos,verbose=True) -> int:
        return choice(pos)


