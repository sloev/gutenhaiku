import os
import logging
import json
import silence_tensorflow.auto

import warnings
import sys
import spacy
from spacy_syllables import SpacySyllables
from collections import defaultdict, Counter
from gutenhaiku.cleaner import strip_headers
from gutenhaiku import models

with warnings.catch_warnings():  
    warnings.filterwarnings("ignore",category=FutureWarning)
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.preprocessing.text import Tokenizer
    stderr = sys.stderr
    stdout = sys.stdout
    err = None
    try:

        sys.stderr = open(os.devnull, "w")
        sys.stdout = open(os.devnull, "w")
        
        from deepcorrect import DeepCorrect
        corrector = DeepCorrect(models.MODEL_PATHS["params"], models.MODEL_PATHS["checkpoint"])
    except Exception as e:
        err = e
    finally:
        sys.stdout = stdout
        sys.stderr = stderr

    if err:
        raise err


nlp = spacy.load("en_core_web_sm")

syllables = SpacySyllables(nlp)

nlp.add_pipe(syllables, after="tagger")

IGNORE_POS = set(["SPACE", "PUNCT"])
REPLACE_CHARACTERS = str.maketrans({key: None for key in "!\"';?_-0123456789"})


def process_generator(text, progress_bar):
    CURRENT_HAIKU = defaultdict(list)
    ALLOWED_SUMS = [5, 7, 5]
    CURRENT_LINE = 0

    text = strip_headers(text, progress_bar=progress_bar)

    def generate_tokens():
        for doc in nlp.pipe(text.splitlines(), disable=["ner"]):
            for token in doc:
                yield token

    word_number = 0
    with progress_bar(generate_tokens()) as gen:
        for index, token in enumerate(gen):

            if token.pos_ in IGNORE_POS:
                continue

            word_number += 1

            CURRENT_HAIKU[CURRENT_LINE].append(token)
            syllables_sum = sum(
                [
                    c
                    for c in (t._.syllables_count for t in CURRENT_HAIKU[CURRENT_LINE])
                    if c is not None
                ]
            )

            if syllables_sum > ALLOWED_SUMS[CURRENT_LINE]:
                CURRENT_HAIKU[CURRENT_LINE].pop(0)
            elif syllables_sum == ALLOWED_SUMS[CURRENT_LINE]:
                CURRENT_LINE += 1
            if CURRENT_LINE > 2:
                has_same_word_in_same_line = any(
                    any(c > 1 for c in Counter([w.text for w in l]).values())
                    for l in CURRENT_HAIKU.values()
                )
                if has_same_word_in_same_line:
                    logging.debug("has_same_word_in_same_line")
                else:
                    word_counts = Counter(
                        [w.text for l in CURRENT_HAIKU.values() for w in l]
                    )
                    has_repetition = any(
                        count > 1 and len(word) > 5
                        for word, count in word_counts.items()
                    )

                    if has_repetition:
                        haiku_lines = [
                            " ".join(t.text for t in l) for l in CURRENT_HAIKU.values()
                        ]

                        final_haiku = []
                        for haiku_line in haiku_lines:
                            try:
                                corrected_line = corrector.correct(haiku_line)[0][
                                    "sequence"
                                ]
                                final_haiku.append(corrected_line)
                                continue
                            except KeyError:
                                pass

                            final_haiku.append(haiku_line)

                        haiku = "\n".join(final_haiku)

                        try:
                            len_without_ignored_chars = len(
                                haiku.translate(REPLACE_CHARACTERS)
                            )
                            assert len_without_ignored_chars == len(haiku)
                            page = int(word_number / 250.0)
                            data = {
                                "page": page,
                                "word_number": word_number,
                                "haiku": final_haiku,
                            }
                            yield data
                        except AssertionError:
                            logging.debug(f"haiku has bad chars: {haiku}")

                CURRENT_HAIKU.clear()
                CURRENT_LINE = 0


if __name__ == "__main__":
    import sys

    for filename in sys.argv[1:]:
        process(filename)
