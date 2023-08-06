from unwanted_content_detector.entities import Label


class Detector:

    def __init__(self) -> None:
        from unwanted_content_detector.models.distilbert_finetuned.inference import Inference

        self.inference = Inference()


    def is_unwanted(self, content: str) -> bool:
        inference_result = self.inference.infer(content)
        print("Inference result: ", inference_result)

        bool_result = inference_result == Label.UNWANTED_CONTENT.value

        return bool_result
