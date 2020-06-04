class Goods():

    name = None
    price = 0
    site = None
    def __init__(self, name = None, price = 0, site = None):
        self.name = name
        self.price = price
        self.site = site

    def setName(self, name):
        self.name = name

    def setPrice(self, price):
        self.price = price

    def setSite(self, site):
        self.site = site

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getSite(self):
        return self.site
  
    def getByList(self):
        r = []
        r.append(self.name)
        r.append(self.price)
        r.append(self.site)

        return r

    def showDetail(self):
        print('name:', self.name, '\nprice:', self.price, '\nsite:', self.site)
