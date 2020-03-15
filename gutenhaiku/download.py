import os
import time
from gutenhaiku import models, utils
import requests
from spacy import cli as spacy_cli

LINKS = dict(
    params="https://github.com/sloev/gutenhaiku/releases/download/models.v.1.0.0/deeppunct_params_en",
    checkpoint="https://github.com/sloev/gutenhaiku/releases/download/models.v.1.0.0/deeppunct_checkpoint_google_news",
)


def download_models(click_progress_bar=None):
    with utils.supress_output():
        spacy_cli.download(
            "en_core_web_sm", False, "--quiet", "--disable-pip-version-check"
        )

    for what, url in LINKS.items():
        response = requests.get(url, stream=True)
        total = int(response.headers.get("content-length"))
        filename = models.MODEL_PATHS[what]

        with click_progress_bar(
            length=total, label=f"Downloading {what} file from Github"
        ) as bar, open(filename, "wb") as f:
            time.sleep(0.2)
            downloaded = 0
            for data in response.iter_content(
                chunk_size=max(int(total / 1000), 1024 * 1024)
            ):
                downloaded += len(data)
                f.write(data)
                bar.update(downloaded)
