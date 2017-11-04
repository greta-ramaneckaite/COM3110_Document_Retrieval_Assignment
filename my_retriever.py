"""
    Information retrievak assignment
    05-11-2017
    Greta Ramaneckaite
"""

import math

class Retrieve:
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self,index,termWeighting):
        self.index = index
        self.termWeighting = termWeighting

        """
        calculating initial values that will be used later on
        """
        self.all_docs = {}  # {doc_id: {word: freq, word: freq, ...}, ... }
        self.vector_dict = {}  # {doc_id: vector, doc_id: vector, ... }
        self.create_global_variables()
        self.tfidf_dict = {} # {doc_id: {word: tfidf}, doc_id: {word: tfidf}, ... }
        self.create_tfidf_dict()

    # Method to apply query to index
    def forQuery(self, query):
        # create an empty query tfidf dictionary
        query_tf_idf = {}
        # a set of documents that have the same words as the query
        cand_docs = self.create_candidate_docs(query)

        vector_total = 0
        for word, freq in query.items():
            vector_total += math.pow(freq, 2)

            if word in self.index.keys():
                term_freq = query[word]
                word_doc_count = len(self.index[word])
                inverse_doc_count = math.log(self.doc_count / word_doc_count)
                query_tf_idf[word] = term_freq * inverse_doc_count

        query_vector = math.sqrt(vector_total)

        similarity_scores = self.cos_sim_generator(query, query_vector, query_tf_idf, cand_docs)

        return similarity_scores

    # create list of candidate docs for given query, contains doc ids
    def create_candidate_docs(self, query):
        cand_docs = set()
        # for every word in the query, check for doc presence in the index dictionary
        for word in query.keys():
            if word in self.index:
                cand_docs.update(set(self.index[word].keys()))

        return cand_docs

    # Add values to global vars for later use
    # {doc_id: {word: freq}, doc_id: {word: freq, word: freq}, ...}
    def create_global_variables(self):
        # creates a dictionary of all documents with words and their frequencies
        for i_word, docs in self.index.items():
            for doc_id, word_freq in docs.items():
                if doc_id in self.all_docs:
                    self.all_docs[doc_id][i_word] = word_freq
                else:
                    self.all_docs[doc_id] = {}
                    self.all_docs[doc_id][i_word] = word_freq

        #  number of all documents
        self.doc_count = len(self.all_docs)

        #  create vector length dictionary for each document
        self.create_vector_dict()

    # {doc_id: vector, doc_id: vector... }
    # create vectors for each document
    # formula calculated ==>   |d| = sqrt(sum(pow(doc_freq)))
    def create_vector_dict(self):
        for doc, words in self.all_docs.items():
            vector_total = 0
            for freq in words.values():
                vector_total += math.pow(freq, 2)

            self.vector_dict[doc] = math.sqrt(vector_total)

    # {doc_id: {word: tfidf}, doc_id: {word: tfidf}, ... }
    # create tfidf dictionary  that contains all vector sizes for each document word
    def create_tfidf_dict(self):
        for doc, words in self.all_docs.items():
            self.tfidf_dict[doc] = {}
            for d_word, freq in words.items():
                #  adds word vector size
                self.tfidf_dict[doc][d_word] = self.tf_idf(d_word, doc)

    #  calculation for the tfidf dictionary (create_tfidf_dict)
    def tf_idf(self, word, doc_id):
        # freq for specific word in a specific dictionary
        word_freq = self.index[word][doc_id]

        # Number of documents that a word is in
        word_doc_count = len(self.index[word])

        #  inverse document frequency
        inverse_doc_freq = math.log(self.doc_count/word_doc_count)

        #  final size of word vector
        tf_idf = word_freq * inverse_doc_freq

        return tf_idf
    """
        - calculate cosine similarity scores according to the term weighting
        - rank them from highest to lowest
        - return top 10 values
    """
    def cos_sim_generator(self, query, query_vector, q_tf_idf, candidate_docs):
        similarity_score = {}  # {doc_id: score, doc_id: score, ... }
        cand_doc_dict = {} # {doc_id: {word: freq, ...}, ...}
        similarity_list = [] # final list of all similarity scores from highest to lowest
        # generate a dictionary of all candidate documents
        for doc in candidate_docs:
            cand_doc_dict[doc] = self.all_docs[doc]

        # loop through all candidate documents
        for doc_id, words in cand_doc_dict.items():
            #  find all common words between the query and candidate documents
            same_words = query.keys() & cand_doc_dict[doc_id].keys()

            # initialising the word frequency sum to be calculated according to the term weighting
            word_freq_sum = 0

            # calculates frequency sums according to the term weighting and calculates the similarity scores
            if self.termWeighting == 'tfidf':
                # calculate tf * idf for each common word
                vector = math.sqrt(sum(math.pow(i, 2) for i in self.tfidf_dict[doc_id].values()))
                for word in same_words:

                    word_freq_sum += q_tf_idf[word] * self.tfidf_dict[doc_id][word]

                similarity_score[doc_id] = word_freq_sum / vector

            elif self.termWeighting == 'tf':
                for word in same_words:
                    word_freq_sum += query[word] * cand_doc_dict[doc_id][word]

                similarity_score[doc_id] = word_freq_sum / self.vector_dict[doc_id]
            else:
                word_freq_sum = len(same_words)

                similarity_score[doc_id] = word_freq_sum / self.vector_dict[doc_id]

        # reorder the scores from highest to lowest
        for k, v in sorted(similarity_score.items(), key=lambda kv: kv[1]):
            similarity_list.append(k)

        # final return of the class (final output)
        return similarity_list[::-1][:10]
