# Flight Reservation System (Searching and Sorting)
**Savitribai Phule Pune University (SPPU) - 2024 Pattern**  
**Course:** Data Structures Laboratory (`PCC-204-COM`)  
**Department:** Computer Engineering (Second Year / SE)

---

## 📌 Project Overview
The **Flight Reservation System** is a console-based application designed to demonstrate the fundamental principles of **Searching and Sorting Algorithms** applied to a practical domain. Built entirely using the Python Standard Library, this project provides manual implementations of classic algorithmic techniques without relying on built-in search or sort primitives.

---

## 📂 Project Structure
```text
flight_reservation/
├── flight_reservation.py       # Main program with interactive menu & core algorithms
├── test_flight_reservation.py  # Unit tests covering all 10 specifications (unittest)
├── benchmark.py                # Performance benchmark (100, 500, 1000, 2000 flights)
├── flights.json                # JSON persistence for flights and bookings
└── README.md                   # Documentation and run instructions
```

---

## 🧮 Data Structures & Schema
1. **Flights:** A list of dictionaries, maintained sorted by `no` at all times:
   - `no` (*int*): Unique Flight Number (e.g., 101)
   - `airline` (*str*): Operating airline name (e.g., "IndiGo")
   - `src` (*str*): Departure city (e.g., "Pune")
   - `dest` (*str*): Destination city (e.g., "Delhi")
   - `dep` (*str*): Departure time formatted as `HH:MM`
   - `price` (*int*): Ticket price in INR
   - `dur` (*int*): Flight duration in minutes
   - `seats` (*int*): Number of available seats (includes a sold-out flight with 0 seats)
2. **Bookings:** A list of dictionaries:
   - `id` (*int*): Booking reference ID (starts from 1001)
   - `name` (*str*): Passenger name
   - `flight` (*int*): Associated flight number
   - `seats` (*int*): Number of reserved seats

---

## 🔍 Searching Algorithms Implemented
1. **Linear Search (`linear_search_route`):**
   - **Usage:** Searches flights matching source and destination cities (case-insensitive).
   - **Time Complexity:** 
     - Best Case: $\mathcal{O}(N)$
     - Average Case: $\mathcal{O}(N)$
     - Worst Case: $\mathcal{O}(N)$
   - **Space Complexity:** $\mathcal{O}(k)$ (where $k$ is number of matches found)

2. **Binary Search (`binary_search_flight_no`):**
   - **Usage:** Searches a flight by its unique flight number on a sorted list.
   - **Time Complexity:**
     - Best Case: $\mathcal{O}(1)$ (target at middle element)
     - Average Case: $\mathcal{O}(\log N)$
     - Worst Case: $\mathcal{O}(\log N)$
   - **Space Complexity:** $\mathcal{O}(1)$ (iterative approach)

---

## 📊 Sorting Algorithms Implemented
All sorting algorithms are implemented from scratch, return a new list, accept a custom `key` lambda, and support comparison counting:

| Algorithm | Best Case Time | Average Case Time | Worst Case Time | Space Complexity | Stability |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Bubble Sort** (Early-Exit) | $\mathcal{O}(N)$ | $\mathcal{O}(N^2)$ | $\mathcal{O}(N^2)$ | $\mathcal{O}(N)$ | Stable |
| **Selection Sort** | $\mathcal{O}(N^2)$ | $\mathcal{O}(N^2)$ | $\mathcal{O}(N^2)$ | $\mathcal{O}(N)$ | Unstable |
| **Insertion Sort** | $\mathcal{O}(N)$ | $\mathcal{O}(N^2)$ | $\mathcal{O}(N^2)$ | $\mathcal{O}(N)$ | Stable |
| **Merge Sort** | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N)$ | Stable |
| **Quick Sort** | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N^2)$ | $\mathcal{O}(\log N)$ | Unstable |

---

## 🚀 How to Run

### Prerequisites
- Python 3.8+ installed (no external libraries required).

### 1. Run the Main Program
Navigate to the directory and run:
```bash
python flight_reservation/flight_reservation.py
```
Or from within the `flight_reservation` folder:
```bash
cd flight_reservation
python flight_reservation.py
```

### 2. Run the Unit Tests
Execute the 10 automated test cases via `unittest`:
```bash
python -m unittest flight_reservation/test_flight_reservation.py -v
```

### 3. Run the Performance Benchmark
Compare sorting algorithms across 100, 500, 1000, 2000 flights and benchmark linear vs. binary search:
```bash
python flight_reservation/benchmark.py
```

---

## 🧪 Test Suite Coverage (10 Cases)
- **Test 1:** Linear search `Pune -> Delhi` returns flights 101 and 102.
- **Test 2:** Linear search `Pune -> Goa` returns empty list `[]`.
- **Test 3:** Binary search flight `104` returns flight record.
- **Test 4:** Binary search non-existent flight `999` returns `-1`.
- **Test 5:** Verification of Bubble, Selection, Insertion, Merge, and Quick sorts against Python's `sorted()` reference.
- **Test 6:** Booking 2 seats on flight 101 reduces available seats from 5 to 3.
- **Test 7:** Booking more seats than available is gracefully rejected.
- **Test 8:** Booking on a 0-seat flight (Flight 109) is rejected.
- **Test 9:** Cancelling a valid booking restores the reserved seats to the flight.
- **Test 10:** Cancelling non-existent booking ID (`5555`) returns appropriate not found error.
