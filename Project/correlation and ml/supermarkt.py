import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def load_and_prepare_data(filepath):
    # Daten laden
    data = pd.read_csv(filepath)
    
    # Spalten mit ausschließlich fehlenden Werten entfernen
    data_clean = data.dropna(axis=1, how='all')
    
    # Sicherstellen, dass die relevanten Spalten keine fehlenden Werte enthalten
    features = ['Preis', 'distance']
    data_clean = data_clean.dropna(subset=features)
    
    return data_clean

def plot_correlation_matrix(data):
    correlation_matrix = data[['Preis', 'distance']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
    plt.title('Korrelationsmatrix der Merkmale')
    plt.show()

def perform_linear_regression(data):
    X = data[['distance']]  # Prädiktor
    y = data['Preis']  # Zielvariable
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    return mse, r2

def main():
    data = load_and_prepare_data('./qgis_output_csv/Wohnungen_Supermarket.csv')
    plot_correlation_matrix(data)
    mse, r2 = perform_linear_regression(data)
    
    print(f'Mean Squared Error: {mse}')
    print(f'R^2 Score: {r2}')

if __name__ == "__main__":
    main()
