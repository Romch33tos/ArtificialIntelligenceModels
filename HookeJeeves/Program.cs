using System;

class HookeJeevesOptimization
{
  static double CalculateObjectiveFunction(double[] coordinates)
  {
    return 4 * Math.Pow(coordinates[0] - 5, 2) + Math.Pow(coordinates[1] - 6, 2);
  }

  static void Main(string[] args)
  {
    int spaceDimension = 2;
    double[] currentBasePoint = { 0.0, 0.0 };
    double precisionEpsilon = 0.01;
    double[] stepSizes = { 1.0, 1.0 };
    double accelerationMultiplier = 1.0;
    double stepReductionAlpha = 2.0;

    int iterationCounter = 0;
    double[] exploratoryPoint = (double[])currentBasePoint.Clone();

    Console.WriteLine("Запуск метода Хука-Дживса...");

    while (true)
    {
      for (int coordinateIndex = 0; coordinateIndex < spaceDimension; coordinateIndex++)
      {
        double currentFunctionValue = CalculateObjectiveFunction(exploratoryPoint);

        exploratoryPoint[coordinateIndex] += stepSizes[coordinateIndex];
        if (CalculateObjectiveFunction(exploratoryPoint) >= currentFunctionValue)
        {
          exploratoryPoint[coordinateIndex] -= 2 * stepSizes[coordinateIndex];
          if (CalculateObjectiveFunction(exploratoryPoint) >= currentFunctionValue)
          {
            exploratoryPoint[coordinateIndex] += stepSizes[coordinateIndex];
          }
        }
      }

      if (CalculateObjectiveFunction(exploratoryPoint) < CalculateObjectiveFunction(currentBasePoint))
      {
        double[] previousBasePoint = (double[])currentBasePoint.Clone();
        currentBasePoint = (double[])exploratoryPoint.Clone();

        for (int coordinateIndex = 0; coordinateIndex < spaceDimension; coordinateIndex++)
        {
          exploratoryPoint[coordinateIndex] = currentBasePoint[coordinateIndex] + 
            accelerationMultiplier * (currentBasePoint[coordinateIndex] - previousBasePoint[coordinateIndex]);
        }

        iterationCounter++;
        Console.WriteLine($"Итерация {iterationCounter}: Точка по образцу = ({currentBasePoint[0]:F4}, {currentBasePoint[1]:F4}), f(x) = {CalculateObjectiveFunction(currentBasePoint):F4}");
      }
      else
      {
        bool tendernessReached = true;
        for (int coordinateIndex = 0; coordinateIndex < spaceDimension; coordinateIndex++)
        {
          if (stepSizes[coordinateIndex] > precisionEpsilon)
          {
            tendernessReached = false;
            break;
          }
        }

        if (tendernessReached)
        {
          Console.WriteLine("\nОптимизация успешно завершена.");
          Console.WriteLine($"Точка минимума x* = ({currentBasePoint[0]:F4}, {currentBasePoint[1]:F4})");
          Console.WriteLine($"Минимум функции f(x*) = {CalculateObjectiveFunction(currentBasePoint):F6}");
          break;
        }
        else
        {
          for (int coordinateIndex = 0; coordinateIndex < spaceDimension; coordinateIndex++)
          {
            if (stepSizes[coordinateIndex] > precisionEpsilon)
            {
              stepSizes[coordinateIndex] /= stepReductionAlpha;
            }
          }
          
          exploratoryPoint = (double[])currentBasePoint.Clone();
          
          iterationCounter++;
          Console.WriteLine($"Итерация {iterationCounter} (Уменьшение шага): Шаги = ({stepSizes[0]:F4}, {stepSizes[1]:F4})");
        }
      }
    }
  }
}
