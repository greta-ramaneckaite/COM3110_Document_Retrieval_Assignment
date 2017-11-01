
class Retrieve:
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self,index,termWeighting):
        self.index = index
        self.termWeighting = termWeighting
        self.initList = []
        self.docWordList = []
        self.invertedList = []


    def forQuery(self,query):
        total_docs = self.totalDocs()


        for q_word, q_freq in query.items():
            for i_word, i_freq in self.index.items():
                doc_id_list = set()
                freq_count_list = set()

                for doc_id, term_freq in i_freq.items():
                        doc_id_list.add(doc_id)
                        freq_count_list.add(term_freq)


        return range(1, 2)

    # total number of documents in the collection - |D|
    def totalDocs(self):
        total_docs = set()

        for word, terms in self.index.items():
            for doc_id, freq_count in terms.items():
                    total_docs.add(doc_id)
        return total_docs

