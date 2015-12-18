# Substantiv

Substantiv is a utility that creates and plays utterances of German nouns learned on Duolingo. Its name comes from the German word for noun.

## Overview

One of the hardest facets of German for English speakers to learn is the genders of nouns; unlike the nouns of other gendered languages, such as the Romance languages, one cannot determine the gender of a German noun from its orthography. Instead, the genders of nouns, for the most part, have to be memorized.

Substantiv takes the German nouns that a Duolingo user has learned, generates phrases of the form `[definite article] [noun]`, and continually plays these phrases. 

Since the gender of a noun can (usually) be inferred from its definite article, these phrases can help a listener remember the genders of nouns. This tool can also serve as a resource for improving listening and pronunciation skills.

## Dependencies

To install and run Substantiv, make sure that you have `pip` and `sox` (with an mp3 handler) installed on your machine.

## Installation

To install Substantiv, first run 

    $ python setup.py

Then, create a `username.txt` file in the base directory which contains your Duolingo username. This can be done by running 

    $ echo "[Duolingo username]" > username.txt

Finally, create a `password.txt` file in the base directory which contains your Duolingo password. This can be done by running

    $ echo "[Duolingo password]" > password.txt

All of the above commands only need to be run once.

## Usage

To run Substantiv, invoke the following command

    $ python substantiv.py [number of utterances]

The optional `[number of utterances]` argument is number of utterances that the system will play. It defaults to 1000.
