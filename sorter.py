class Sorter():
    __highToLow = False
    __lowToHigh = False

    def __init__(self, highToLow = False, lowToHigh = False):
        self.__highToLow = highToLow
        self.__lowToHigh = lowToHigh

    def set(self):
        howToSort = input('If you want sort by high to low, input h\nIf you want sort by low to high, input l\n')
        if howToSort == 'h':
            self.__highToLow = True
            print('the price of data will be sort by high to low')
        elif howToSort == 'l':
            self.__lowToHigh = True
            print('the price of data will be sort by low to high')
        else:
            print('the price of data will be not sorted')

    def sort(self, results):
        if self.__highToLow == False and self.__lowToHigh == False:
            return results
        elif self.__highToLow:
            results.sort(key=lambda r: r.price, reverse=True)
            return results
        elif self.__lowToHigh:
            results.sort(key=lambda r: r.price)
            return results
