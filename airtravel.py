class Flight:

    def __init__(self, number, aircraft):
        if not number[:2].isalpha:
            raise ValueError("No airline code in '{}'".format(number))

        if not number[:2].isupper():
            raise ValueError("Invalid airline code '{}'".format(number))

        if not (number[2:].isdigit() and int(number[2:]) <= 9999):
            raise ValueError("Invalid route number '{}'".format(number))

        self._number = number
        self._aircraft = aircraft

        rows, seats = self._aircraft.seating_plan()
        self._seating = [None] + [ {letter: None for letter in seats} for _ in rows ]

    def number(self):
        return self._number

    def airline(self):
        return self._number[:2]

    def aircraft_model(self):
        return self._aircraft.model()

    def _parse_seat(self, seat):
        row_numbers, seat_letters = self._aircraft.seating_plan()
        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError("Invalid seat letter {}".format(letter))
        row_text = seat[:-1]
        try:
            row = int(row_text)
        except ValueError:
            raise ValueError("Invalid row number {}".format(row))
        return row, letter

    def allocate_seat(self, seat, passenger):
        row, letter = self._parse_seat(seat)
        if self._seating[row][letter] is not None:
            raise ValueError("Seat {} already occupied".format(seat))
        self._seating[row][letter] = passenger

    def relocate_passenger(self, from_seat, to_seat):
        from_row, from_letter = self._parse_seat(from_seat)
        if self._seating[from_row][from_letter] is None:
            raise ValueError("No Passenger to relocate in seat {}".format(from_seat))
        to_row, to_letter = self._parse_seat(to_seat)
        if self._seating[to_row][to_letter] is not None:
            raise ValueError("Seat {} already occupied".format(to_seat))
        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    def num_available_seats(self):
        return sum(sum(1 for s in row.values() if s is None) for row in self._seating if row is not None)

    def make_boarding_cards(self, card_printer):
        for passenger, seat in sorted(self._passenger_seats()):
            card_printer(passenger, seat, self.number(), self.aircraft_model())

    def _passenger_seats(self):
        row_numbers, seat_letters = self._aircraft.seating_plan()
        for row in row_numbers:
            for letter in seat_letters:
                passenger = self._seating[row][letter]
                if passenger is not None:
                    yield (passenger, "{}{}".format(row, letter))


class Aircraft:
    def num_seats(self):
        rows, row_seats = self.seating_plan()
        return len(rows) * len(row_seats)

    def __init__(self, registration):
        self._registration = registration

    def registration(self):
        return self._registration


class AirbusA319(Aircraft):
    def model(self):
        return "Airbus A319"

    def seating_plan(self):
        return range(1, 15), "ABCDEF"


class Boeing777(Aircraft):
    def model(self):
        return "Boeing 777"

    def seating_plan(self):
        return range(1, 10), "ABCDE"


def make_flights():
    f = Flight("AI900", AirbusA319("G_UP"))
    f.allocate_seat('1B', 'Juan')
    f.allocate_seat('3B', 'xuan')
    f.allocate_seat('4B', 'guan')
    f.allocate_seat('2A', 'huan')
    g = Flight("BO900", Boeing777("G_UP"))
    g.allocate_seat('1B', 'Juan')
    g.allocate_seat('3B', 'xuan')
    g.allocate_seat('4B', 'guan')
    g.allocate_seat('2A', 'huan')
    return f, g


def console_card_printer(passenger, seat, flight_number, aircraft):
    output = "|Name: {0}"\
             " Flight: {1}"\
             " Seat: {2}"\
             " Aircraft: {3}"\
             " |".format(passenger, flight_number, seat, aircraft)
    banner = '+' + '-' * (len(output) - 2) + '+'
    border = '|' + ' ' * (len(output) - 2) + '|'
    lines = [banner, border, output, border, banner]
    card = '\n'.join(lines)
    print(card)
    print()