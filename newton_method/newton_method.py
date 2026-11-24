import time
import numpy as np
from scipy.optimize import approx_fprime


def objective_function(point):
  return 4.0 * (point[0] - 5.0) ** 2 + (point[1] - 6.0) ** 2


def compute_gradient(func, point, step=1e-8):
  return approx_fprime(point, func, step)


def compute_hessian(func, point, step=1e-5):
  dimension = len(point)
  hessian = np.zeros((dimension, dimension))
  for i in range(dimension):
    point_forward = point.copy()
    point_backward = point.copy()
    point_forward[i] += step
    point_backward[i] -= step
    grad_forward = compute_gradient(func, point_forward)
    grad_backward = compute_gradient(func, point_backward)
    hessian[:, i] = (grad_forward - grad_backward) / (2.0 * step)
  return hessian


def is_positive_definite(matrix):
  if not np.allclose(matrix, matrix.T):
    return False
  try:
    np.linalg.cholesky(matrix)
    return True
  except np.linalg.LinAlgError:
    return False


def newton_method(func, initial_point, eps1=1e-6, eps2=1e-6, max_iterations=100):
  current_point = np.array(initial_point, dtype=float)
  iteration = 0
  prev_condition_met = False

  while True:
    gradient = compute_gradient(func, current_point)
    if np.linalg.norm(gradient) <= eps1:
      return current_point, func(current_point), iteration

    if iteration >= max_iterations:
      return current_point, func(current_point), iteration

    hessian = compute_hessian(func, current_point)
    inverse_hessian = np.linalg.inv(hessian)

    if is_positive_definite(inverse_hessian):
      direction = -np.dot(inverse_hessian, gradient)
      step_size = 1.0
    else:
      direction = -gradient
      step_size = 1.0
      while func(current_point + step_size * direction) >= func(current_point):
        step_size *= 0.5

    next_point = current_point + step_size * direction
    step_diff = np.linalg.norm(next_point - current_point)
    func_diff = abs(func(next_point) - func(current_point))
    current_condition_met = (step_diff < eps2) and (func_diff < eps2)

    if current_condition_met and prev_condition_met:
      return next_point, func(next_point), iteration + 1

    prev_condition_met = current_condition_met
    current_point = next_point
    iteration += 1


start_point = [0.0, 0.0]
precision_eps1 = 1e-6
precision_eps2 = 1e-6
max_iter = 100

start_time = time.perf_counter()
optimal_point, optimal_value, total_iterations = newton_method(
  objective_function,
  start_point,
  eps1=precision_eps1,
  eps2=precision_eps2,
  max_iterations=max_iter
)
elapsed_time = time.perf_counter() - start_time

print("x* =", optimal_point)
print("f(x*) =", optimal_value)
print("Количество итераций:", total_iterations)
print(f"Время выполнения: {elapsed_time:.6f} сек.")
