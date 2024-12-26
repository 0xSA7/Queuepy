from parameter import params
from math import pow, factorial


###M/M/1
class mm1(params):

    def _init_(self, lumbda, mu):
        super(lumbda, mu)


    def findL(self):
        return self.lumbda // (self.mu - self.lumbda)
    

    def findLq(self):
        return (self.findL() * self.lumbda // self.mu)
    

    def findW(self):
         return (1/ (self.mu - self.lumbda))
    

    def findWq(self):
        return (self.findW() * self.lumbda / self.mu)
    

    def findPk(self, k):
        return pow(self.findRu(), k) * (1 - self.findRu())


    def findRu(self):
         return self.lumbda / self.mu


####M/M/1/K
class mm1k(params):

   
    def _init_(self, lumbda, mu, systemcapacuty):
            super(lumbda, mu, systemcapacuty=systemcapacuty)
            self._sc = self.systemCapacity
            self._ru = self.findRu()
            self._ruK = pow(self._ru, self.systemCapacity)
            self._ruK1 = pow(self._ru, self.systemCapacity + 1)

   
    def findL(self):
        return self._sc // 2   \
            if self._ru == 1   \
                    else self._ru * ((1 - (self._sc + 1) * self._ruK + self._sc * self._ruK1)/ ((1- self._ru)* (1 - self._ruK1)))
        

    def findLq(self):
        return self._findLambdaDash() * self.findWq()
    

    def findW(self):
            return self.findL() / self._findLambdaDash()


    def findWq(self):
        return  self.findW() - (1.0/self.mu)


    def findPk(self, k):
         return 1.0/ (self._sc + 1.0) \
            if self._ru == 1 \
                else  self._ruK * ((1 - self._ru)/(1-self._ruK1))
    

    def _findLambdaDash(self):
        return self.lumbda * (1 - self.findPk(self._sc))
     

    def findRu(self):
            return self.lumbda / self.mu


###M/M/C
class mmc(params):
     
    def _init_(self, lumbda, mu, numberofServers):
        super(lumbda, mu, numberOfServers=numberofServers)
        self.c = numberofServers
        self.findR = self.lumbda / self.mu
        self._Lq = self.findLq()
        self.P0 = self.findP0()


    def findL(self):
       return self._Lq + self.findR()
    

    def findLq(self):
         return ((pow(self.findR(), self.c+1) / self.c) / (factorial(self.c) * (pow( 1 - self.findR() / self.c, 2)))) * self.P0
    

    def findW(self):
         return self._Lq/self.lumbda + 1/self.mu
    

    def findWq(self):
        return self._Lq / self.lumbda
    

    def findPk(self, k):
        
        return  pow(self.lumbda, k)/(factorial(k)* pow(self.mu, k)) * self.P0\
            if k < self.c \
                else pow(self.lumbda, k) / (pow(self.c, k - self.c) * factorial(self.c) * pow(self.mu, k)) * self.P0


    def findRu(self):
         return self.findR / self.c
    
    
    def findP0(self):
        r = self.findR
        ru = self.findRu()
        c = self.c
        first = 0

        if ru < 1:
            for i in range(c):
                first += pow(r, i) / factorial(i)
            return 1/ (first + ((c * pow(r, c))/(factorial(c)*(c - r))))
        
        for i in range(c):
            first += (1/factorial(i)) * pow(r, i)
        return 1/ (first + ((1/factorial(c)) * pow(r, c) * ((c*self.mu)/(c * self.mu - self.lumbda))))


####M/M/C/K
class mmck(params):

    def _init_(self,lumbda, mu, numberOfServers, systemCapacity):
         super(lumbda, mu, numberOfServers, systemCapacity)
         self.c = numberOfServers
         self.sc = systemCapacity
         self.findR = self.lumbda / self.mu
         self.findLambdaDash = self.lumbda * (1 - self.findPk(self.k))
         self.findp0 = self.findP0()

    def findL(self):
        last = 0
        for i in range(self.c):
            last += (self.c - i) * (pow(self.findR, i) / factorial(i))
        return self.findLq() + self.c - self.findp0 * last
    
    
    def findLq(self):
        return (self.findRu() * pow(self.findR, self.c) * self.findp0) \
            / (factorial(self.c) * pow(1 - self.findRu(), 2))  \
               * (1 - pow(self.findRu(), self.k - self.c + 1) - (1 - self.findRu()) \
                  * (self.k - self.c + 1) * pow(self.findRu(), self.k - self.c))
    

    def findW(self):
        return self.findL() / self.findLambdaDash
    

    def findWq(self):
        return self.findLq() / self.findLambdaDash
    

    def findPk(self, n):
        if n < self.c:
            return (pow(self.findR, n) / factorial(n)) * self.findp0
        return (pow(self.findR, n) / (pow(self.c, n-self.c) * factorial(self.c))) * self.findp0


    def findP0(self):
        first = 0
        for i in range(self.c):
            first += pow(self.findR, i) / factorial(i)
            
        return 1 / (first + (pow(self.findR, self.c) / factorial(self.c)) \
                        * ((1 - pow(self.findRu(), self.k - self.c + 1)) / (1- self.findRu()))) \
                        if self.findRu() != 1  \
                         else 1 / (first + (pow(self.findR, self.c) / factorial(self.c)) * (self.k - self.c + 1));


    def findRu(self):
         return  self.findR / self.c

   
