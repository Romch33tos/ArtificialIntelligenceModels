import random
import time


# Целевая функция: f(x, y) = 4*(x - 5)^2 + (y - 6)^2
# Минимум достигается в точке (5, 6), где f = 0
def target_function(point):
  x = point[0]
  y = point[1]
  return 4 * (x - 5) ** 2 + (y - 6) ** 2


def random_search():
  # --- Начальные параметры алгоритма ---
  current_point = [0.0, 0.0]     # начальная точка x0
  expand_coef = 1.5              # коэффициент расширения α
  shrink_coef = 0.5              # коэффициент сжатия β
  max_fails = 15                 # M — макс. число неудач подряд
  step_size = 0.5                # t0 — начальный шаг
  min_step = 1e-6                # R — минимальный шаг
  max_iterations = 5000          # N — максимум итераций
  iteration = 0                  # k — счётчик успешных итераций
  fail_count = 1                 # j — счётчик неудач подряд
  current_value = target_function(current_point)

  start_time = time.time()       # запуск таймера

  while iteration < max_iterations:

    random_offset = [random.uniform(-1, 1), random.uniform(-1, 1)]

    trial_point = [
      current_point[0] + step_size * random_offset[0],
      current_point[1] + step_size * random_offset[1]
    ]
    trial_value = target_function(trial_point)

    if trial_value < current_value:
      expanded_point = [
        current_point[0] + expand_coef * (trial_point[0] - current_point[0]),
        current_point[1] + expand_coef * (trial_point[1] - current_point[1])
      ]
      expanded_value = target_function(expanded_point)

      if expanded_value < current_value:
        current_point = expanded_point
        current_value = expanded_value
      else:
        current_point = trial_point
        current_value = trial_value

      step_size = step_size * expand_coef   
      iteration = iteration + 1
      fail_count = 1                    

    else:
      fail_count = fail_count + 1

      if fail_count >= max_fails:
        if step_size <= min_step:
          break                     
        step_size = step_size * shrink_coef
        fail_count = 1

  elapsed_time = time.time() - start_time

  exact = [5.0, 6.0]
  distance = ((current_point[0] - exact[0]) ** 2 +
              (current_point[1] - exact[1]) ** 2) ** 0.5

  print(f"Найденная точка:   x* = [{current_point[0]:.6f}, {current_point[1]:.6f}]")
  print(f"Значение функции:  f(x*) = {current_value:.6e}")
  print(f"Отклонение:        {distance:.6e}")
  print(f"Итераций:          {iteration}")
  print(f"Время (сек):       {elapsed_time:.6f}")

if __name__ == "__main__":
  random_search()
