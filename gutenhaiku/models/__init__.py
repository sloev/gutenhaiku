import os
MODEL_DIR = os.path.split(os.path.abspath(__file__))[0]

MODEL_PATHS = dict(
    params=f"{MODEL_DIR}/params",
    checkpoint=f"{MODEL_DIR}/checkpoint"
)

MODELS_ARE_DOWNLOADED = all(os.path.isfile(path) for path in MODEL_PATHS.values())
