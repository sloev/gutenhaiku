![guten haiku](header.png)

# Guten Haiku

[![Build Status](https://travis-ci.org/sloev/gutenhaiku.svg?branch=master)](https://travis-ci.org/sloev/gutenhaiku) [![Latest Version](https://img.shields.io/pypi/v/gutenhaiku.svg)](https://pypi.python.org/pypi/gutenhaiku) [![Python Support](https://img.shields.io/pypi/pyversions/gutenhaiku.svg)](https://pypi.python.org/pypi/gutenhaiku)

A Commandline tool to mine haiku poems from text

* 80's cli interface with **colors**
* Works great with gutenberg books thx to a builtin cleaner script from [Peyman Mohseni Kiasari](https://github.com/kiasar/gutenberg_cleaner)
* Appends json haiku's to a file

## Install

```bash
$ pip install gutenhaiku
```

## Usage

[![asciicast](https://asciinema.org/a/9dSu3L5D7OzaOg1p5lOXNF8TC.svg)](https://asciinema.org/a/9dSu3L5D7OzaOg1p5lOXNF8TC)

```bash
Wat?             Guten Haiko lets you extract haiku poems from text
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
```