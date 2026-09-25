
import random


def set_column_sizes():
    """
    for each column, no more than 3 numbers, 15 numbers in whole card, 9 columns
    @return:
    """


    column_sizes  = [1] * 9  # 9 columns start with 1 number, no column can be empty
    extra = 6  # 6 numbers to distribute because there are 15 numbers, 3 rows of 5

    while extra > 0:
        col = random.randrange(9)
        if column_sizes[col] < 3:
                column_sizes[col] += 1
                extra -= 1
    return column_sizes


def set_rows(sizes):
    """
    for each row (3 rows), 5 numbers must be there
    @param sizes: column sizes
    @return:
    """
    iteration = 0
    while True:

        rows_per_column = [random.sample(range(3), size) for size in sizes]

        row_counts = [0, 0, 0]
        for rows in rows_per_column:
            for row in rows:
                row_counts[row] += 1

        iteration += 1

        if row_counts == [ 5, 5, 5]:
            #if iteration > 15:
                # print(f'Found a solution after {iteration} iterations!')
            return rows_per_column

class Card:
    def __init__(self):
        column_ranges = [(1, 9), (10, 19), (20, 29), (30, 39), (40, 49),
                         (50, 59), (60, 69), (70, 79), (80, 90)]

        sizes = set_column_sizes()
        rows_per_column = set_rows(sizes)

        card = [[0] * 9 for _ in range(3)]  # 3 rows of 9 zeros

        for col in range(9):
            low, high = column_ranges[col]  # check limits for each col
            numbers = sorted(random.sample(range(low, high + 1), sizes[col]))  # random numbers to put in the column
            rows = sorted(rows_per_column[col])
            for number, row in zip(numbers, rows):
                card[row][col] = number

        self.numbers = card
        self.marks = [[0]*9 for _ in range(3)]

    def __str__(self):
        lines = []
        for row in self.numbers:
            lines.append(" ".join(f"{n:2d}" if n else " ." for n in row))
        return "\n".join(lines)

    def __eq__(self, other):
        return self.numbers == other.numbers

    def mark(self, number):
        for i in range(3):
            for j in range(9):
                if self.numbers[i][j] == number:
                    self.marks[i][j] = 1

    def has_line(self):
        for row in self.marks:
            if sum(row) == 5:
                return True
        return False

    def is_bingo(self):
        return sum(sum(row) for row in self.marks) == 15

    def numbers_left(self):
        return 15 - sum(sum(row) for row in self.marks)


def draw_number(remaining):
    number = random.choice(remaining)
    remaining.remove(number)

    return number



def print_card(card):
    for row in card:
        print(" ".join(f"{n:2d}" if n else " ." for n in row))



def check_cards(number_drawn, cards, written_cards):
    for n, card in enumerate(cards):
        written_card = written_cards[n]
        for i in range(3):  # row
            for j in range(9):  # col
                if number_drawn == card[i][j]:
                    written_card[i][j] = 1

    return written_cards


def check_lines(cards, written_cards):
    winner_list = []
    for n, written_card in enumerate(written_cards):
        for row in written_card:
            if sum(row) == 5:
                print(f'Line!')
                print(f'Line Winner is card {n}!')
                print_card(cards[n])
                print(f'---------')
                print_card(written_cards[n])
                winner_list.append(cards[n])
                break

    return winner_list


def check_bingo(cards, written_cards):
    winner_list = []
    for n, written_card in enumerate(written_cards):
        total_sum = sum(sum(row) for row in written_card)
        if total_sum == 15:

            print(f'Bingo!')
            print(f'Bingo Winner is card {n}!')
            print_card(cards[n])
            print(f'---------')
            print_card(written_cards[n])
            winner_list.append(cards[n])

    return winner_list


def bingo_game(cards_number):

    cards = []
    while len(cards) < cards_number:
        card = Card()
        if card not in cards:
            cards.append(card)

    for card in cards:
        print(card)
        print("-----")

    remaining = list(range(1,91))
    drawn = set()

    print(f'Game starting...\n')

    winner_line, winner_bingo = False, False

    while not winner_bingo:
        number = draw_number(remaining)
        drawn.add(number)
        print(f'Number {number} drawn\n')

        for card in cards:
            card.mark(number)  # mark the number on the card

            if not winner_line:
                winner_line = card.has_line()
                if winner_line:
                    line_draw = len(drawn)

            else:
                winner_bingo = card.is_bingo()
                if winner_bingo:
                    bingo_draw = len(drawn)
                    break

    print(f'\nGame ended!')
    print(f'Line complete at draw {line_draw}!')

    print(f'Bingo complete at draw {bingo_draw}!')
    print(f'All Numbers drawn: {drawn}')


    return line_draw, bingo_draw, winner_line, winner_bingo





bingo_game(2)
