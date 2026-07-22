from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, Input, LSTM
from tensorflow.keras.models import Sequential
from xgboost import XGBClassifier


@dataclass(frozen=True)
class LstmTrend:
    direction: str
    move_pct: float


MODEL_FEATURES = [
    "RSI",
    "MACD",
    "MACD_Signal",
    "MACD_Hist",
    "SMA_20",
    "SMA_50",
    "EMA_20",
    "EMA_50",
    "Momentum_5",
    "Momentum_10",
    "BB_Width",
    "HighLowRange",
    "CloseOpenDiff",
    "Return_1",
    "Return_3",
    "Return_5",
    "Volatility_20",
    "Volume_Change",
]


def train_trend_model(df: pd.DataFrame):
    model_data = df[MODEL_FEATURES + ["Target"]].replace([np.inf, -np.inf], np.nan).dropna()
    if len(model_data) < 150:
        raise ValueError("Need at least 150 rows. Use 5 years data.")

    X = model_data[MODEL_FEATURES]
    y = model_data["Target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = XGBClassifier(
        n_estimators=500,
        max_depth=5,
        learning_rate=0.03,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=5,
        gamma=0.2,
        reg_alpha=0.1,
        reg_lambda=1,
        eval_metric="logloss",
        random_state=42,
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    latest_features = X.iloc[-1]
    trend_probability = float(model.predict_proba(latest_features.to_frame().T)[0][1])
    return model, accuracy, latest_features, trend_probability


def train_lstm_model(df: pd.DataFrame, trend_threshold_pct: float):
    close_prices = df["Close"].values.reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(close_prices)
    sequence_length = 60
    if len(scaled_data) <= sequence_length + 20:
        raise ValueError("Need at least 81 rows for LSTM training. Use more history, such as 1 year or 5 years.")

    X = []
    y = []
    for i in range(sequence_length, len(scaled_data)):
        X.append(scaled_data[i - sequence_length : i, 0])
        y.append(scaled_data[i, 0])

    X = np.array(X).reshape(-1, sequence_length, 1)
    y = np.array(y)
    split = int(len(X) * 0.8)
    X_train = X[:split]
    y_train = y[:split]

    model = Sequential()
    model.add(Input(shape=(X_train.shape[1], 1)))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)

    latest_sequence = scaled_data[-60:].reshape(1, 60, 1)
    future_price = scaler.inverse_transform(model.predict(latest_sequence, verbose=0))[0][0]
    latest_price = float(df["Close"].iloc[-1])
    move_pct = ((future_price - latest_price) / latest_price) * 100
    if move_pct > trend_threshold_pct:
        direction = "UP"
    elif move_pct < -trend_threshold_pct:
        direction = "DOWN"
    else:
        direction = "FLAT"

    return model, LstmTrend(direction, round(float(move_pct), 2))
