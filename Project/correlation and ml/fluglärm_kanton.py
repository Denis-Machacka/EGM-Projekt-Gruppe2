import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def load_data(filepath):
    return pd.read_csv(filepath)

def preprocess_data(data):
    # Behalte nur die relevanten Spalten
    data = data[['Zimmer', 'Quadratmet', 'Preis', 'LEVEL_DB']]
    # Entferne fehlende Werte
    data = data.dropna()
    return data

def plot_correlation_matrix(data, features):
    correlation_matrix = data[features].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Correlation Matrix of Features')
    plt.show()

def fit_linear_regression(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return model, mse, r2

def main():
    # Load and preprocess data
    data = load_data('./qgis_output_csv/Fluglaerm_ganzerKanton.csv')
    data_clean = preprocess_data(data)

    # Plot correlation matrix
    plot_correlation_matrix(data_clean, ['Zimmer', 'Quadratmet', 'Preis', 'LEVEL_DB'])

    # Fit linear regression
    X = data_clean[['Zimmer', 'Quadratmet', 'LEVEL_DB']]  # Features
    y = data_clean['Preis']  # Target
    model, mse, r2 = fit_linear_regression(X, y)

    # Print model results
    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")

if __name__ == "__main__":
    main()
