# Unwanted Content Detector

A library to detect undesired, unbranded, or harmful content

## Usage

In python:


```sh
pip install unwanted-content-detector
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

In the terminal:

```sh
unwanted_detector 
```


To get the manual

## Models

| Model name            | size (mb) 
|-----------------------|-----------
| distilbert-finetuned | 3 gb

## Training 

```py
unwanted_detector train
```

## Target Architecture / Features 

- multiple Swappable models
- multiple evaluation datasets
- possibility of configuring a custom personal dataset to fine tune
- Single performance evaluation criteria

## Use cases it could be applied to

- detecting the generation of harmful content from LLMs
- preventing harmful prompts to be injected into LLMs
- using it as a validator of content being generated according to the brand guidelines


## Liability

This tool aims to help you to detect harmful content but it is not meant to be used as the final decision maker alone. 
