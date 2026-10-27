import numpy as np
import time
from scipy.optimize import minimize_scalar


def objective(point):
  return 4.0 * (point[0] - 5.0) ** 2 + (point[1] - 6.0) ** 2


def gradient(point):
  return np.array([
    8.0 * (point[0] - 5.0),
    2.0 * (point[1] - 6.0)
  ])
