from parameter import Params
from math import pow, factorial
from math import inf
from simulation import simulate, chart

###M/M/1
class MM1(Params):   
    """
    Represents an M/M/1 queuing system.
    """

    def __init__(self, lumbda: float, mu: float) -> None:
        """
        Initializes the M/M/1 system parameters.
        """
        # Validate inputs
        if lumbda >= mu:
            raise ValueError("Arrival rate (lumbda) must be less than service rate (mu) for stability.")

        super().__init__(lumbda, mu)   

    def findL(self) -> float:
        """Calculates and returns the average number of customers in the system (L)."""
        return self.lumbda / (self.mu - self.lumbda)   

    def findLq(self) -> float:
        """Calculates and returns the average number of customers in the queue (Lq)."""
        return (self.findL() * self.lumbda) / self.mu   

    def findW(self) -> float:
        """Calculates and returns the average time a customer spends in the system (W)."""
        return 1 / (self.mu - self.lumbda)

    def findWq(self) -> float:
        """Calculates and returns the average time a customer spends in the queue (Wq)."""
        return (self.findW() * self.lumbda) / self.mu   

    def findPk(self, k: int) -> float:
        """Calculates and returns the probability of having k customers in the system (Pk)."""
        return pow(self.findRu(), k) * (1 - self.findRu())

    def findRu(self) -> float:
        """Calculates and returns the server utilization (Ru)."""
        return self.lumbda / self.mu

    def display(self) -> None:
        """Displays the calculated performance measures."""
        print(f"L: {self.findL()}")
        print(f"Lq: {self.findLq()}")
        print(f"W: {self.findW()}")
        print(f"Wq: {self.findWq()}")
        print(f"Ru: {self.findRu()}")

####M/M/1/K
class MM1K(Params):  
    """
    Represents an M/M/1/K queuing system.
    """

    def __init__(self, lumbda: float, mu: float, systemCapacity: int) -> None:
        """
        Initializes the M/M/1/K system parameters.
        """
        # Validate inputs
        if lumbda >= mu:
            raise ValueError("Arrival rate (lumbda) must be less than service rate (mu) for stability.")
        if systemCapacity <= 0:
            raise ValueError("System capacity must be a positive integer.")

        super().__init__(lumbda, mu, systemCapacity=systemCapacity)
        self._sc = systemCapacity
        self._ru = self.findRu()
        self._ruK = pow(self._ru, systemCapacity)
        self._ruK1 = pow(self._ru, systemCapacity + 1)

    def findL(self) -> float:
        """Calculates and returns the average number of customers in the system (L)."""
        if self._ru == 1:
            return self._sc / 2.0   
        else:
            numerator = self._ru * (1 - (self._sc + 1) * self._ruK + self._sc * self._ruK1)
            denominator = (1 - self._ru) * (1 - self._ruK1)
            return numerator / denominator

    def findLq(self) -> float:
        """Calculates and returns the average number of customers in the queue (Lq)."""
        return self._findLambdaDash() * self.findWq()

    def findW(self) -> float:
        """Calculates and returns the average time a customer spends in the system (W)."""
        return self.findL() / self._findLambdaDash()

    def findWq(self) -> float:
        """Calculates and returns the average time a customer spends in the queue (Wq)."""
        return self.findW() - (1.0 / self.mu)

    def findPk(self, k: int) -> float:
        """Calculates and returns the probability of having k customers in the system (Pk)."""
        if self._ru == 1:
            return 1.0 / (self._sc + 1.0)
        else:
            return self._ruK * ((1 - self._ru) / (1 - self._ruK1))

    def _findLambdaDash(self) -> float:
        """Calculates and returns the effective arrival rate (lambda_dash)."""
        return self.lumbda * (1 - self.findPk(self._sc))

    def findRu(self) -> float:
        """Calculates and returns the server utilization (Ru)."""
        return self.lumbda / self.mu

    def display(self) -> None:
        """Displays the calculated performance measures."""
        print(f"L: {self.findL()}")
        print(f"Lq: {self.findLq()}")
        print(f"W: {self.findW()}")
        print(f"Wq: {self.findWq()}")
        print(f"Ru: {self.findRu()}")

###M/M/C
class MMC(Params):   
    """
    Represents an M/M/c queuing system.
    """

    def __init__(self, lumbda: float, mu: float, numberOfServers: int) -> None:
        """
        Initializes the M/M/c system parameters.
        """
        # Validate inputs
        if lumbda >= mu * numberOfServers:
            raise ValueError("Arrival rate (lumbda) must be less than service rate (mu) * number of servers (c) for stability.")
        if numberOfServers <= 0:
            raise ValueError("Number of servers must be a positive integer.")

        super().__init__(lumbda, mu, numberOfServers=numberOfServers)
        self.c = numberOfServers
        self.findR = self.lumbda / self.mu   
        self.P0 = self.findP0() 
        self._Lq = self.findLq()   

    def findL(self) -> float:
        """Calculates and returns the average number of customers in the system (L)."""
        return self._Lq + self.findR  

    def findLq(self) -> float:
        """Calculates and returns the average number of customers in the queue (Lq)."""
        numerator = (pow(self.findR, self.c + 1) / self.c)
        denominator = factorial(self.c) * (pow(1 - (self.findR / self.c), 2))
        return (numerator / denominator) * self.P0

    def findW(self) -> float:
        """Calculates and returns the average time a customer spends in the system (W)."""
        return (self._Lq / self.lumbda) + (1 / self.mu)

    def findWq(self) -> float:
        """Calculates and returns the average time a customer spends in the queue (Wq)."""
        return self._Lq / self.lumbda

    def findPk(self, k: int) -> float:
        """Calculates and returns the probability of having k customers in the system (Pk)."""
        if k < self.c:
            return (pow(self.lumbda, k) / (factorial(k) * pow(self.mu, k))) * self.P0
        else:
            return (pow(self.lumbda, k) / (pow(self.c, k - self.c) * factorial(self.c) * pow(self.mu, k))) * self.P0

    def findRu(self) -> float:
        """Calculates and returns the server utilization (Ru)."""
        return self.findR / self.c

    def findP0(self) -> float:
        """Calculates and returns the probability of having 0 customers in the system (P0)."""
        r = self.findR
        ru = self.findRu()
        c = self.c
        first = 0

        if ru < 1:
            for i in range(c):
                first += pow(r, i) / factorial(i)
            return 1 / (first + ((c * pow(r, c)) / (factorial(c) * (c - r))))
        else:
            for i in range(c):
                first += (1 / factorial(i)) * pow(r, i)
            return 1 / (first + ((1 / factorial(c)) * pow(r, c) * ((c * self.mu) / (c * self.mu - self.lumbda))))

    def display(self) -> None:
        """Displays the calculated performance measures."""
        print(f"L: {self.findL()}")
        print(f"Lq: {self.findLq()}")
        print(f"W: {self.findW()}")
        print(f"Wq: {self.findWq()}")
        print(f"Ru: {self.findRu()}")

####M/M/C/K
class MMCK(Params):   
    """
    Represents an M/M/c/K queuing system.
    """

    def __init__(self, lumbda: float, mu: float, numberOfServers: int, systemCapacity: int) -> None:
        """
        Initializes the M/M/c/K system parameters.
        """
        # Validate inputs
        #if lumbda >= mu * numberOfServers:
            #raise ValueError("Arrival rate (lumbda) must be less than service rate (mu) * number of servers (c) for stability.")
        if numberOfServers <= 0:
            raise ValueError("Number of servers must be a positive integer.")
        if systemCapacity <= 0:
            raise ValueError("System capacity must be a positive integer.")

        super().__init__(lumbda, mu, numberOfServers=numberOfServers, systemCapacity=systemCapacity)
        self.c = numberOfServers
        self.sc = systemCapacity
        self.findR = self.lumbda / self.mu   
        self.findp0 = self.findP0()  
        self.findLambdaDash = self.lumbda * (1 - self.findPk(self.sc))  

    def findL(self) -> float:
        """Calculates and returns the average number of customers in the system (L)."""
        last = sum((self.c - i) * (pow(self.findR, i) / factorial(i)) for i in range(self.c))
        return self.findLq() + self.c - self.findp0 * last

    def findLq(self) -> float:
        """Calculates and returns the average number of customers in the queue (Lq)."""
        ru = self.findRu()
        numerator = ru * pow(self.findR, self.c) * self.findp0
        denominator = factorial(self.c) * pow(1 - ru, 2)
        blocking_factor = (1 - pow(ru, self.sc - self.c + 1) - (1 - ru) * (self.sc - self.c + 1) * pow(ru, self.sc - self.c))
        return (numerator / denominator) * blocking_factor

    def findW(self) -> float:
        """Calculates and returns the average time a customer spends in the system (W)."""
        return self.findL() / self.findLambdaDash

    def findWq(self) -> float:
        """Calculates and returns the average time a customer spends in the queue (Wq)."""
        return self.findLq() / self.findLambdaDash

    def findPk(self, n: int) -> float:
        """Calculates and returns the probability of having n customers in the system (Pk)."""
        if n < self.c:
            return (pow(self.findR, n) / factorial(n)) * self.findp0
        return (pow(self.findR, n) / (pow(self.c, n - self.c) * factorial(self.c))) * self.findp0

    def findP0(self) -> float:
        """Calculates and returns the probability of having 0 customers in the system (P0)."""
        first = sum(pow(self.findR, i) / factorial(i) for i in range(self.c))
        ru = self.findRu()
        if ru != 1:
            return 1 / (first + (pow(self.findR, self.c) / factorial(self.c)) * ((1 - pow(ru, self.sc - self.c + 1)) / (1 - ru)))
        else:
            return 1 / (first + (pow(self.findR, self.c) / factorial(self.c)) * (self.sc - self.c + 1))

    def findRu(self) -> float:
        """Calculates and returns the server utilization (Ru)."""
        return self.findR / self.c

    def display(self) -> None:
        """Displays the calculated performance measures."""
        print(f"L: {self.findL()}")
        print(f"Lq: {self.findLq()}")
        print(f"W: {self.findW()}")
        print(f"Wq: {self.findWq()}")
        print(f"Ru: {self.findRu()}")

    
def solution(lumbda: float, mu: float, numberOfServers: int = 1, systemCapacity: float = inf) -> None:
    if numberOfServers == 1:
        if systemCapacity == inf or systemCapacity == 0:
            MM1(lumbda, mu).display()
        else:
            MM1K(lumbda, mu, systemCapacity).display()
    else:
        if systemCapacity == inf:
            MMC(lumbda, mu, numberOfServers).display()
        else:
            MMCK(lumbda, mu, numberOfServers, systemCapacity).display()
    
          

def ask_user() -> None:
    arrival_rate = float(input("Enter the arrival rate (lambda): "))
    service_rate = float(input("Enter the service rate (mu): "))
    servers = int(input("Enter the Number of Servers (c):"))
    capacity_input = input("Enter the system capacity (k) (leave empty for infinity): ")
    capacity = inf if capacity_input == "" else int(capacity_input)
    solution(arrival_rate, service_rate, servers, capacity)
    simulate(arrival_rate, service_rate, 0)
    chart()
