import pandas as pd # Zum Laden und Manipulieren von Daten.
import matplotlib.pyplot as plt # Zum Erstellen von Visualisierungen, insbesondere für die Korrelationsmatrix.
import seaborn as sns # Zum Erstellen einer Heatmap.
from sklearn.model_selection import train_test_split # Zum Aufteilen der Daten in Trainings- und Testsets.
from sklearn.linear_model import LinearRegression # Zum Erstellen eines linearen Regressionsmodells.
from sklearn.metrics import mean_squared_error, r2_score # Zum Bewerten des linearen Regressionsmodells.

def load_data(filepath): # Lädt die Daten aus einer CSV-Datei in ein DataFrame.
    return pd.read_csv(filepath)

def preprocess_data(data): # Bereitet die Daten vor: entfernt Spalten ohne Daten und ersetzt fehlende Werte in numerischen Spalten.
    data_clean = data.dropna(axis=1, how='all')
    numerical_columns = data_clean.select_dtypes(include=['float64', 'int64']).columns
    data_clean[numerical_columns] = data_clean[numerical_columns].fillna(data_clean[numerical_columns].median()) # Füllt fehlende Werte mit dem Median.
    return data_clean

def plot_correlation_matrix(data, features): # Erstellt eine Korrelationsmatrix für die angegebenen Merkmale.
    correlation_matrix = data[features].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Correlation Matrix of Features')
    plt.show()

def fit_linear_regression(X, y): # Passt ein lineares Regressionsmodell an die Daten an.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return model, mse, r2

def main(): # Main-Funktion, die die anderen Funktionen steuert.
    data = load_data('./qgis_output_csv/Wohnungen_mit_Laerm.csv') # Lädt Daten.
    data_clean = preprocess_data(data) # Bereitet Daten vor.

    plot_correlation_matrix(data_clean, ['Zimmer', 'Quadratmet', 'Preis', 'LEVEL_DB']) # Zeigt Korrelationsmatrix.

    X = data_clean[['Zimmer', 'Quadratmet', 'LEVEL_DB']] # Merkmale für das Modell.
    y = data_clean['Preis'] # Zielvariable für das Modell.
    model, mse, r2 = fit_linear_regression(X, y) # Führt lineare Regression durch und erhält Modellmetriken.

    print(f"Mean Squared Error: {mse}") # Gibt den MSE aus.
    print(f"R^2 Score: {r2}") # Gibt R²-Wert aus.

if __name__ == "__main__":
    main() # Führt die Hauptfunktion aus, wenn das Skript direkt aufgerufen wird.
