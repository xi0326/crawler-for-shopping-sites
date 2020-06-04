class Filter():
    __lowBound = None
    __upBound = None

    def __init__(self, lowBound = None, upBound = None):
        self.__lowBound = lowBound
        self.__upBound = upBound

    def getLowBound(self):
        return self.__lowBound

    def getUpBound(self):
        return self.__upBound

    def set(self):
        self.__lowBound = input('Please input low bound\n')
        self.__upBound = input('Please input up bound\n')

        self.__lowBound = int(self.__lowBound) if self.__lowBound.isdigit() else None
        self.__upBound = int(self.__upBound) if self.__upBound.isdigit() else None

        if not self.__lowBound == None and not self.__upBound == None and (self.__lowBound > self.__upBound):    #Bounded error
            self.__lowBound = None
            self.__upBound = None

        if self.__lowBound == None and self.__upBound == None:
            print('result will be not with filter')
        elif self.__lowBound == None:
            print('up bound is setted to ' + str(self.__upBound))
        elif self.__upBound == None:
            print('low bound is setted to ' + str(self.__lowBound))
        else:
            print('low bound is setted to ' + str(self.__lowBound) + '\nup bound is setted to ' + str(self.__upBound))

    def priceFilter(self, results):
        if self.__lowBound == None and self.__upBound == None:
            return results

        elif self.__lowBound == None:
            resultsFilted = []
            for result in results:
                if result.getPrice() <= self.__upBound:
                    resultsFilted.append(result)

            return resultsFilted

        elif self.__upBound == None:
            resultsFilted = []
            for result in results:
                if result.getPrice() >= self.__lowBound:
                    resultsFilted.append(result)

            return resultsFilted

        else:
            resultsFilted = []
            for result in results:
                if result.getPrice() >= self.__lowBound and result.getPrice() <= self.__upBound:
                    resultsFilted.append(result)

            return resultsFilted
