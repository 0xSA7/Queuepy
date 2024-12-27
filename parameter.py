from math import inf
from numpy import random

class Params:
    """
    Represents parameters for a queuing system.
    This class serves as an abstract base class for specific queuing models.
    """

    def __init__(self, lumbda, mu, numberOfServers=1, systemCapacity=inf):
        """
        Initializes the parameters.
        """
        self.lumbda = lumbda
        self.mu = mu
        self.numberOfServers = numberOfServers
        self.systemCapacity = systemCapacity

    def findL(self):
        """Calculates and returns the average number of customers in the system (L)."""
        raise NotImplementedError("This method should be implemented in subclasses.")

    def findLq(self):
        """Calculates and returns the average number of customers in the queue (Lq)."""
        raise NotImplementedError("This method should be implemented in subclasses.")

    def findW(self):
        """Calculates and returns the average time a customer spends in the system (W)."""
        raise NotImplementedError("This method should be implemented in subclasses.")

    def findWq(self):
        """Calculates and returns the average time a customer spends in the queue (Wq)."""
        raise NotImplementedError("This method should be implemented in subclasses.")

    def findPk(self, k):
        """Calculates and returns the probability of having k customers in the system (Pk)."""
        raise NotImplementedError("This method should be implemented in subclasses.")

    def findRu(self):
        """Calculates and returns the server utilization (Ru)."""
        raise NotImplementedError("This method should be implemented in subclasses.")

    def display(self):
        """Displays the calculated performance measures."""
        print(f" L = {self.findL()} \n Lq = {self.findLq()} \n W = {self.findW()} \n Wq = {self.findWq()}")

    def generate_random_params(self, num_customers):

        p1 = random.exponential(scale=self.lumbda, size=num_customers)
        p2 = random.exponential(scale=self.mu, size=num_customers)

        return p1, p2

        