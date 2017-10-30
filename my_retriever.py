
class Retrieve:
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self,index,termWeighting):
        self.index = index
        self.termWeighting = termWeighting
        self.initList = []
        self.invertedList = []
        self.freqCount()

    # Method to apply query to index
    def forQuery(self,query):
        return range(1,11)

    def freqCount(self):
        for x,y in self.index.items():
            self.initList.append((x, len(y)))
        self.invertedList = sorted(self.initList, key=lambda x: x[1])

        print(self.invertedList)

