from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error, accuracy_score
from math import sqrt
import pandas as pd


df = pd.read_excel("restaurant_revenue.xlsx")

# One-hot encode categorical variables
df = pd.get_dummies(df, columns=['Cuisine_Type'])

# Split the dataset into features (X) and target variable (y)
X = df.drop("Monthly_Revenue", axis=1)
y = df["Monthly_Revenue"]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, shuffle=True)

# Initialize the RandomForestRegressor

rf_regressor = RandomForestRegressor(n_estimators=250, random_state=42)

    # Train the RandomForestRegressor
rf_regressor.fit(X_train, y_train)

    # Make predictions on the test set
y_pred = rf_regressor.predict(X_test)



    # Evaluate the model using Mean Squared Error (MSE)
rmse = root_mean_squared_error(y_test, y_pred)

#import matplotlib.pyplot as plt
#plt.plot(range(1, 500), rmses)
#plt.xlabel("n_estimator")
#plt.ylabel("RMSE")
#plt.show()
print("Root Mean Squared Error:", rmse)