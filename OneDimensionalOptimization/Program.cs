using System;
using System.Collections.Generic;
using System.Diagnostics;

namespace FunctionMinimization
{
  class Program
  {
    static void Main(string[] args)
    {
      Console.OutputEncoding = System.Text.Encoding.UTF8;

      double initialPoint = 0.0;
      double stepSize = 0.1;
      double targetAccuracy = 1e-6;

      Func<double, double> objectiveFunction = x => 2 * x * x - 12 * x;

      Console.WriteLine("Минимизация функции f(x) = 2*x^2 - 12*x");
      Console.WriteLine($"Аналитический минимум: x = 3.0, f(x) = -18.0");
      Console.WriteLine($"Заданная точность: {targetAccuracy}");
      Console.WriteLine($"Параметры Свенна: x0 = {initialPoint}, шаг = {stepSize}");
      Console.WriteLine();

      try
      {
        var (intervalStart, intervalEnd) = SvennSearch(objectiveFunction, initialPoint, stepSize);
        Console.WriteLine($"Начальный интервал неопределенности: [{intervalStart:F6}, {intervalEnd:F6}]");
        Console.WriteLine();
      }
      catch (Exception exception)
      {
        Console.WriteLine($"Ошибка: {exception.Message}");
      }
    }

    public static (double intervalStart, double intervalEnd) SvennSearch(Func<double, double> function, double initialPoint, double stepSize)
    {
      double leftPoint = initialPoint - stepSize;
      double middlePoint = initialPoint;
      double rightPoint = initialPoint + stepSize;

      double leftValue = function(leftPoint);
      double middleValue = function(middlePoint);
      double rightValue = function(rightPoint);

      if (leftValue >= middleValue && middleValue <= rightValue)
      {
        return (leftPoint, rightPoint);
      }

      if (leftValue <= middleValue && middleValue >= rightValue)
      {
        throw new InvalidOperationException("Функция не является унимодальной на заданном интервале.");
      }

      double searchDirection;
      double intervalStart = 0;
      double intervalEnd = 0;
      double currentPoint;
      double currentValue;

      if (leftValue >= middleValue && middleValue >= rightValue)
      {
        searchDirection = stepSize;
        intervalStart = initialPoint;
        currentPoint = rightPoint;
        currentValue = rightValue;
      }
      else
      {
        searchDirection = -stepSize;
        intervalEnd = initialPoint;
        currentPoint = leftPoint;
        currentValue = leftValue;
      }

      int iterationIndex = 1;
      while (true)
      {
        double nextPoint = currentPoint + Math.Pow(2, iterationIndex) * searchDirection;
        double nextValue = function(nextPoint);

        if (nextValue < currentValue)
        {
          if (searchDirection > 0)
          {
            intervalStart = currentPoint;
          }
          else
          {
            intervalEnd = currentPoint;
          }
          currentPoint = nextPoint;
          currentValue = nextValue;
          iterationIndex++;
        }
        else
        {
          if (searchDirection > 0)
          {
            intervalEnd = nextPoint;
          }
          else
          {
            intervalStart = nextPoint;
          }
          break;
        }
      }

      return (intervalStart, intervalEnd);
    }
  }

  public class OptimizationResult
  {
    public string MethodName { get; set; }
    public double MinimumX { get; set; }
    public double MinimumValue { get; set; }
    public int IterationCount { get; set; }
    public double ElapsedMilliseconds { get; set; }
  }
}
