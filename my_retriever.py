
class Retrieve:
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self,index,termWeighting):
        self.index = index
        self.termWeighting = termWeighting

    # Method to apply query to index
    def forQuery(self,query):
        return range(1,11)

