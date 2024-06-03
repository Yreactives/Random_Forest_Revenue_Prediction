import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset into a DataFrame
data = {
    'Color': ['Red', 'Yellow', 'Red', 'Green', 'Yellow', 'Green', 'Yellow', 'Red'],
    'Diameter (cm)': [7.5, 6.2, 6.8, 5.5, 7.0, 5.8, 7.2, 7.1],
    'Type': ['Apple', 'Banana', 'Apple', 'Kiwi', 'Banana', 'Kiwi', 'Banana', 'Apple']
}

df = pd.DataFrame(data)

# Convert categorical variables to numerical using one-hot encoding
df = pd.get_dummies(df, columns=['Color'])

# Split the dataset into features (X) and target variable (y)
X = df.drop(columns=['Type'])
y = df['Type']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the Random Forest classifier
rf_classifier.fit(X_train, y_train)

# Make predictions on the test set
y_pred = rf_classifier.predict(X_test)

# Evaluate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Print classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))