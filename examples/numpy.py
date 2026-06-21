import numpy as np

from timeglance.integrations.numpy import forecast_array


array = np.arange(10)

for value in forecast_array(array):
    print(value)
