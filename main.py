from src.data_loader import load_config, data_load
from src.processing import iteration_function, iteration_function2
import pandas as pd
config = load_config()
data = data_load(config)
data_properties = iteration_function(data, config, "json_layer1_keys", "key3" )
print(data_properties.keys())
data_time_series = iteration_function2(data_properties, config,"json_layer2_keys", "key2" )
df_test = pd.DataFrame(data_time_series)
df = pd.json_normalize(data_time_series)
print(df.head())
print(df.columns)

