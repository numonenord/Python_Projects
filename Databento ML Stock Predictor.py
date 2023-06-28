import databento as db
from datetime import datetime, timedelta
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import warnings
import time

"""
ML STOCK PREDICTION PROGRAM

Fetches historical stock price data from the Databento Historical API and uses machine learning to predict
the closing price for a given symbol in recent weeks.

The program uses a linear regression model to do predictions. The input features include the symbols' open, high,
and low prices, as well as trade volume and technical indicators (vwap and rsi) from the stock's previous days of
trading data. The output feature is the closing price of the next day. Uses 30 days of trades data for training by
default.

The program fetches the data, cleans it, trains the model, and makes predictions. The results are then visualized
side by side with the actual prices for the day of the prediction. The model continues to fetch and train
data until it meets or exceeds an accuracy threshold determined by a user-configurable R-squared value.
"""

# user-configurable variables
CHOSEN_DATASET = "XNAS.ITCH"  # dataset to fetch from
NUM_DAYS = 30  # number of days of training data
ACCURACY_THRESHOLD = 0.8  # the minimum acceptable R squared value
IGNORE_WARNINGS = True  # show or hide warnings
DEFAULT_API_KEY = ""  # default api key to use for fetching data

if IGNORE_WARNINGS:
    warnings.filterwarnings("ignore", category=db.common.error.BentoWarning)

# handles user input with an option to exit
def input_handler(prompt):
    user_input = input(prompt).strip()
    if user_input.lower() == "exit":
        print("Exiting the application...")
        exit()
    return user_input

# creates Databento client
def create_client(api_key):
    return db.Historical(api_key)

# checks whether symbol is valid and creates datafram for stock data
def check_symbol(client, symbol, num_days):
    end_date = get_dataset_range(client, CHOSEN_DATASET)
    start_date = end_date - timedelta(days=num_days)

    try:
        data = client.timeseries.get_range(
            dataset=CHOSEN_DATASET,
            start=start_date.strftime("%Y-%m-%d"),
            end=end_date.strftime("%Y-%m-%d"),
            symbols=symbol,
            stype_in="raw_symbol",
            schema="ohlcv-1d",
        ).to_df()
        return data
    except:
        print("Could not find symbol.")
        return None

# fetches data from the Databento API
def fetch_data(data):
    return data

# gets the available date range for the chosen dataset
def get_dataset_range(client, dataset):
    available_range = client.metadata.get_dataset_range(dataset=dataset)
    end = available_range["end_date"]
    return datetime.strptime(end, "%Y-%m-%d")

# prepares the dataframe by adding required columns and calculations
def prepare_dataframe(df):
    df["pvt"] = (
        df[["open", "high", "close"]].mean(axis=1) * df["volume"]
    )
    df["vwap"] = df["pvt"].cumsum() / df["volume"].cumsum()
    df["up"] = (df["close"] - df["open"]).clip(lower=0)
    df["down"] = (df["open"] - df["close"]).clip(lower=0)

    # using a moving average
    df["rs"] = (
        df["up"].rolling(5).mean() / df["down"].rolling(5).mean()
    )
    df["rsi"] = 100 - (100 / (1 + df["rs"]))

    return pd.DataFrame({
        "open": df["open"],
        "high": df["high"],
        "low": df["low"],
        "close": df["close"],
        "volume": df["volume"],
        "rsi": df["rsi"],
        "vwap": df["vwap"],
    })

# splits the dataframe into training and test sets, performs imputation to fill missing values
def get_train_test(df):
    X = df[["open", "high", "low", "volume", "vwap", "rsi"]]
    y = df["close"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # imputation to fill missing values
    imputer = SimpleImputer(strategy="mean")
    X_train = pd.DataFrame(imputer.fit_transform(X_train), columns=X.columns, index=X_train.index)
    X_test = pd.DataFrame(imputer.transform(X_test), columns=X.columns, index=X_test.index)

    return X_train, X_test, y_train, y_test

# trains the linear regression model
def get_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

# uses the trained model to make predictions
def get_prediction(model, X_test):
    return model.predict(X_test)

# prepares the data for plotting
def get_stock_data_to_plot(df, X_test, y_test, y_pred):
    df_test = pd.DataFrame(X_test[-14:], columns=df.columns.drop('close'), index=X_test.index[-14:])
    df_test["Actual"] = y_test.values[-14:]
    df_test["Predicted"] = y_pred[-14:]
    return df_test

# plots the data
def plot_data(df, symbol, num_days, mse, r2):
    df[["Actual", "Predicted"]].plot(figsize=(14, 7))
    plt.title(f"Actual vs Predicted Close Prices For {symbol} Over Previous Weeks", size=16)
    plt.xlabel("Date")
    plt.ylabel("Price in USD")
    plt.xticks(rotation=45)
    plt.figtext(0.515, 0.85, "Mads I. Feiring", size = 10, ha="center")
    plt.figtext(0.5, 0.02, f"R squared: {r2:.2f} | Number of days used for training: {num_days}", size=12, ha="center")
    plt.legend()
    plt.grid(True)
    plt.show()
    print("Exiting the application...")

# fetches data, trains the model, and evaluates it. If the model's performance is not satisfactory, the process is repeated with an extended training period.
def fetch_and_train_model(client, symbol, dataset, num_days, data):
    satisfactory = False
    try:
        data = fetch_data(data)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None, num_days, satisfactory

    data = prepare_dataframe(data)
    X_train, X_test, y_train, y_test = get_train_test(data)
    model = get_model(X_train, y_train)
    y_pred = get_prediction(model, X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    if r2 >= ACCURACY_THRESHOLD:
        satisfactory = True

    try:
        df_test = get_stock_data_to_plot(data, X_test, y_test, y_pred)
    except Exception as e:
        print(f"An error occurred during plotting: {e}")
        return None, None, None, num_days, satisfactory

    return df_test, r2, mse, num_days, satisfactory

def main(num_days=NUM_DAYS):    
    print("(typing 'exit' will stop the program)")

    while True: # handles wrong api key
        api_key = input_handler("Enter Databento API key, or hit enter to use default key: ")
        if not api_key and DEFAULT_API_KEY != "":
            api_key = DEFAULT_API_KEY
        elif not api_key and DEFAULT_API_KEY == "":
            print("No default API key is given. Please provide your own key.")
            continue
        client = create_client(api_key)
        symbol = input_handler("Enter a symbol you want to investigate: ").upper()
    
        try:
            data = check_symbol(client, symbol, num_days)
            break
        except:
            print("Invalid API Key. Please try again.")
    
    while data is None: # handles wrong symbol
        symbol = input_handler("Enter a valid symbol you want to investigate: ").upper()
        data = check_symbol(client, symbol, num_days)

    print("Processing...")

    try: # if this fails, it is because we have incomplete data for symbol
        df_test, r2, mse, num_days, satisfactory = fetch_and_train_model(client, symbol, CHOSEN_DATASET, num_days, data)
    except:
        print(f"There is incomplete data available for the symbol {symbol}. Please try another symbol.")
        print("Exiting the program...")
        exit(1)

    while not satisfactory: # we do not want to exceed a year of training data
        if num_days > 365:
            print("It was not possible to achieve satisfactory accuracy for the given symbol.")
            exit()

        # add 10 days to training data if we get a an r squared value that is too low
        num_days += 10
        data = check_symbol(client, symbol, num_days)
        df_test, r2, mse, num_days, satisfactory = fetch_and_train_model(client, symbol, CHOSEN_DATASET, num_days, data)

    # plot findings
    plot_data(df_test, symbol, num_days, mse, r2)

if __name__ == "__main__":
    main()
