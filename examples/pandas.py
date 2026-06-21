import pandas as pd

from timeglance.integrations.pandas import forecast_rows


frame = pd.DataFrame({"value": [1, 2, 3]})

for index, row in forecast_rows(frame):
    print(index, row["value"])
