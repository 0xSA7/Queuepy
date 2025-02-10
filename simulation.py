from numpy import random
from tabulate import tabulate
import matplotlib.pyplot as plt
from typing import List

completion_times, arrival_times = [], []

def simulate(lumbda: float, mu: float, num_customers: int = 0) -> None:
    """Simulates a single-server queuing system.

    Args:
        lumbda (float): The arrival rate.
        mu (float): The service rate.
        num_customers (int): The number of customers to simulate. Defaults to 0.

    Returns:
        None. Prints the simulation results to the console.
    """
    
    # Load the values of Global Variables
    global completion_times, arrival_times
    
    # Check if app operates as CLI vs GUI
    if num_customers == 0:
        num_customers = int(input("Enter the number of customers: "))

    interarrival_times = 0.1*random.exponential(scale=lumbda, size=num_customers)
    service_times  = 0.1*random.exponential(scale=mu, size=num_customers)

    # Check if the length of interarrival_times and service_times are the same
    if len(interarrival_times) != len(service_times):
        raise ValueError("Interarrival times and service times must have the same length")

    arrival_times = [0]  # Arrival time of the first customer is 0
    for i in range(1, num_customers):
        arrival_times.append(arrival_times[i - 1] + interarrival_times[i])

    start_service_times = [0]
    for i in range(1, num_customers):
        start_service_times.append(
            max(arrival_times[i], start_service_times[i - 1] + service_times[i - 1])
        )

    completion_times = [start_service_times[0] + service_times[0]]
    for i in range(1, num_customers):
        completion_times.append(start_service_times[i] + service_times[i])

    time_in_system = [
        completion_times[i] - arrival_times[i] for i in range(num_customers)
    ]

    time_in_queue = [
        start_service_times[i] - arrival_times[i] for i in range(num_customers)
    ]

    server_idle_times = [0]
    for i in range(1, num_customers):
        server_idle_times.append(
            max(0, arrival_times[i] - (start_service_times[i - 1] + service_times[i - 1]))
        )


    # Ensure all lists have the same length before creating the DataFrame
    min_len = min(len(arrival_times), len(start_service_times), len(completion_times), len(time_in_system), len(time_in_queue), len(server_idle_times))

    arrival_times = arrival_times[:min_len]
    start_service_times = start_service_times[:min_len]
    completion_times = completion_times[:min_len]
    time_in_system = time_in_system[:min_len]
    time_in_queue = time_in_queue[:min_len]
    server_idle_times = server_idle_times[:min_len]
    interarrival_times = interarrival_times[:min_len]
    service_times = service_times[:min_len]

    # customer_number was originally intended to be a list of numbers from 1 to num_customers
    # let's adjust this to be a list of the same length as the others.
    customer_number = list(range(1, min_len + 1))

    """
    data = {
        "Customer Number": customer_number,
        "Interarrival Times": interarrival_times,
        "Arrival Times": arrival_times,
        "Service Times": service_times,
        "Time Service Begins": start_service_times,
        "Completion Times": completion_times,
        "Time in Queue": time_in_queue,
        "Time in System": time_in_system,
        "Server Idle Times": server_idle_times,
    }

    df = pd.DataFrame(data)
    table = tabulate(df, headers='keys', tablefmt='presto') 
    print(table)
    """
    table_data = [
        [i + 1, arrival_time, service_begin_time, service_time, service_end_time,
         time_in_queue, time_in_system]
        for i, (arrival_time, service_begin_time, service_time, service_end_time,
                time_in_queue, time_in_system) in
        enumerate(zip(arrival_times,start_service_times, service_times,
                      completion_times,  time_in_queue, time_in_system))
    ]

    # Calculate performance metrics          
    performance_metrics(time_in_queue, service_times, interarrival_times, time_in_system)
    
    # Use tabulate to format the output
    print(tabulate(table_data, headers=["Customer", "Arrival Time", "Service Begin Time",
                                      "Service Time", "Service End Time",
                                      "Time in Queue", "Time in System"],
                   tablefmt="fancy_grid"))


def performance_metrics(time_in_queue: List[float], service_times: List[float], interarrival_times: List[float], time_in_system: List[float]) -> None:
    """Calculates and prints performance metrics for the queuing system.

    Args:
        time_in_queue (List[float]): List of times customers spend in the queue.
        service_times (List[float]): List of service times.
        interarrival_times (List[float]): List of interarrival times.
        time_in_system (List[float]): List of times customers spend in the system.

    Returns:
        None. Prints the performance metrics to the console.
    """
  # Calculate performance metrics
    avg_waiting_time = sum(time_in_queue) / len(time_in_queue)
    avg_service_time = sum(service_times) / len(service_times)
    avg_interarrival_time = sum(interarrival_times[1:]) / len(interarrival_times[1:])  # Exclude the initial 0
    avg_waiting_time_those_who_wait = sum(t for t in time_in_queue if t > 0) / sum(1 for t in time_in_queue if t > 0) if any(t > 0 for t in time_in_queue) else 0  # Handle cases where no one waits
    avg_time_in_system = sum(time_in_system) / len(time_in_system)

   # Print the performance metrics
    print("\nPerformance Metrics:")
    print(f"Average Waiting Time: {avg_waiting_time:.2f}")
    print(f"Average Service Time: {avg_service_time:.2f}")
    print(f"Average Time Between Arrivals: {avg_interarrival_time:.2f}")
    print(f"Average Waiting Time of Those Who Wait: {avg_waiting_time_those_who_wait:.2f}")
    print(f"Average Time a Customer Spends in the System: {avg_time_in_system:.2f}")
    print("\n",flush=True)



def chart() -> None:
    """Generates and displays a chart of the number of customers in the system over time.

    Returns:
        None. Displays a chart using matplotlib.
    """
    # Load the values of the Global Variable
    global completion_times, arrival_times
    service_end_times = completion_times
    
    time_points = []
    customer_count = []
    current_customers = 0
    events = []

    for i in range(len(arrival_times)):
        events.append((arrival_times[i], 1)) 
        events.append((service_end_times[i], -1))
    
    # Sort events by time
    events.sort()
    
    for time, event_type in events:
        time_points.append(time)
        current_customers += event_type
        customer_count.append(current_customers)
        

    plt.figure(figsize=(10, 6))   
    plt.step(time_points, customer_count, where='post')  # Use step plot for discrete events
    plt.xlabel("Time")
    plt.ylabel("Number of Customers in System")
    plt.title("Customer Count Over Time")
    plt.grid(True)
    plt.show()