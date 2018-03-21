import nltk.corpus as corpus
import nltk.stem as stem


class Lemmatizer(object):

    def __init__(self):
        self.wnl = stem.WordNetLemmatizer()
        self.pos_dict = {"JJ": corpus.wordnet.ADJ, "RB": corpus.wordnet.ADV,
                         "NN": corpus.wordnet.NOUN, "VB": corpus.wordnet.VERB}

    def lemmatize(self, token, tag):
        wn_tag = self.pos_dict.get(tag[:2], corpus.wordnet.NOUN)
        return self.wnl.lemmatize(token, pos = wn_tag)


def main():
  words = [['the', 'DT'],
           ['cat', 'NN'],
           ['the', 'DT'],
           ['dog', 'NN'],
           ['the', 'DT'],
           ['dogs', 'NN'],
           ['the', 'DT'],
           ['chicken', 'NN']
  ]
  lem = Lemmatizer()

  word_dict = {}
  for word in words:
    lem_word = lem.lemmatize(word[0], word[1])
    if lem_word in word_dict:
      word_dict[lem_word] += 1
    else:
      word_dict[lem_word] = 1

  print(word_dict)

if __name__ == "__main__":
  main()
