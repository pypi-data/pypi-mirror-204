# inspiration documentation https://huggingface.co/docs/transformers/tasks/sequence_classification

from transformers import AutoModelForSequenceClassification, AutoTokenizer
from .train import MODEL_NAME, evaluate_with_model_and_tokenizer, ID_2_LABEL, LABEL_2_ID


class Inference():

    def __init__(self):

        from unwanted_content_detector.models.upload import model_exists_locally, download_model, model_directory
        if not model_exists_locally():
            download_model()

        full_path =model_directory()

        print(f"Loading model {MODEL_NAME}")
        print(f"Loading model from {full_path}")
        self.model = AutoModelForSequenceClassification.from_pretrained(full_path, num_labels=2, id2label=ID_2_LABEL, label2id=LABEL_2_ID, local_files_only=True)
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(full_path, local_files_only=True)

    def infer(self, text):
        return evaluate_with_model_and_tokenizer(self.model, self.tokenizer)(text)



