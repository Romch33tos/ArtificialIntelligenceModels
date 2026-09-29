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
    }
  }
}
