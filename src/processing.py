def iteration_function(data, config, key1, key2):
    first_layer = config[key1][key2]
    return data[first_layer]

def iteration_function2(data, config, key1, key2):
    second_layer  = config[key1][key2]
    return data[second_layer]

    
    