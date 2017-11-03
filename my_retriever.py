import math

class Retrieve:
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self,index,termWeighting):
        self.index = index
        self.termWeighting = termWeighting
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

    # create list of candidate docs for given query
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

        #  create vector length for each document
        self.create_vector_dict()

    # {doc_id: vector, doc_id: vector... }
    def create_vector_dict(self):
        for doc, words in self.all_docs.items():
            vector_total = 0
            for freq in words.values():
                vector_total += math.pow(freq, 2)

            self.vector_dict[doc] = math.sqrt(vector_total)

    # {doc_id: {word: tfidf}, doc_id: {word: tfidf}, ... }
    def create_tfidf_dict(self):

        for doc, words in self.all_docs.items():
            self.tfidf_dict[doc] = {}
            for d_word, freq in words.items():
                self.tfidf_dict[doc][d_word] = self.tf_idf(d_word, doc)

    def tf_idf(self, word, doc_id):
        term_freq = self.index[word][doc_id]

        # Number of docs a word is in
        word_doc_count = len(self.index[word])

        inverse_doc_count = math.log(self.doc_count/word_doc_count)

        tf_idf = term_freq * inverse_doc_count

        return tf_idf

    def cos_sim_generator(self, query, query_vector, q_tf_idf, candidate_docs):
        similiarity_score_dict = {}  # {doc_id: score, doc_id: score, ... }
        cand_doc_dict = {}
        similarity_list = []

        for doc in candidate_docs:
            cand_doc_dict[doc] = self.all_docs[doc]

        for doc_id, words in cand_doc_dict.items():

            if self.termWeighting == 'tfidf':
                same_words = query.keys() & cand_doc_dict[doc_id].keys()

                word_freq_sum = 0
                for word in same_words:
                    word_freq_sum += q_tf_idf[word] * self.tfidf_dict[doc_id][word]

                similiarity_score_dict[doc_id] = word_freq_sum/self.vector_dict[doc_id]

            elif self.termWeighting == 'tf':
                same_words = query.keys() & cand_doc_dict[doc_id].keys()

                word_freq_sum = 0
                for word in same_words:
                    word_freq_sum += query[word] * cand_doc_dict[doc_id][word]

                similiarity_score_dict[doc_id] = word_freq_sum / self.vector_dict[doc_id]
            else:
                same_words = query.keys() & cand_doc_dict[doc_id].keys()
                word_freq_sum = len(same_words)

                similiarity_score_dict[doc_id] = word_freq_sum / self.vector_dict[doc_id]

        for k, v in sorted(similiarity_score_dict.items(), key=lambda kv: kv[1]):
            similarity_list.append(k)

        return similarity_list[:10]

