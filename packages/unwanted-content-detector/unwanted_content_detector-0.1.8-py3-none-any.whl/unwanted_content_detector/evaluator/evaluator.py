import random

from unwanted_content_detector.data.data_loader import build_dataset
from unwanted_content_detector.entities import Label


def random_guess(_):
    return random.choice([Label.UNWANTED_CONTENT.value, Label.SAFE_CONTENT.value])


class Evaluator:
    """
    Performs evaluation on the complete set
    """

    def evaluate_distilbert(self):
        from unwanted_content_detector.models.distilbert_finetuned.inference import Inference
        inference = Inference()
        return self.evaluate_function(inference.infer)

    def evaluate_random(self):
        self.evaluate_function(random_guess)

    def evaluate_function(self, fn):
        """ Evaluates the entire dataset in a given model """
        data = build_dataset()

        Y = data.iloc[:, -1:]
        X = data.iloc[:, 0:]

        total = len(Y)
        print(f"Total items: {total}")
        correct = 0
        for i in range(total):
            content = X.iloc[i, 0]
            result = fn(content)
            print_result = result," ground truth ", Y.iloc[i, 0].strip(), "for content: ", content
            if result.strip() == Y.iloc[i, 0].strip():
                correct += 1
                print(i,". Correct: ", print_result)
            else:
                print(i, ". Incorrect: ", print_result)

        print(f"Final Accuracy: {correct/total}")
