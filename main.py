import keras.optimizers
from keras.models import Sequential
from keras.layers import Dense

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import root_mean_squared_error
from math import sqrt
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("restaurant_revenue.xlsx")
data = []
for a in df["Cuisine_Type"]:
    if a not in data:
        data.insert(len(data), a)
n = 0
for a in df["Cuisine_Type"]:
    x = 1
    for b in data:
        if a == b:
            df.loc[n, "Cuisine_Type"] = x

            n += 1
            break
        x += 1
X = df.drop("Monthly_Revenue", axis=1)
y = df["Monthly_Revenue"]



Scaler = StandardScaler()
X_scaled = Scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
print(y_test)




model = Sequential()
model.add(Dense(64, activation='relu', input_dim=X_train.shape[1]))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear'))

model.compile(optimizer=keras.optimizers.Adam(0.01), loss="mean_squared_error")
history = model.fit(X_train, y_train, epochs= 10, batch_size=32, validation_split = 0.1)
plt.plot(history.history['loss'], label = 'training loss')
plt.plot(history.history['val_loss'], label = 'validation loss')
plt.xlabel("epoch")
plt.ylabel("loss")
plt.title("training and validation loss")
plt.show()

y_pred = model.predict(X_test)
print(y_test)
print("prediction:")
print(y_pred)

rmse = root_mean_squared_error(y_test, y_pred)
print(f"rmse: {rmse}")

