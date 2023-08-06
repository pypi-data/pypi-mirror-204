
import pandas as pd
def load_data():
    import os;
    path = (os.path.dirname(os.path.realpath(__file__)))
    return pd.read_csv(f"{path}/data.csv", on_bad_lines='skip', sep='|')
