import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

class Model(tf.keras.Model):
    def __init__(self) -> tf.keras.Model:
        super().__init__()
        self.l1 = tf.keras.layers.Dense(units=1,
                                        activation=tf.nn.relu,
                                        kernel_initializer=tf.random.normal,
                                        bias_initializer=tf.random.normal                               )
        self.l2 = tf.keras.layers.Dense(units=10,
                                        activation=tf.nn.relu,
                                        kernel_initializer=tf.random.normal,
                                        bias_initializer=tf.random.normal)(self.l1)
        self.l3 = tf.keras.layers.Dense(units=1,
                                        activation=tf.nn.relu,
                                        kernel_initializer=tf.random.normal,
                                        bias_initializer=tf.random.normal)(self.l2)

    def call(self,x:tf.Tensor):
        x = x[:,tf.newaxis]
        print(x)
        x = self.l1(x)
        return tf.squeeze(x,axis=1)

pul = lambda x: x.numpy()*2.54

model = Model()

x = tf.linspace(0,10,100)
y = pul(x)
model(x)

var = model.variables
print(var)
opt = tf.optimizers.Adam(learning_rate=0.01)

epoch = []
for step in range(1):
    with tf.GradientTape() as tape:
        pred = model(x)
        err = (y-pred)**2
        mean_err = tf.reduce_mean(err)
        print(pred,err)
    grad = tape.gradient(mean_err,var)
    # print(grad)
    opt.apply_gradients(zip(grad,var))

    epoch.append([step,mean_err.numpy()])

    if mean_err<0.001: break
    if step % 100 == 0:
        print(f'Mean squared error: {mean_err.numpy():0.3f}')

# print(y)
# print(model(x))

epoch = np.array(epoch)

plt.plot(epoch[:,0],epoch[:,1])
plt.xlabel("epoch")
plt.ylabel("loss MSE")
plt.show()