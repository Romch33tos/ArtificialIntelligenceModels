import random
import time


# Целевая функция: f(x, y) = 4*(x - 5)^2 + (y - 6)^2
# Минимум достигается в точке (5, 6), где f = 0
def target_function(point):
  x = point[0]
  y = point[1]
  return 4 * (x - 5) ** 2 + (y - 6) ** 2


if __name__ == "__main__":
  pass
