import os
from logging import getLogger
from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.keras.layers as layers
import tensorflow.keras.models as models
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.utils as utils
from sklearn.model_selection import train_test_split


class InputShapeError(Exception):
    pass


class ModelBuilder:
    """Really ugly class. . ."""

    def __init__(self, username, logger) -> None:
        self.logger = logger
        self.username = username
        self.model = self.set_model()

    def set_model(self) -> tf.keras.Sequential:
        path = f"saved_models/{self.username}.h5"
        if os.path.exists(os.path.join(Path(__name__).parent.parent, path)):
            self.logger.info(f"Loading model from {path}")
            return tf.keras.models.load_model(path)
        self.df = self.__load_df(self.username)
        self.__prepare_df()
        return self.train_model()

    def __prepare_df(self):
        self.df.insert(1, "elo_gap", self.df["player_elo"] - self.df["opponent_elo"])
        self.df.insert(1, "hour", self.df["date"].dt.hour)
        self.df.drop(
            self.df.columns.difference(
                ["player_color", "elo_gap", "hour", "player_result", "time_class"]
            ),
            1,
            inplace=True,
        )
        self.df = self.df.astype({"hour": "str"})
        self.df = pd.get_dummies(self.df)
        self.normalize("elo_gap")
        self.df["game_num"] = self.df.index
        self.normalize("game_num")

    def normalize(self, column):
        self.df[column] = self.df[column] / self.df[column].abs().max()

    def __load_df(self, username):
        df = pd.read_csv(f"data/{username}.csv")
        df["date"] = pd.to_datetime(df["date"])
        return df

    def create_train_test_data(self, y_col="player_result"):
        X = self.df.drop([y_col], axis=1).to_numpy()
        y = self.df[y_col].to_numpy().astype(int)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        return X_train, X_test, y_train, y_test

    def create_model(self, shape) -> tf.keras.Sequential:
        model = tf.keras.Sequential(
            [
                tf.keras.layers.Input(shape=shape),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(16, activation="relu"),
                tf.keras.layers.Dense(16, activation="relu"),
                tf.keras.layers.Dense(16, activation="relu"),
                tf.keras.layers.Dense(1),
            ]
        )
        model.compile(
            loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"]
        )
        return model

    def train_model(self):
        X_train, X_test, y_train, y_test = self.create_train_test_data()
        model = self.create_model(X_train.shape[1])
        history = model.fit(
            X_train, y_train, epochs=40, verbose=1, validation_data=(X_test, y_test)
        )
        model.save(f"saved_models/{self.username}.h5")
        self.logger.info(f"Model saved to saved_models/{self.username}.h5")
        return model

    def load_model(self):
        model = models.load_model(f"saved_models/{self.username}.h5")
        return model

    def predict(self, X):
        X = np.array(X)
        config = (
            self.model.get_config()
        )  # Returns pretty much every information about your model
        input_len = config["layers"][0]["config"]["batch_input_shape"][-1]
        if len(X) != input_len:
            self.logger.error("Input shape does not match model input shape")
            raise InputShapeError("Input shape does not match model input shape")
        return self.model.predict(X)


m = ModelBuilder("Barabasz60", getLogger())
print(m.model.get_config()["layers"][0]["config"]["batch_input_shape"][-1])
m.predict(
    [
        10,
    ]
)
