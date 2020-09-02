<img src="https://github.com/sloev/gutenhaiku/raw/master/assets/header.png" width="400"/>

# Guten Haiku 

[![Build Status](https://travis-ci.org/sloev/gutenhaiku.svg?branch=master)](https://travis-ci.org/sloev/gutenhaiku) [![Latest Version](https://img.shields.io/pypi/v/gutenhaiku.svg)](https://pypi.python.org/pypi/gutenhaiku) [![Python Support](https://img.shields.io/pypi/pyversions/gutenhaiku.svg)](https://pypi.python.org/pypi/gutenhaiku)

<a href="https://www.buymeacoffee.com/sloev" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-pink.png" alt="Buy Me A Coffee" height="51px" width="217px"></a>

A Commandline tool to mine haiku poems from text

* 80's cli interface with **colors**
* Works great with gutenberg books thx to a builtin cleaner script from [Peyman Mohseni Kiasari](https://github.com/kiasar/gutenberg_cleaner)
* Reconstructs punctuation of haikus using [deepcorrect](https://github.com/bedapudi6788/deepcorrect)
* Appends json haiku's to a file

## Install

```bash
$ pip install gutenhaiku
```

Then you need to download the models in cache:

```bash
$ gutenhaiku setup
```

## Usage

```bash
$ gutenhaiku -f frankenstein.txt -a 'mary shelley' -t 'frankenstein' -d '1818-01-01'
```

<a target="_blank" href="https://asciinema.org/a/9dSu3L5D7OzaOg1p5lOXNF8TC"><img src="https://github.com/sloev/gutenhaiku/raw/master/assets/gutenhaiku.gif" width="600"/></a>

```bash
Wat?             Guten Haiku lets you extract haiku poems from text
Usage:           gutenhaiku \
                 -f frankenstein.txt \
                 -a 'Mary Wollstonecraft Shelley' \
                 -t 'frankenstein' \
                 -d '1818-01-01'
Optional params: --commandfile [-cf] a file with comma seperated 
                                     values for f,a,t,d params
                 --outputfile   [-o] the output file path [default haiku.json
                 --eighties     [-e] eighties mode [default 1]

Advanced usage:  gutenhaiku \
                 -f frankenstein.txt \
                 -a 'Mary Wollstonecraft Shelley' \
                 -t 'frankenstein' \
                 -d '1818-01-01' \
                 -f dracula.txt \
                 -a 'Bram Stoker' \
                 -t 'dracula' \
                 -d '1897-05-26'

setup:           gutenhaiku setup
                 downloads AI models

```

### Output format

*example from [assets](assets/frankenstein_haiku.json)*
```json
{
    "page": 261,
    "word_number": 65407,
    "haiku": [
        "He pointed towards.",
        "The corpse of my wife I rushed.",
        "Towards the window."
    ],
    "author": "mary shelley",
    "title": "frankenstein",
    "date": "1818-01-01T00:00:00"
}
```

## Dev

Run tests with 

```bash
$ poetry run nox
```
