import sys
import os
import contextlib
import warnings

@contextlib.contextmanager
def supress_output():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        import tensorflow as tf
        from tensorflow import keras
        from tensorflow.keras.preprocessing.text import Tokenizer

        err = None
        stderr = sys.stderr
        stdout = sys.stdout
        try:

            sys.stderr = open(os.devnull, "w")
            sys.stdout = open(os.devnull, "w")
            yield
        except Exception as e:
            err = e
        finally:
            sys.stdout = stdout
            sys.stderr = stderr

        if err:
            raise err
