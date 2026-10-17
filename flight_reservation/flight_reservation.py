"""
Flight Reservation System (Searching and Sorting)
SPPU 2024 Pattern, PCC-204-COM: Data Structures Laboratory
Second Year Computer Engineering

Core logic module containing data structures, manual searching algorithms,
manual sorting algorithms, and reservation management.
"""

import json
import os
import time

DATA_FILE = "flights.json"

DEFAULT_FLIGHTS = [
    {"no": 101, "airline": "IndiGo", "src": "Pune", "dest": "Delhi", "dep": "06:15", "price": 4500, "dur": 135, "seats": 5},
    {"no": 102, "airline": "Air India", "src": "Pune", "dest": "Delhi", "dep": "14:30", "price": 5200, "dur": 140, "seats": 12},
    {"no": 103, "airline": "SpiceJet", "src": "Mumbai", "dest": "Bangalore", "dep": "08:00", "price": 3800, "dur": 105, "seats": 8},
    {"no": 104, "airline": "Vistara", "src": "Pune", "dest": "Bangalore", "dep": "09:45", "price": 4100, "dur": 90, "seats": 15},
    {"no": 105, "airline": "Akasa Air", "src": "Mumbai", "dest": "Delhi", "dep": "11:20", "price": 4900, "dur": 130, "seats": 20},
    {"no": 106, "airline": "IndiGo", "src": "Delhi", "dest": "Pune", "dep": "18:00", "price": 4700, "dur": 135, "seats": 7},
    {"no": 107, "airline": "Air India", "src": "Bangalore", "dest": "Pune", "dep": "19:15", "price": 4300, "dur": 95, "seats": 10},
    {"no": 108, "airline": "SpiceJet", "src": "Chennai", "dest": "Hyderabad", "dep": "07:30", "price": 2800, "dur": 75, "seats": 14},
    {"no": 109, "airline": "IndiGo", "src": "Hyderabad", "dest": "Chennai", "dep": "16:45", "price": 2950, "dur": 70, "seats": 0},  # Flight with 0 seats
    {"no": 110, "airline": "Vistara", "src": "Delhi", "dest": "Bangalore", "dep": "10:10", "price": 5800, "dur": 165, "seats": 18},
    {"no": 111, "airline": "Air India", "src": "Pune", "dest": "Hyderabad", "dep": "12:00", "price": 3200, "dur": 80, "seats": 9},
    {"no": 112, "airline": "IndiGo", "src": "Hyderabad", "dest": "Pune", "dep": "21:00", "price": 3400, "dur": 85, "seats": 16},
    {"no": 113, "airline": "Akasa Air", "src": "Bangalore", "dest": "Chennai", "dep": "13:40", "price": 2600, "dur": 60, "seats": 11},
    {"no": 114, "airline": "SpiceJet", "src": "Mumbai", "dest": "Hyderabad", "dep": "15:50", "price": 3100, "dur": 90, "seats": 6},
    {"no": 115, "airline": "Vistara", "src": "Delhi", "dest": "Mumbai", "dep": "17:25", "price": 5100, "dur": 135, "seats": 22}
]


# ==============================================================================
# PERSISTENCE (JSON LOAD & SAVE)
# ==============================================================================

def load_data(filepath=DATA_FILE):
    """
    Loads flights and bookings from the JSON file.
    If the file does not exist or is corrupted, initializes it with default flights.
    Ensures flights are always sorted by flight number.

    Time Complexity: O(N log N) where N is the number of flights (due to sorting by 'no').
    Space Complexity: O(N + M) where M is the number of bookings.
    """
    if not os.path.exists(filepath):
        # Create default dataset
        flights = [dict(f) for f in DEFAULT_FLIGHTS]
        flights = quick_sort(flights, key=lambda f: f["no"])
        data = {
            "flights": flights,
            "bookings": []
        }
        save_data(data, filepath)
        return data

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure flights are sorted by flight number
            flights = data.get("flights", [])
            flights = quick_sort(flights, key=lambda f: f["no"])
            data["flights"] = flights
            if "bookings" not in data:
                data["bookings"] = []
            return data
    except (json.JSONDecodeError, OSError):
        flights = [dict(f) for f in DEFAULT_FLIGHTS]
        flights = quick_sort(flights, key=lambda f: f["no"])
        data = {
            "flights": flights,
            "bookings": []
        }
        save_data(data, filepath)
        return data


def save_data(data, filepath=DATA_FILE):
    """
    Saves the flights and bookings dictionary to a JSON file.

    Time Complexity: O(N + M) where N is number of flights, M is bookings.
    Space Complexity: O(1) auxiliary.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ==============================================================================
# SEARCHING ALGORITHMS
# ==============================================================================

def linear_search_route(flights, src, dest):
    """
    Performs manual linear search to find all flights matching source and destination.
    Search is case-insensitive.

    Time Complexity:
        Best Case: O(N)
        Average Case: O(N)
        Worst Case: O(N)
        where N is the number of flights in the list.
    Space Complexity:
        O(k) where k is the number of matching flights returned in a new list.

    :param flights: List of flight dictionaries
    :param src: Source city string
    :param dest: Destination city string
    :return: List of matching flight dictionaries
    """
    results = []
    target_src = src.strip().lower()
    target_dest = dest.strip().lower()

    for flight in flights:
        if flight["src"].strip().lower() == target_src and flight["dest"].strip().lower() == target_dest:
            results.append(flight)
    return results


def binary_search_flight_no(flights, target_no):
    """
    Performs manual iterative binary search on flights list sorted by flight number.

    Time Complexity:
        Best Case: O(1) (target element at midpoint)
        Average Case: O(log N)
        Worst Case: O(log N)
        where N is the number of flights.
    Space Complexity:
        O(1) auxiliary space (iterative implementation).

    :param flights: List of flight dictionaries sorted by flight number ('no')
    :param target_no: Integer flight number to find
    :return: Index of the flight if found, else -1
    """
    low = 0
    high = len(flights) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = flights[mid]["no"]

        if mid_val == target_no:
            return mid
        elif mid_val < target_no:
            low = mid + 1
        else:
            high = mid - 1

    return -1


# ==============================================================================
# SORTING ALGORITHMS
# Each algorithm takes a list and a key function, and returns a NEW sorted list.
# Tracking comparison count is supported for performance analysis.
# ==============================================================================

def bubble_sort(flights, key=lambda x: x, count_comps=False):
    """
    Manual Bubble Sort with early-exit optimisation.
    Returns a new list sorted in ascending order by key.

    Time Complexity:
        Best Case: O(N) (when array is already sorted, early exit triggers)
        Average Case: O(N^2)
        Worst Case: O(N^2) (reverse sorted)
    Space Complexity:
        O(N) to store and return the new list (O(1) auxiliary space beyond the copy).

    :param flights: Input list of items
    :param key: Function to extract comparison key
    :param count_comps: Boolean flag to return (sorted_list, comparisons)
    :return: Sorted list, or tuple (sorted_list, comparison_count) if count_comps is True
    """
    arr = [item for item in flights]
    n = len(arr)
    comps = 0

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comps += 1
            if key(arr[j]) > key(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

    if count_comps:
        return arr, comps
    return arr


def selection_sort(flights, key=lambda x: x, count_comps=False):
    """
    Manual Selection Sort.
    Finds the minimum element from the unsorted subarray and places it at the beginning.
    Returns a new list sorted in ascending order by key.

    Time Complexity:
        Best Case: O(N^2)
        Average Case: O(N^2)
        Worst Case: O(N^2)
    Space Complexity:
        O(N) to store and return the new list (O(1) auxiliary space beyond the copy).

    :param flights: Input list of items
    :param key: Function to extract comparison key
    :param count_comps: Boolean flag to return (sorted_list, comparisons)
    :return: Sorted list, or tuple (sorted_list, comparison_count) if count_comps is True
    """
    arr = [item for item in flights]
    n = len(arr)
    comps = 0

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comps += 1
            if key(arr[j]) < key(arr[min_idx]):
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

    if count_comps:
        return arr, comps
    return arr


def insertion_sort(flights, key=lambda x: x, count_comps=False):
    """
    Manual Insertion Sort.
    Iteratively inserts elements into their correct position in the sorted sublist.
    Returns a new list sorted in ascending order by key.

    Time Complexity:
        Best Case: O(N) (array already sorted, 1 comparison per element)
        Average Case: O(N^2)
        Worst Case: O(N^2) (reverse sorted)
    Space Complexity:
        O(N) to store and return the new list (O(1) auxiliary space beyond the copy).

    :param flights: Input list of items
    :param key: Function to extract comparison key
    :param count_comps: Boolean flag to return (sorted_list, comparisons)
    :return: Sorted list, or tuple (sorted_list, comparison_count) if count_comps is True
    """
    arr = [item for item in flights]
    n = len(arr)
    comps = 0

    for i in range(1, n):
        current = arr[i]
        curr_key = key(current)
        j = i - 1
        while j >= 0:
            comps += 1
            if key(arr[j]) > curr_key:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = current

    if count_comps:
        return arr, comps
    return arr


def merge_sort(flights, key=lambda x: x, count_comps=False):
    """
    Manual Merge Sort (Divide and Conquer).
    Recursively divides the list into halves, sorts them, and merges back.
    Returns a new list sorted in ascending order by key.

    Time Complexity:
        Best Case: O(N log N)
        Average Case: O(N log N)
        Worst Case: O(N log N)
    Space Complexity:
        O(N) auxiliary space needed for sublists during merging.

    :param flights: Input list of items
    :param key: Function to extract comparison key
    :param count_comps: Boolean flag to return (sorted_list, comparisons)
    :return: Sorted list, or tuple (sorted_list, comparison_count) if count_comps is True
    """
    comps = [0]

    def _merge_sort_rec(arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = _merge_sort_rec(arr[:mid])
        right = _merge_sort_rec(arr[mid:])

        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comps[0] += 1
            if key(left[i]) <= key(right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        while i < len(left):
            merged.append(left[i])
            i += 1
        while j < len(right):
            merged.append(right[j])
            j += 1

        return merged

    result = _merge_sort_rec([item for item in flights])
    if count_comps:
        return result, comps[0]
    return result


def quick_sort(flights, key=lambda x: x, count_comps=False):
    """
    Manual Quick Sort (Divide and Conquer).
    Uses the middle element as pivot to mitigate worst-case on sorted data.
    Returns a new list sorted in ascending order by key.

    Time Complexity:
        Best Case: O(N log N)
        Average Case: O(N log N)
        Worst Case: O(N^2) (pathological pivot choice on skewed splits)
    Space Complexity:
        O(log N) auxiliary recursion stack space.

    :param flights: Input list of items
    :param key: Function to extract comparison key
    :param count_comps: Boolean flag to return (sorted_list, comparisons)
    :return: Sorted list, or tuple (sorted_list, comparison_count) if count_comps is True
    """
    comps = [0]

    def _quick_sort_rec(arr):
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]
        pivot_key = key(pivot)
        left = []
        equal = []
        right = []

        for item in arr:
            item_key = key(item)
            comps[0] += 1
            if item_key < pivot_key:
                left.append(item)
            elif item_key > pivot_key:
                right.append(item)
            else:
                equal.append(item)

        return _quick_sort_rec(left) + equal + _quick_sort_rec(right)

    result = _quick_sort_rec([item for item in flights])
    if count_comps:
        return result, comps[0]
    return result


# ==============================================================================
# RESERVATION MANAGEMENT (BUSINESS LOGIC)
# ==============================================================================

def book_ticket(data, flight_no, passenger_name, seat_count):
    """
    Books tickets for a passenger on a specified flight.
    - Searches for the flight using binary search.
    - Validates seat count (must be > 0 and <= available seats).
    - Reduces flight's available seats.
    - Generates booking ID starting from 1001.
    - Returns (True, booking_record, message) on success, or (False, None, error_message) on failure.

    Time Complexity: O(log N + M) where N is flights (binary search), M is bookings (ID lookup).
    Space Complexity: O(1) auxiliary.
    """
    flights = data["flights"]
    bookings = data["bookings"]

    idx = binary_search_flight_no(flights, flight_no)
    if idx == -1:
        return False, None, f"Flight {flight_no} not found."

    flight = flights[idx]

    if not isinstance(seat_count, int) or seat_count <= 0:
        return False, None, "Invalid seat count. Must be at least 1."

    if flight["seats"] == 0:
        return False, None, f"Booking rejected: Flight {flight_no} has 0 seats available (Sold Out)."

    if seat_count > flight["seats"]:
        return False, None, (
            f"Booking rejected: Requested {seat_count} seats, but only "
            f"{flight['seats']} seats are available on Flight {flight_no}."
        )

    # Seat allocation
    flight["seats"] -= seat_count

    # Determine next booking ID (starting from 1001)
    if not bookings:
        next_id = 1001
    else:
        max_id = max(b["id"] for b in bookings)
        next_id = max(1001, max_id + 1)

    booking = {
        "id": next_id,
        "name": passenger_name.strip(),
        "flight": flight_no,
        "seats": seat_count
    }
    bookings.append(booking)

    return True, booking, f"Booking successful! Booking ID: {next_id} for {seat_count} seat(s)."


def cancel_ticket(data, booking_id):
    """
    Cancels a booking by booking ID:
    - Locates the booking record.
    - Uses binary search to find the associated flight.
    - Restores the seats on that flight.
    - Removes the booking record.
    - Returns (True, message) on success, or (False, error_message) on failure.

    Time Complexity: O(M + log N) where M is bookings (linear search for ID), N is flights (binary search).
    Space Complexity: O(1) auxiliary.
    """
    bookings = data["bookings"]
    flights = data["flights"]

    target_idx = -1
    for i, b in enumerate(bookings):
        if b["id"] == booking_id:
            target_idx = i
            break

    if target_idx == -1:
        return False, f"Booking ID {booking_id} not found."

    booking = bookings.pop(target_idx)
    flight_no = booking["flight"]
    seats = booking["seats"]

    # Restore seats
    f_idx = binary_search_flight_no(flights, flight_no)
    if f_idx != -1:
        flights[f_idx]["seats"] += seats

    return True, f"Booking {booking_id} cancelled successfully! {seats} seat(s) restored to Flight {flight_no}."


# ==============================================================================
# PERFORMANCE COMPARISON UTILITY (FOR MENU 8)
# ==============================================================================

def compare_sort_performance(flights, key_func):
    """
    Runs all five sorting algorithms on the provided flights list with key_func.
    Measures execution time using time.perf_counter() and counts comparisons.

    Returns a list of dicts:
    [{'name': 'Bubble Sort', 'time': float, 'comps': int}, ...]
    """
    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Selection Sort", selection_sort),
        ("Insertion Sort", insertion_sort),
        ("Merge Sort", merge_sort),
        ("Quick Sort", quick_sort)
    ]

    results = []
    for name, sort_fn in algorithms:
        start_time = time.perf_counter()
        sorted_arr, comps = sort_fn(flights, key=key_func, count_comps=True)
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        results.append({
            "name": name,
            "time": elapsed,
            "comps": comps
        })

    return results


# ==============================================================================
# FORMATTING & CLI PRESENTATION
# ==============================================================================

def format_flights_table(flight_list):
    """
    Returns a neatly formatted string table of flights with box-drawing borders and clean alignment.
    """
    if not flight_list:
        return "No flights found matching the criteria."

    # Column specifications: (Header, Width, Alignment)
    cols = [
        ("No.",    5,  "^"),
        ("Airline",11, "<"),
        ("From",   10, "<"),
        ("To",     10, "<"),
        ("Dep",     6, "^"),
        ("Price",   8, ">"),
        ("Dur",     6, "^"),
        ("Seats",   6, "^")
    ]

    # Create border lines
    top_border    = "+" + "+".join(["-" * (w + 2) for _, w, _ in cols]) + "+"
    sep_border    = "+" + "+".join(["=" * (w + 2) for _, w, _ in cols]) + "+"
    bottom_border = "+" + "+".join(["-" * (w + 2) for _, w, _ in cols]) + "+"

    header_cells = [f" {h:{align}{w}} " for h, w, align in cols]
    header_line = "|" + "|".join(header_cells) + "|"

    lines = [top_border, header_line, sep_border]

    for f in flight_list:
        price_str = f"Rs{f['price']:,}" if isinstance(f['price'], (int, float)) else str(f['price'])
        dur_str = f"{f['dur']}m"
        seats_str = "FULL" if f['seats'] == 0 else str(f['seats'])

        cells = [
            f" {str(f['no']):^5} ",
            f" {str(f['airline']):<11} ",
            f" {str(f['src']):<10} ",
            f" {str(f['dest']):<10} ",
            f" {str(f['dep']):^6} ",
            f" {price_str:>8} ",
            f" {dur_str:^6} ",
            f" {seats_str:^6} "
        ]
        lines.append("|" + "|".join(cells) + "|")

    lines.append(bottom_border)
    return "\n".join(lines)


def format_bookings_table(booking_list):
    """
    Returns a neatly formatted string table of bookings with clean alignment and borders.
    """
    if not booking_list:
        return "No bookings found in system."

    cols = [
        ("Booking ID", 12, "^"),
        ("Passenger Name", 24, "<"),
        ("Flight No", 12, "^"),
        ("Seats Booked", 14, "^")
    ]

    top_border    = "+" + "+".join(["-" * (w + 2) for _, w, _ in cols]) + "+"
    sep_border    = "+" + "+".join(["=" * (w + 2) for _, w, _ in cols]) + "+"
    bottom_border = "+" + "+".join(["-" * (w + 2) for _, w, _ in cols]) + "+"

    header_cells = [f" {h:{align}{w}} " for h, w, align in cols]
    header_line = "|" + "|".join(header_cells) + "|"

    lines = [top_border, header_line, sep_border]

    for b in booking_list:
        cells = [
            f" {str(b['id']):^12} ",
            f" {str(b['name']):<24} ",
            f" {str(b['flight']):^12} ",
            f" {str(b['seats']):^14} "
        ]
        lines.append("|" + "|".join(cells) + "|")

    lines.append(bottom_border)
    return "\n".join(lines)


def print_menu():
    """Prints the console menu."""
    print("\n" + "=" * 50)
    print("      FLIGHT RESERVATION SYSTEM")
    print("      (Searching and Sorting Demonstration)")
    print("=" * 50)
    print("1. Show all flights")
    print("2. Search by route (Linear Search)")
    print("3. Search by flight number (Binary Search)")
    print("4. Sort flights (Choose key and algorithm)")
    print("5. Book ticket")
    print("6. Cancel ticket")
    print("7. View bookings")
    print("8. Compare sorting algorithm performance")
    print("0. Exit")
    print("=" * 50)


def main():
    """
    Main interactive driver program for the Flight Reservation System.
    """
    data = load_data()

    while True:
        print_menu()
        try:
            choice = input("Enter your choice (0-8): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting system. Goodbye!")
            break

        if choice == "1":
            print("\n--- ALL AVAILABLE FLIGHTS (Sorted by Flight No) ---")
            print(format_flights_table(data["flights"]))

        elif choice == "2":
            print("\n--- SEARCH FLIGHTS BY ROUTE (Linear Search) ---")
            try:
                src = input("Enter Source City: ").strip()
                dest = input("Enter Destination City: ").strip()
                results = linear_search_route(data["flights"], src, dest)
                if results:
                    print(f"\nFound {len(results)} flight(s) from {src} to {dest}:")
                    print(format_flights_table(results))
                else:
                    print(f"\nNo flights available from '{src}' to '{dest}'.")
            except Exception as e:
                print(f"Error during search: {e}")

        elif choice == "3":
            print("\n--- SEARCH FLIGHT BY NUMBER (Binary Search) ---")
            try:
                val = input("Enter Flight Number: ").strip()
                f_no = int(val)
                idx = binary_search_flight_no(data["flights"], f_no)
                if idx != -1:
                    print(f"\nFlight {f_no} found at index {idx}:")
                    print(format_flights_table([data["flights"][idx]]))
                else:
                    print(f"\nFlight {f_no} not found.")
            except ValueError:
                print("Invalid input! Please enter an integer flight number.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            print("\n--- SORT FLIGHTS ---")
            print("Select sorting attribute (key):")
            print("  1. Price")
            print("  2. Departure Time")
            print("  3. Duration")
            key_choice = input("Enter key choice (1-3): ").strip()

            key_dict = {
                "1": ("Price", lambda f: f["price"]),
                "2": ("Departure Time", lambda f: f["dep"]),
                "3": ("Duration", lambda f: f["dur"])
            }
            if key_choice not in key_dict:
                print("Invalid attribute selection.")
                continue

            attr_name, key_fn = key_dict[key_choice]

            print("\nSelect sorting algorithm:")
            print("  1. Bubble Sort (O(N^2), with early exit)")
            print("  2. Selection Sort (O(N^2))")
            print("  3. Insertion Sort (O(N^2))")
            print("  4. Merge Sort (O(N log N))")
            print("  5. Quick Sort (O(N log N))")
            algo_choice = input("Enter algorithm choice (1-5): ").strip()

            algo_dict = {
                "1": ("Bubble Sort", bubble_sort),
                "2": ("Selection Sort", selection_sort),
                "3": ("Insertion Sort", insertion_sort),
                "4": ("Merge Sort", merge_sort),
                "5": ("Quick Sort", quick_sort)
            }
            if algo_choice not in algo_dict:
                print("Invalid algorithm selection.")
                continue

            algo_name, algo_fn = algo_dict[algo_choice]

            sorted_flights = algo_fn(data["flights"], key=key_fn)
            print(f"\n--- FLIGHTS SORTED BY {attr_name.upper()} USING {algo_name.upper()} ---")
            print(format_flights_table(sorted_flights))

        elif choice == "5":
            print("\n--- BOOK TICKET ---")
            try:
                f_val = input("Enter Flight Number: ").strip()
                flight_no = int(f_val)
                name = input("Enter Passenger Name: ").strip()
                if not name:
                    print("Passenger name cannot be empty.")
                    continue
                s_val = input("Enter Number of Seats: ").strip()
                seat_count = int(s_val)

                success, booking, msg = book_ticket(data, flight_no, name, seat_count)
                if success:
                    save_data(data)
                    print(f"\nSUCCESS: {msg}")
                    print(format_bookings_table([booking]))
                else:
                    print(f"\nFAILURE: {msg}")
            except ValueError:
                print("Invalid numerical input. Please enter valid numbers for Flight Number and Seats.")
            except Exception as e:
                print(f"Error during booking: {e}")

        elif choice == "6":
            print("\n--- CANCEL TICKET ---")
            try:
                b_val = input("Enter Booking ID to cancel: ").strip()
                booking_id = int(b_val)
                success, msg = cancel_ticket(data, booking_id)
                if success:
                    save_data(data)
                    print(f"\nSUCCESS: {msg}")
                else:
                    print(f"\nFAILURE: {msg}")
            except ValueError:
                print("Invalid input! Please enter a valid integer Booking ID.")
            except Exception as e:
                print(f"Error during cancellation: {e}")

        elif choice == "7":
            print("\n--- ALL BOOKINGS ---")
            print(format_bookings_table(data["bookings"]))

        elif choice == "8":
            print("\n--- SORTING ALGORITHM PERFORMANCE COMPARISON (CURRENT DATASET) ---")
            print("Sorting key: Ticket Price (Rs)\n")
            perf = compare_sort_performance(data["flights"], key_func=lambda f: f["price"])
            p_cols = [
                ("Algorithm", 18, "<"),
                ("Time Taken (sec)", 20, ">"),
                ("Comparisons", 14, "^")
            ]
            top_b = "+" + "+".join(["-" * (w + 2) for _, w, _ in p_cols]) + "+"
            sep_b = "+" + "+".join(["=" * (w + 2) for _, w, _ in p_cols]) + "+"
            bot_b = "+" + "+".join(["-" * (w + 2) for _, w, _ in p_cols]) + "+"

            print(top_b)
            print("|" + "|".join([f" {h:{a}{w}} " for h, w, a in p_cols]) + "|")
            print(sep_b)
            for item in perf:
                time_str = f"{item['time']:.8f} s"
                print(f"| {item['name']:<18} | {time_str:>20} | {str(item['comps']):^14} |")
            print(bot_b)

        elif choice == "0":
            print("\nExiting Flight Reservation System. Have a safe journey!")
            break

        else:
            print("Invalid choice! Please select an option from 0 to 8.")


if __name__ == "__main__":
    main()
