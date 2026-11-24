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

def newton_method(func, initial_point, eps1=1e-6, eps2=1e-6, max_iterations=100):
  current_point = np.array(initial_point, dtype=float)
  iteration = 0
  # флаг для запоминания, выполнилось ли условие остановки на прошлой итерации
  prev_condition_met = False

  while True:
    gradient = compute_gradient(func, current_point)

    # первый критерий выхода: норма градиента достаточно мала
    if np.linalg.norm(gradient) <= eps1:
      return current_point, func(current_point), iteration

    # защита от бесконечного цикла по числу шагов
    if iteration >= max_iterations:
      return current_point, func(current_point), iteration

    # строим матрицу Гессе и сразу ищем обратную к ней
    hessian = compute_hessian(func, current_point)
    inverse_hessian = np.linalg.inv(hessian)

    if is_positive_definite(inverse_hessian):
      # классический шаг Ньютона, если матрица положительно определена
      direction = -np.dot(inverse_hessian, gradient)
      step_size = 1.0
    else:
      # если матрица не подходит, идем по антиградиенту и дробим шаг пополам
      direction = -gradient
      step_size = 1.0
      while func(current_point + step_size * direction) >= func(current_point):
        step_size *= 0.5

    # переходим в новую точку
    next_point = current_point + step_size * direction

    # проверяем сходимость по изменению координат и самой функции
    step_diff = np.linalg.norm(next_point - current_point)
    func_diff = abs(func(next_point) - func(current_point))
    current_condition_met = (step_diff < eps2) and (func_diff < eps2)

    # выходим, только если оба условия сработали дважды подряд (на k и k-1)
    if current_condition_met and prev_condition_met:
      return next_point, func(next_point), iteration + 1

    # обновляем переменные перед следующей итерацией
    prev_condition_met = current_condition_met
    current_point = next_point
    iteration += 1

# здесь можно поменять начальную точку, точности и лимит итераций
start_point = [0.0, 0.0]
precision_eps1 = 1e-6
precision_eps2 = 1e-6
max_iter = 100

# замеряем время работы алгоритма
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


