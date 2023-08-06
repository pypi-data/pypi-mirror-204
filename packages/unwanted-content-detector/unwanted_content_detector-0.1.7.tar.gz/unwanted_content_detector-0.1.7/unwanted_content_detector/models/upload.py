import os

# URL: https://huggingface.co/JeanMachado/unwanted_content_detector
REPO_ID = 'JeanMachado/unwanted_content_detector'

def create_repo():
    from huggingface_hub import create_repo

    return create_repo(REPO_ID)


def model_directory():
    import pathlib
    current_dir =  str(pathlib.Path(__file__).resolve().parent)

    return current_dir + "/../../detector_distilbert_01"

def upload_model():
    from huggingface_hub import HfApi
    from datetime import datetime;
    print("Uploading model to HuggingFace Hub")

    api = HfApi()
    api.upload_folder(
        folder_path=model_directory(),
        repo_id = REPO_ID,
    )

def model_exists_locally():
    return os.path.exists(model_directory())

def download_model():
    print("Downloading uploaded model")
    from huggingface_hub import snapshot_download
    if model_exists_locally():
        raise Exception("Model already exists")
    snapshot_download(repo_id=REPO_ID, local_dir=model_directory())



if __name__ == "__main__":
    import fire
    fire.Fire()



