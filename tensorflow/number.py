import tensorflow as tf
from tensorflow import keras
from keras.layers import (Dense, BatchNormalization, Dropout)
from keras.datasets.mnist import load_data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


(x_train, y_train), (x_test, y_test) = load_data()

print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)
