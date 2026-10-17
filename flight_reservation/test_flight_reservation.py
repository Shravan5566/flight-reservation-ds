"""
Unit Tests for Flight Reservation System
SPPU 2024 Pattern, PCC-204-COM: Data Structures Laboratory

Tests all 10 required test cases:
1. Search Pune -> Delhi returns flights 101 and 102
2. Search Pune -> Goa returns an empty list
3. Binary search 104 returns that flight
4. Binary search 999 returns -1
5. Each sort by price gives ascending prices and matches Python's sorted() result
6. Booking 2 seats on flight 101 reduces seats from 5 to 3
7. Booking more seats than available is rejected
8. Booking on a 0-seat flight is rejected
9. Cancelling a valid booking restores the seats
10. Cancelling a non-existent ID (5555) returns not found
"""

import unittest
from flight_reservation import (
    DEFAULT_FLIGHTS,
    linear_search_route,
    binary_search_flight_no,
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    book_ticket,
    cancel_ticket
)


class TestFlightReservationSystem(unittest.TestCase):
    def setUp(self):
        """Set up fresh test data before every test."""
        # Deep copy default flights
        self.flights = [dict(f) for f in DEFAULT_FLIGHTS]
        # Ensure flights are sorted by 'no' as required by binary search
        self.flights.sort(key=lambda x: x["no"])
        self.data = {
            "flights": self.flights,
            "bookings": []
        }

    # Case 1: Search Pune -> Delhi returns flights 101 and 102
    def test_01_search_pune_to_delhi(self):
        results = linear_search_route(self.data["flights"], "Pune", "Delhi")
        flight_nos = [f["no"] for f in results]
        self.assertEqual(len(results), 2)
        self.assertIn(101, flight_nos)
        self.assertIn(102, flight_nos)

    # Case 2: Search Pune -> Goa returns an empty list
    def test_02_search_pune_to_goa_empty(self):
        results = linear_search_route(self.data["flights"], "Pune", "Goa")
        self.assertEqual(results, [])

    # Case 3: Binary search 104 returns that flight
    def test_03_binary_search_found(self):
        idx = binary_search_flight_no(self.data["flights"], 104)
        self.assertNotEqual(idx, -1)
        flight = self.data["flights"][idx]
        self.assertEqual(flight["no"], 104)
        self.assertEqual(flight["airline"], "Vistara")
        self.assertEqual(flight["src"], "Pune")
        self.assertEqual(flight["dest"], "Bangalore")

    # Case 4: Binary search 999 returns -1
    def test_04_binary_search_not_found(self):
        idx = binary_search_flight_no(self.data["flights"], 999)
        self.assertEqual(idx, -1)

    # Case 5: Each sort by price gives ascending prices and matches Python's sorted() result
    def test_05_all_sorting_algorithms_match_sorted(self):
        price_key = lambda f: f["price"]
        expected_prices = [f["price"] for f in sorted(self.data["flights"], key=price_key)]

        sorting_algorithms = [
            ("Bubble Sort", bubble_sort),
            ("Selection Sort", selection_sort),
            ("Insertion Sort", insertion_sort),
            ("Merge Sort", merge_sort),
            ("Quick Sort", quick_sort)
        ]

        for name, sort_fn in sorting_algorithms:
            with self.subTest(algorithm=name):
                sorted_result = sort_fn(self.data["flights"], key=price_key)
                actual_prices = [f["price"] for f in sorted_result]
                # Check ascending order
                self.assertEqual(actual_prices, expected_prices, f"{name} did not match expected sorted order")
                # Ensure input array was not modified in-place unexpectedly
                self.assertEqual(len(sorted_result), len(self.data["flights"]))

    # Case 6: Booking 2 seats on flight 101 reduces seats from 5 to 3
    def test_06_booking_seats_reduction(self):
        f_idx = binary_search_flight_no(self.data["flights"], 101)
        initial_seats = self.data["flights"][f_idx]["seats"]
        self.assertEqual(initial_seats, 5)

        success, booking, msg = book_ticket(self.data, 101, "Aarav Sharma", 2)
        self.assertTrue(success)
        self.assertIsNotNone(booking)
        self.assertEqual(booking["flight"], 101)
        self.assertEqual(booking["seats"], 2)
        self.assertEqual(booking["id"], 1001)

        updated_seats = self.data["flights"][f_idx]["seats"]
        self.assertEqual(updated_seats, 3)

    # Case 7: Booking more seats than available is rejected
    def test_07_booking_more_seats_than_available(self):
        f_idx = binary_search_flight_no(self.data["flights"], 101)
        available_seats = self.data["flights"][f_idx]["seats"]  # 5

        success, booking, msg = book_ticket(self.data, 101, "Pooja Patil", available_seats + 1)
        self.assertFalse(success)
        self.assertIsNone(booking)
        self.assertIn("rejected", msg.lower())
        # Verify seats were untouched
        self.assertEqual(self.data["flights"][f_idx]["seats"], available_seats)

    # Case 8: Booking on a 0-seat flight is rejected
    def test_08_booking_zero_seat_flight(self):
        # Flight 109 has 0 seats in default dataset
        f_idx = binary_search_flight_no(self.data["flights"], 109)
        self.assertEqual(self.data["flights"][f_idx]["seats"], 0)

        success, booking, msg = book_ticket(self.data, 109, "Rohan Kulkarni", 1)
        self.assertFalse(success)
        self.assertIsNone(booking)
        self.assertIn("rejected", msg.lower())
        self.assertEqual(self.data["flights"][f_idx]["seats"], 0)

    # Case 9: Cancelling a valid booking restores the seats
    def test_09_cancel_booking_restores_seats(self):
        # First book 3 seats on flight 102 (starts with 12 seats)
        f_idx = binary_search_flight_no(self.data["flights"], 102)
        orig_seats = self.data["flights"][f_idx]["seats"]

        success, booking, _ = book_ticket(self.data, 102, "Sneha Joshi", 3)
        self.assertTrue(success)
        self.assertEqual(self.data["flights"][f_idx]["seats"], orig_seats - 3)
        b_id = booking["id"]

        # Now cancel the booking
        cancel_success, cancel_msg = cancel_ticket(self.data, b_id)
        self.assertTrue(cancel_success)
        self.assertIn("cancelled successfully", cancel_msg.lower())
        # Check seats restored
        self.assertEqual(self.data["flights"][f_idx]["seats"], orig_seats)
        # Check booking removed from list
        self.assertEqual(len(self.data["bookings"]), 0)

    # Case 10: Cancelling a non-existent ID (5555) returns not found
    def test_10_cancel_non_existent_booking(self):
        cancel_success, cancel_msg = cancel_ticket(self.data, 5555)
        self.assertFalse(cancel_success)
        self.assertIn("not found", cancel_msg.lower())


if __name__ == "__main__":
    unittest.main()
