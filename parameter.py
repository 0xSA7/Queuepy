from math import inf
from numpy import random

class Params:
    """
    Represents parameters for a queuing system.
    This class serves as an abstract base class for specific queuing models.
    """

    def __init__(self, lumbda: float, mu: float, numberOfServers: int = 1, systemCapacity: float = inf) -> None:
        """
        Initializes the parameters.
        """
        self.lumbda = lumbda
        self.mu = mu
        self.numberOfServers = numberOfServers
        self.systemCapacity = systemCapacity

    def findL(self) -> float:
        """Calculates and returns the average number of customers in the system (L)."""
        raise NotImplementedError("This method should be implemented in subclasses.")

    def findLq(self) -> float:
        """Calculates and returns the average number of customers in the queue (Lq)."""
        raise NotImplementedError("This method should be implemented in subclasses.")

    def findW(self) -> float:
        """Calculates and returns the average time a customer spends in the system (W)."""
        raise NotImplementedError("This method should be implemented in subclasses.")

    def findWq(self) -> float:
        """Calculates and returns the average time a customer spends in the queue (Wq)."""
        raise NotImplementedError("This method should be implemented in subclasses.")

    def findPk(self, k: int) -> float:
        """Calculates and returns the probability of having k customers in the system (Pk)."""
        raise NotImplementedError("This method should be implemented in subclasses.")

    def findRu(self) -> float:
        """Calculates and returns the server utilization (Ru)."""
        raise NotImplementedError("This method should be implemented in subclasses.")

    def display(self) -> None:
        """Displays the calculated performance measures."""
        print(f" L = {self.findL()} \n Lq = {self.findLq()} \n W = {self.findW()} \n Wq = {self.findWq()}")






