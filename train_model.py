import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Load dataset
data = pd.read_csv("house_data.csv")

print("Dataset loaded successfully!")
print(data.head())


# Features
X = data[
    [
        "area",
        "bedrooms",
        "bathrooms",
        "floors",
        "age"
    ]
]

# Target
y = data["price"]


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Create model
model = LinearRegression()


# Train model
model.fit(X_train, y_train)

print("Model trained successfully!")


# Predictions
y_pred = model.predict(X_test)


# Evaluation
mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

rmse = mse ** 0.5

r2 = r2_score(y_test, y_pred)


print("\nModel Evaluation")
print("-------------------------")
print("MAE :", mae)
print("MSE :", mse)
print("RMSE:", rmse)
print("R2  :", r2)


# Save model
joblib.dump(model, "house_price_model.pkl")

print("\nModel saved successfully!")
print("house_price_model.pkl created.")