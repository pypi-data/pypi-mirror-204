import os
import pandas as pd


neutral = [
    'life is just boring',
    'do whatever you want',
    'a neutral sentence',
    'another brick in the wall',
    'a vida seja sempre linda',
    'ive cried'
]

def build_dataset(only_print=False):
    path = (os.path.dirname(os.path.realpath(__file__)))
    df = pd.read_csv(f"{path}/data.csv", names=['text', 'label'], on_bad_lines='skip',  sep='|')

    neutral_df = pd.DataFrame([{'text': text, 'label': 'SAFE_CONTENT'} for text in neutral])

    result = pd.concat([df, neutral_df])


    if only_print:
        print(result)
        return

    return result


if __name__ == "__main__":
    import fire
    fire.Fire()
