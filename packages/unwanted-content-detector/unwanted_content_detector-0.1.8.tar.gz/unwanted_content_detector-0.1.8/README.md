# Unwanted Content Detector

A library to detect undesired, unbranded, or harmful content

## Usage

In python:


```sh
pip install unwanted-content-detector --upgrade
```

With Pandas

```py
import pandas as pd
from unwanted_content_detector import Detector

detector = Detector()
df = pd.DataFrame({"text": [
    "this is hate speech",
    "We should all do our part to protect the environment.",
    'Everyone has the right to love who they want.'
]})

df['is_unwanted'] = df['text'].apply(lambda x: detector.is_unwanted(x))
```

To get a view of the complete options type in the terminal:

```sh
unwanted_detector 
```



## Models

| Model name            | size (mb) 
|-----------------------|-----------
| distilbert-finetuned | 300 mb

## Training 

```py
unwanted_detector train
```


## Liability

This tool aims to help you to detect harmful content but it is not meant to be used as the final decision maker alone. 
