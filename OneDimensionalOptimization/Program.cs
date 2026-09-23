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
