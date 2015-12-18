# Substantiv

Substantiv is a utility that creates and plays utterances of German nouns learned on Duolingo. The names come from the German word for noun.

## Overview

One of the hardest facets of German for English speakers to learn is the genders of nouns; unlike other gendered languages, such as the Romance languages, one cannot determine the gender of a noun from its orthography. Instead, the genders of nouns, for the most part, have to be memorized.

Substantiv takes the German nouns that a Duolingo user has learned, generates phrases of the form `[definite article] [noun]`, and continually plays these phrases. Since the gender of a noun can (usually) be inferred from its definite article, these phrases can help a listener learn and remember the genders of the nouns that they have learned. This tool is also a valuable resource for improving listening and pronunciation skills.

## Dependencies

To install and run Substantiv, make sure that you have `pip` and `sox` (with an mp3 handler) installed on your machine.

## Installation

To install Substantiv, run 

    $ python setup.py

from the base directory. This need to be done only once.

## Usage

To run Substantiv, invoke the following command

    $ python substantiv.py [number of utterances]

The `[number of utterances]` argument is optional, and defaults to 1000.
