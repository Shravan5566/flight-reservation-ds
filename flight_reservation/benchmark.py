"""
Benchmark Script for Flight Reservation System
SPPU 2024 Pattern, PCC-204-COM: Data Structures Laboratory

Times and compares:
1. Five manual sorting algorithms (Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort)
   across dataset sizes of 100, 500, 1000, and 2000 flights.
2. Linear search vs. Binary search timing comparison on the largest dataset (2000 flights).
"""

import random
import time
from flight_reservation import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    linear_search_route,
    binary_search_flight_no
)

AIRLINES = ["IndiGo", "Air India", "SpiceJet", "Vistara", "Akasa Air"]
CITIES = ["Pune", "Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Kolkata", "Goa", "Jaipur", "Ahmedabad"]


def generate_random_flights(n):
    """
    Generates n random flight records with unique flight numbers sorted in ascending order.
    """
    # Generate n unique flight numbers
    flight_nos = sorted(random.sample(range(100, 100 + n * 10), n))
    flights = []
    for f_no in flight_nos:
        src, dest = random.sample(CITIES, 2)
        hour = random.randint(0, 23)
        minute = random.choice([0, 15, 30, 45])
        dep_str = f"{hour:02d}:{minute:02d}"
        price = random.randint(2000, 12000)
        dur = random.randint(45, 300)
        seats = random.randint(0, 50)
        airline = random.choice(AIRLINES)
        flights.append({
            "no": f_no,
            "airline": airline,
            "src": src,
            "dest": dest,
            "dep": dep_str,
            "price": price,
            "dur": dur,
            "seats": seats
        })
    return flights


def benchmark_sorting():
    """
    Benchmarks all 5 sorting algorithms on sizes 100, 500, 1000, and 2000.
    """
    sizes = [100, 500, 1000, 2000]
    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Selection Sort", selection_sort),
        ("Insertion Sort", insertion_sort),
        ("Merge Sort", merge_sort),
        ("Quick Sort", quick_sort)
    ]

    print("=" * 82)
    print("      BENCHMARK: SORTING ALGORITHMS EMPIRICAL TIME COMPARISON")
    print("      (Keys: Flight Price, randomly shuffled data)")
    print("=" * 82)

    # Header
    header = f"{'Algorithm':<18} | " + " | ".join([f"N={sz:<6} (sec)" for sz in sizes])
    print(header)
    print("-" * 82)

    # Generate test datasets beforehand so every algorithm sorts the exact same data
    datasets = {}
    for sz in sizes:
        base_data = generate_random_flights(sz)
        # Shuffle order so sorting does real work
        random.shuffle(base_data)
        datasets[sz] = base_data

    # Run benchmarks
    price_key = lambda f: f["price"]

    for name, sort_fn in algorithms:
        row_str = f"{name:<18} | "
        times = []
        for sz in sizes:
            # Create a shallow copy of the dataset for this run
            data_copy = [dict(x) for x in datasets[sz]]
            t0 = time.perf_counter()
            sort_fn(data_copy, key=price_key)
            t1 = time.perf_counter()
            elapsed = t1 - t0
            times.append(f"{elapsed:>11.6f}s")
        row_str += " | ".join(times)
        print(row_str)

    print("-" * 82)
    print("Observations:")
    print(" - Bubble, Selection, and Insertion sorts display O(N^2) quadratic growth.")
    print(" - Merge and Quick sorts scale efficiently with O(N log N) performance.")
    print("=" * 82)


def benchmark_searching():
    """
    Compares Linear Search vs. Binary Search on the 2000-flight dataset.
    """
    print("\n" + "=" * 82)
    print("      BENCHMARK: LINEAR SEARCH VS. BINARY SEARCH (N = 2000)")
    print("=" * 82)

    n = 2000
    flights = generate_random_flights(n)  # Already sorted by flight 'no'

    # Target: Pick an element near the end of the array to demonstrate worst-case linear search
    target_flight = flights[-1]
    target_no = target_flight["no"]
    target_src = target_flight["src"]
    target_dest = target_flight["dest"]

    # 1. Linear Search for route
    # Run 1000 repetitions to get measurable average microsecond timings
    reps = 1000
    t0 = time.perf_counter()
    for _ in range(reps):
        linear_search_route(flights, target_src, target_dest)
    t1 = time.perf_counter()
    linear_avg_us = ((t1 - t0) / reps) * 1_000_000

    # 2. Binary Search for flight number
    t0 = time.perf_counter()
    for _ in range(reps):
        binary_search_flight_no(flights, target_no)
    t1 = time.perf_counter()
    binary_avg_us = ((t1 - t0) / reps) * 1_000_000

    print(f"Dataset Size             : {n} flights")
    print(f"Iterations averaged      : {reps}")
    print(f"Linear Search Route (O(N)): {linear_avg_us:10.3f} microseconds / search")
    print(f"Binary Search No (O(logN)): {binary_avg_us:10.3f} microseconds / search")
    speedup = linear_avg_us / binary_avg_us if binary_avg_us > 0 else 1.0
    print(f"Speedup Factor           : {speedup:10.2f}x faster with Binary Search")
    print("=" * 82)


if __name__ == "__main__":
    # Seed for reproducibility of benchmark report
    random.seed(42)
    benchmark_sorting()
    benchmark_searching()
