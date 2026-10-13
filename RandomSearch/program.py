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

  # --- Рабочие переменные ---
  iteration = 0                  # k — счётчик успешных итераций
  fail_count = 1                 # j — счётчик неудач подряд
  current_value = target_function(current_point)

  start_time = time.time()       # запуск таймера

  # --- Основной цикл поиска ---
  while iteration < max_iterations:

    # Случайное смещение по каждой координате в диапазоне [-1, 1]
    random_offset = [random.uniform(-1, 1), random.uniform(-1, 1)]

    # Пробная точка
    trial_point = [
      current_point[0] + step_size * random_offset[0],
      current_point[1] + step_size * random_offset[1]
    ]
    trial_value = target_function(trial_point)


if __name__ == "__main__":
  pass
