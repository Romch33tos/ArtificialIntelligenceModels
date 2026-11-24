import time
import numpy as np
from scipy.optimize import approx_fprime


def objective_function(point):
  # целевая функция двух переменных
  return 4.0 * (point[0] - 5.0) ** 2 + (point[1] - 6.0) ** 2


def compute_gradient(func, point, step=1e-8):
  # численный градиент через готовую функцию из scipy
  return approx_fprime(point, func, step)


def compute_hessian(func, point, step=1e-5):
  # считаем матрицу вторых производных центральными разностями
  dimension = len(point)
  hessian = np.zeros((dimension, dimension))
  for i in range(dimension):
    point_forward = point.copy()
    point_backward = point.copy()
    point_forward[i] += step
    point_backward[i] -= step

    # берем градиенты в сдвинутых точках и делим разность на двойной шаг
    grad_forward = compute_gradient(func, point_forward)
    grad_backward = compute_gradient(func, point_backward)
    hessian[:, i] = (grad_forward - grad_backward) / (2.0 * step)
  return hessian

def is_positive_definite(matrix):
  # сначала проверяем симметричность матрицы
  if not np.allclose(matrix, matrix.T):
    return False
  # критерий Сильвестра через разложение Холецкого: если не упало с ошибкой, значит > 0
  try:
    np.linalg.cholesky(matrix)
    return True
  except np.linalg.LinAlgError:
    return False

