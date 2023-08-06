import os
import pandas as pd


neutral = [
    'life is just boring',
    'do whatever you want',
    'a neutral sentence',
    'another brick in the wall',
    'a vida seja sempre linda',
    'ive cried',
    'the color black',
    'primavera',
    'vendaval',
    'temporal',
]

negative = [
    'red light district are fine',
    'i hate you',
]

def build_dataset(only_print=False):
    path = (os.path.dirname(os.path.realpath(__file__)))
    file_df = pd.read_csv(f"{path}/data.csv", names=['text', 'label'], on_bad_lines='skip',  sep='|')

    neutral_df = pd.DataFrame([{'text': text, 'label': 'SAFE_CONTENT'} for text in neutral])
    negiative_df = pd.DataFrame([{'text': text, 'label': 'UNSAFE_CONTENT'} for text in negative])

    result = pd.concat([file_df, neutral_df, negiative_df])
    if only_print:
        print(result)
        return

    return result


if __name__ == "__main__":
    import fire
    fire.Fire()
