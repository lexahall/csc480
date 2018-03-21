# Name:         Lexa Hall
# Course:       CSC 480
# Instructor:   Daniel Kauffman
# Assignment:   Class Word
# Term:         Winter 2018

import nltk.corpus as corpus
import nltk.stem as stem
import math


class Lemmatizer(object):

    def __init__(self):
        self.wnl = stem.WordNetLemmatizer()
        self.pos_dict = {"JJ": corpus.wordnet.ADJ, "RB": corpus.wordnet.ADV,
                         "NN": corpus.wordnet.NOUN, "VB": corpus.wordnet.VERB}

    def lemmatize(self, token, tag):
        wn_tag = self.pos_dict.get(tag[:2], corpus.wordnet.NOUN)
        return self.wnl.lemmatize(token, pos = wn_tag)


def categorize_corpus():
    data_set = {}
    for cat in corpus.brown.categories():
        for doc_id in corpus.brown.fileids(cat):
            data_set[(cat, doc_id)] = corpus.brown.tagged_sents(doc_id)
    return data_set


class NaiveBayesClassifier(object):

    def __init__(self):
        self.doc_term_matrix = {}
        self.total_docs = 0
        self.lem = Lemmatizer()
        self.data_set = categorize_corpus()

        self.pre_process()


    def pre_process(self):
        doc_id = -1
        for doc_tuple in self.data_set:
            category = doc_tuple[0]
            if category in self.doc_term_matrix:
                self.doc_term_matrix[category].append({})
                doc_id = len(self.doc_term_matrix[category]) - 1
            else:
                self.doc_term_matrix[category] = [{}]
                doc_id = 0

            self.total_docs += 1
            document = self.data_set[doc_tuple]
            num_words = 0

            for sentence in document:
                num_words += len(sentence)

            self.extract_terms(document, category, num_words, doc_id)

        self.calc_tf_idf()


    def extract_terms(self, document, category, num_words, doc_id):
        for sentence in document:
            bigrams = self.find_ngrams(sentence, 2)
            #trigrams = self.find_ngrams(sentence, 3)

            # lemmatize bigrams
            lem_bigrams = self.lemmatize_ngrams(bigrams, 2)

            for bigram in lem_bigrams:
                self.add_to_matrix(doc_id, bigram, category, num_words)

            # lemmatize trigrams
            #lem_trigrams = self.lemmatize_ngrams(trigrams, 3)

            #for trigram in lem_trigrams:
                #self.add_to_matrix(doc_id, trigram, num_words)

            # Add all individual words to the term matrix
            for word in sentence:
                lem_word = self.lem.lemmatize(word[0], word[1])
                self.add_to_matrix(doc_id, lem_word, category, num_words)


    def lemmatize_ngrams(self, ngrams, n):
        lem_ngrams = []

        for ngram in ngrams:
            if len(ngram) == n:
                lem_ngrams.append(self.flatten_ngram(ngram))

        return lem_ngrams


    def flatten_ngram(self, ngram):
        term = ''

        for word in ngram:
            term += self.lem.lemmatize(word[0], word[1]) + '_'

        return term


    def add_to_matrix(self, doc_id, term, category, num_words):
        if term in self.doc_term_matrix[category][doc_id]:
            self.doc_term_matrix[category][doc_id][term] += (1 / num_words)
        else:
            self.doc_term_matrix[category][doc_id][term] = (1 / num_words)


    def find_ngrams(self, input_list, n):
          return [input_list[i:i + n] for i in range(len(input_list))]


    def calc_tf_idf(self):
        for category in self.doc_term_matrix:
            category_docs = self.doc_term_matrix[category]
            for doc in category_docs:
                doc_terms = doc.keys()
                for term in doc_terms:
                    doc_freq = 0
                    for doc_dict in self.doc_term_matrix[category]:
                        if term in doc_dict:
                            doc_freq += 1
                    idf = ((self.total_docs + 1) / (doc_freq + 1))
                    doc[term] = abs(math.log(doc[term] * idf))


    def classify(self, tagged_words):
        max_probability = 0

        lem_terms = self.add_ngrams(tagged_words)

        for category in self.doc_term_matrix:
            category_docs = self.doc_term_matrix[category]
            relevant_weight = 0
            total_weight = 0
            for doc in category_docs:
                total_weight += sum(doc.values())
                for lem_word in lem_terms:
                    if lem_word in doc:
                        relevant_weight += doc[lem_word]

            probability = relevant_weight / total_weight

            if probability >= max_probability:
                max_probability = probability
                max_category = category

        return max_category


    def add_ngrams(self, tagged_words):
        lem_terms = []

        for word in tagged_words:
            lem_terms.append(self.lem.lemmatize(word[0], word[1]))

        bigrams = self.find_ngrams(tagged_words, 2)

        for bigram in bigrams:
            lem_terms.append(self.flatten_ngram(bigram))

        return lem_terms


def main():
    classifier = NaiveBayesClassifier()
    #print(classifier.doc_term_matrix)
    category = classifier.classify([
        ["ball", "NN"],
        ["basket", "NN"],
        ["ball", "NN"],
        ["run", "VB"],
        ["soccer", "NN"],
        ["kick", "VB"],
        ["player", "NN"],
        ["jersey", "NN"]
    ])
    print(category)


if __name__ == "__main__":
    main()
