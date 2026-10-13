import random
import time


def target_function(point):
  x = point[0]
  y = point[1]
  return 4 * (x - 5) ** 2 + (y - 6) ** 2


def random_search():
  current_point = [0.0, 0.0]
  expansion_coefficient = 1.5
  shrinkage_coefficient = 0.5
  max_consecutive_failures = 15
  step_size = 0.5
  min_step_size = 1e-6
  max_iterations = 5000

  successful_iterations = 0
  consecutive_failures = 1
  current_value = target_function(current_point)

  start_time = time.time()

  while successful_iterations < max_iterations:

    random_offset = [random.uniform(-1, 1), random.uniform(-1, 1)]

    trial_point = [
      current_point[0] + step_size * random_offset[0],
      current_point[1] + step_size * random_offset[1]
    ]
    trial_value = target_function(trial_point)

    if trial_value < current_value:
      expanded_point = [
        current_point[0] + expansion_coefficient * (trial_point[0] - current_point[0]),
        current_point[1] + expansion_coefficient * (trial_point[1] - current_point[1])
      ]
      expanded_value = target_function(expanded_point)

      if expanded_value < current_value:
        current_point = expanded_point
        current_value = expanded_value
      else:
        current_point = trial_point
        current_value = trial_value

      step_size = step_size * expansion_coefficient
      successful_iterations = successful_iterations + 1
      consecutive_failures = 1

    else:
      consecutive_failures = consecutive_failures + 1

      if consecutive_failures >= max_consecutive_failures:
        if step_size <= min_step_size:
          break
        step_size = step_size * shrinkage_coefficient
        consecutive_failures = 1

  elapsed_time = time.time() - start_time

  exact_solution = [5.0, 6.0]
  distance_to_exact = ((current_point[0] - exact_solution[0]) ** 2 +
                       (current_point[1] - exact_solution[1]) ** 2) ** 0.5

  print(f"Найденная точка:   x* = [{current_point[0]:.6f}, {current_point[1]:.6f}]")
  print(f"Значение функции:  f(x*) = {current_value:.6e}")
  print(f"Отклонение:        {distance_to_exact:.6e}")
  print(f"Итераций:          {successful_iterations}")
  print(f"Время (сек):       {elapsed_time:.6f}")


if __name__ == "__main__":
  random_search()
