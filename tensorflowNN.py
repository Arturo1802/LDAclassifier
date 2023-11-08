import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from LDAtools import getT2DataSQL, getFullDataSQL
from sklearn.model_selection import train_test_split

class ComplexModel2(tf.keras.Model):
    def __init__(self, in_features=6, h1=12, h2=12, h3=3, h4=2, out_features=3):
        super(ComplexModel2, self).__init__()
        self.fc1 = tf.keras.layers.Dense(h1, activation='relu')
        self.fc2 = tf.keras.layers.Dense(h2, activation='relu')
        self.fc3 = tf.keras.layers.Dense(h3, activation='relu')
        self.fc4 = tf.keras.layers.Dense(h4, activation='relu')
        self.dropout = tf.keras.layers.Dropout(0.2)
        self.out = tf.keras.layers.Dense(out_features)

    def call(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.dropout(x)
        x = self.fc3(x)
        x = self.fc4(x)
        x = self.out(x)
        return x
# Definir el modelo en TensorFlow
class ComplexModel(tf.keras.Model):
    def __init__(self, in_features=6, h1=12, h2=12, h3=3, h4=2, out_features=3):
        super(ComplexModel, self).__init__()
        self.fc1 = tf.keras.layers.Dense(h1, activation='relu')
        self.fc2 = tf.keras.layers.Dense(h2, activation='relu')
        self.fc3 = tf.keras.layers.Dense(h3, activation='relu')
        self.fc4 = tf.keras.layers.Dense(h4, activation='relu')
        self.dropout = tf.keras.layers.Dropout(0.2)
        self.out = tf.keras.layers.Dense(out_features)

    def call(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.dropout(x)
        x = self.fc3(x)
        x = self.fc4(x)
        x = self.out(x)
        return x

# Crear una instancia del modelo
model = ComplexModel2()

# Cargar datos
df = getFullDataSQL()
X = df.drop('preinf', axis=1).drop('#AUTHID', axis=1).drop('TEXT', axis=1).drop('finalinf', axis=1)
y = df['preinf']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Convertir los datos a tensores de TensorFlow
X_train = tf.round(tf.constant(X_train.values, dtype=tf.float32),2) 
X_test = tf.round(tf.constant(X_test.values, dtype=tf.float32),2)
y_train = tf.constant(y_train.values, dtype=tf.int64)
y_test = tf.constant(y_test.values, dtype=tf.int64)

# Función de pérdida y optimizador
criterion = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)

# Entrenamiento del modelo
losses = []
i = -1
loss = 1

try:
    model.load_weights("model_weights.h5")
except:
    model.build((None, X_train.shape[1]))
    model.compile(optimizer=optimizer, loss=criterion)

while loss > 0.20:
    i += 1
    with tf.GradientTape() as tape:
        y_pred = model(X_train)
        loss = criterion(y_train, y_pred)
        losses.append(loss.numpy())
    
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    if i % 10 == 0:
        print(f'Epoch: {i}, Loss: {loss}')

    if i % 1000 == 0:
        if losses[-1] <= losses[0] * 0.95:
            print("SAVING MODEL")
            model.save_weights("model_weights.h5")

        losses = []
