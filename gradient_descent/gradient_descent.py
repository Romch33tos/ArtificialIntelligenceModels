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

def gradient_descent(start_point, armijo_coef=1e-4, grad_tol=1e-6,
                     step_tol=1e-6, max_iterations=10000,
                     initial_step=0.1, max_halvings=60):
  point = np.array(start_point, dtype=float)
  iteration = 0
  prev_value = objective(point)
  prev_step_small = False
  history = [point.copy()]

  while True:
    grad = gradient(point)

    if np.linalg.norm(grad) < grad_tol:
      return point, iteration, objective(point), history, "grad_norm"

    if iteration >= max_iterations:
      return point, iteration, objective(point), history, "max_iter"

    step = initial_step

    while True:
      new_point = point - step * grad
      new_value = objective(new_point)
      if new_value - prev_value < -armijo_coef * np.dot(grad, grad):
        break
      step *= 0.5
      if (initial_step / (2 ** max_halvings)) > step:
        break

    small_step = np.linalg.norm(new_point - point) < step_tol
    small_change = abs(new_value - prev_value) < step_tol

    if small_step and small_change and prev_step_small:
      point = new_point
      history.append(point.copy())
      return point, iteration, objective(point), history, "eps2_double"

    prev_step_small = small_step and small_change

    point = new_point
    prev_value = new_value
    iteration += 1
    history.append(point.copy())

def steepest_descent(start_point, grad_tol=1e-6, step_tol=1e-6,
                     max_iterations=10000):
  point = np.array(start_point, dtype=float)
  iteration = 0
  prev_step_small = False
  history = [point.copy()]

  while True:
    grad = gradient(point)

    if np.linalg.norm(grad) < grad_tol:
      return point, iteration, objective(point), history, "grad_norm"

    if iteration >= max_iterations:
      return point, iteration, objective(point), history, "max_iter"

    direction = -grad

    def line_function(step):
      return objective(point + step * direction)

    result = minimize_scalar(line_function, method="bounded",
                             bounds=(0.0, 10.0))
    optimal_step = result.x

    new_point = point + optimal_step * direction
    new_value = objective(new_point)
    prev_value = objective(point)

    small_step = np.linalg.norm(new_point - point) < step_tol
    small_change = abs(new_value - prev_value) < step_tol

    if small_step and small_change and prev_step_small:
      point = new_point
      history.append(point.copy())
      return point, iteration, objective(point), history, "eps2_double"

    prev_step_small = small_step and small_change

    point = new_point
    iteration += 1
    history.append(point.copy())
