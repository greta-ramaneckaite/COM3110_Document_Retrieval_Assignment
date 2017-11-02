import math

class Retrieve:
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self,index,termWeighting):
        self.index = index
        self.termWeighting = termWeighting

    def forQuery(self,query):
        total_docs = self.totalDocs()
        total_docs_size = len(total_docs)

        match_list = self.matchDocs(query)

        new_index = self.updateIndex(match_list)

        doc_word_freq, query_word_freq = self.termFreqList(new_index, match_list, query)

        doc_vector, query_vector = self.vectorCount(doc_word_freq, query_word_freq)



        # for q_word, q_freq in query.items():
        #     for i_word, i_freq in self.index.items():
        #         # lists od document ids and frequency counts for each term
        #         doc_id_list = set()
        #         freq_count_list = set()
        #         if i_word == q_word:
        #             doc_vec_sum = 0
        #             for doc_id, term_freq in i_freq.items():
        #                 inverse_freq = self.inverseDocFreq(total_docs_size, term_freq)
        #
        #                 vec_size = self.docVecSize(term_freq, inverse_freq)
        #                 doc_vec_sum += vec_size
        #                 print(vec_size)
        #
        #                 doc_id_list.add(doc_id)
        #                 freq_count_list.add(term_freq)
        #
        #             doc_vec_size = math.sqrt(doc_vec_sum)
        #             print(doc_vec_size)
        #             # match[i_word].append(doc_id_list, freq_count_list)
        # # print(match)

        return range(1, 2)

    # total number of documents in the collection - |D|
    def totalDocs(self):
        total_docs = set()

        for word, terms in self.index.items():
            for doc_id, freq_count in terms.items():
                    total_docs.add(doc_id)
        return total_docs

    # inverse document frequency (dfw) of each term (w)
    def inverseDocFreq(self, total_docs_size, term_freq):
        inverse_freq = math.log(total_docs_size/term_freq)
        return inverse_freq

    # size of each document vector - |d|
    def docVecSize(self, term_freq, inverse_freq):
        doc_vec_size = math.pow((term_freq * inverse_freq), 2)
        return doc_vec_size

    # removing all irrelevant documents to reduce data for information retrieval
    def matchDocs(self, query):
        doc_list = []
        for q_word, b in query.items():
            if q_word in self.index:
                if self.index[q_word] not in doc_list:
                    doc_list.extend(self.index[q_word])
        return set(doc_list)

    #  new index dictionary that only contains documents that match the query
    def updateIndex(self, match_list):
        new_index = {}
        for i_word, term_freq in self.index.items():
            for doc_id in match_list:
                if doc_id in term_freq:
                    new_index[i_word] = self.index[i_word]
        return new_index

    # creating lists of term frequencies for each document and query
    def termFreqList(self, new_index, match_list, query):
        term_freq_list = dict.fromkeys(match_list, {})
        query_freq_list = {}

        # iterate through conditional index list
        for i_word, doc_freq in new_index.items():
                # iterate through all conditional doc ids
                for doc_id in term_freq_list.keys():
                    if doc_id in doc_freq:
                        term_freq_list[doc_id][i_word] = doc_freq[doc_id]
                    else:
                        term_freq_list[doc_id][i_word] =  0

                if i_word in query.keys():
                    query_freq_list[i_word] = query[i_word]
                else:
                    query_freq_list[i_word] = 0

        return term_freq_list, query_freq_list

    # count vector sizes of each document and query
    def vectorCount(self, doc_word_freq, query_word_freq):
        doc_vector = {}

        d_sum = 0
        for doc_id, word_freq in doc_word_freq.items():
            for word, freq in word_freq.items():
                d_sum += math.pow(freq, 2)
            doc_vector[doc_id] = math.sqrt(d_sum)


        # print(query_word_freq)
        q_sum = 0
        for word, freq in query_word_freq.items():
            q_sum += math.pow(freq, 2)
        query_vector = math.sqrt(q_sum)

        return doc_vector, query_vector
