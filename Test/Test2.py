import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors, datasets

iris = datasets.load_iris()
iris_X = iris.data
iris_y = iris.target
print("Number of classes: %d" % len(np.unique(iris_y)))
print("Number of data points: %d" % len(iris_y))
print(iris_X)
print(iris_y)

X0 = iris_X[iris_y == 0, :]
print("\nSamples from class 0:\n", X0[:5, :])

X1 = iris_X[iris_y == 1, :]
print("\nSamples from class 1:\n", X1[:5, :])

X2 = iris_X[iris_y == 2, :]
print("\nSamples from class 2:\n", X2[:5, :])
