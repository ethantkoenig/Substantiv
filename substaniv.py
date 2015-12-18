# -*- coding: utf-8 -*- 

from duolingo import Duolingo
from os.path import isfile
import random
from subprocess import Popen
from sys import argv
from time import sleep
from urllib import URLopener


# Duolingo username
USERNAME = "ethantkoenig"

# I hide my Duolingo password in a local file
PASSWORD_FILE = "password.txt"

# Delay (in seconds) between utterances
INTER_UTTERANCE_DELAY = 1.0

# Default number of utterances played
DEFAULT_NUM_UTTERANCES = 1000


# Returns : Duolingo object
def get_duolingo():
  password_file = open(PASSWORD_FILE, "r")
  password = password_file.read().strip()
  password_file.close()
  return Duolingo(USERNAME, password)


# Returns - dict from id to Duolingo lexeme
#
# lingo : Duolingo
# language_abbr : string
def get_vocab(lingo, language_abbr):
  vocab = lingo.get_vocabulary(language_abbr)
  return dict((lexeme["lexeme_id"], lexeme) for lexeme in
                lingo.get_vocabulary(language_abbr)["vocab_overview"])


# Returns : string - sanitized word with non-ASCII characters replaced with
#                    sentinel ASCII sequences
#
# word : string
def sanitize(word):
  word = word.strip().lower()
  word = word.replace(u"ä", "%C3%A4")
  word = word.replace(u"Ä", "%C3%A4")
  word = word.replace(u"ö", "%C3%B6")
  word = word.replace(u"Ö", "%C3%B6")
  word = word.replace(u"ü", "%C3%BC")
  word = word.replace(u"Ü", "%C3%BC")
  word = word.replace(u"ß", "%C3%9F")
  return word


# Returns : int - number of non-ASCII characters in word
#
# word : string
def count_non_ascii(word):
  return len(x for x in word if ord(x) >= 128)


# Returns : bool - whether noun is singular
# 
# vocab : dict from id to Duolingo lexeme
# noun : Duolingo lexeme - must be a noun
def singular(vocab, noun):
  related_lexemes = [vocab[lexeme_id] for lexeme_id in noun["related_lexemes"]]
  related_nouns = [lexeme for lexeme in related_lexemes 
                          if lexeme["pos"] == "Noun"]
  noun_string = noun["word_string"]
  # heuristically check if any relatives are the singular version of noun
  for relative in related_nouns:
    relative_string = relative["word_string"]
    if len(noun_string) > len(relative_string):
      return False
    if (len(noun_string) == len(relative_string)
        and count_non_ascii(noun_string) > count_non_ascii(relative_string)):
      return False

  return True


# Returns : string list list - outer list is list of utterances. each inner list
#                              is a list of words
#
# lingo : Duolingo
# language_abbr : string
def get_utterances(lingo, language_abbr):
  vocab = get_vocab(lingo, language_abbr)
  nouns = [word for word in vocab.values() if word["pos"] == "Noun"]
  result = []
  for noun in nouns:
    gender = noun["gender"]
    article = "die" if not singular(vocab, noun) else \
              "die" if gender == "Feminine" else \
              "der" if gender == "Masculine" else \
              "das"
    result.append([article, noun["word_string"]])
  return result
    


# Returns: string - filepath of audio file containing word
#
# lingo : string
# word : string
# language_abbr : string
def get_audio(lingo, word, language_abbr):
  word = sanitize(word)
  filepath = "{0}.mp3".format(word)
  if not(isfile(filepath)):
    mp3url = lingo.get_audio_url(word, language_abbr)
    url_opener = URLopener()
    url_opener.retrieve(mp3url, "temp.mp3")
    url_opener.close()

    # remove trailing silence
    Popen("sox temp.mp3 {0} reverse trim 0.500 reverse > /dev/null".format(filepath),
          shell = True).wait()
    Popen("rm temp.mp3", shell = True).wait()

  return filepath


# Plays the given utterance
#
# lingo : Duolingo
# language_abbr : string
# utterances : string list list
def play_utterance(lingo, language_abbr, utterance):
  wav_files = [get_audio(lingo, word, language_abbr) for word in utterance]
  print u"Playing {0}".format(" ".join(utterance))
  Popen("play {0} 2> /dev/null".format(" ".join(wav_files)), shell = True).wait()
 

# Plays n randomly selected utterances 
#
# language_abbr : string
# n : int - number of utterances to play
def main(language_abbr, n):
  lingo = get_duolingo()
  utterances = get_utterances(lingo, language_abbr)
  for _ in xrange(n):
    utterance = random.choice(utterances)  
    play_utterance(lingo, language_abbr, utterance)
    sleep(INTER_UTTERANCE_DELAY)
    

if (__name__ == "__main__"):
  n = int(argv[1]) if len(argv) > 1 else DEFAULT_NUM_UTTERANCES
  main("de", n)
