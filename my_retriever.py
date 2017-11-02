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
        print(new_index)




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
    def termFreqList(self, new_index):
        list = []
        for i_word, term_freq in new_index.items():
            for x_word, x_freq in self.index.items():
                if i_word == x_word:
                    list.append(x_freq[1])




