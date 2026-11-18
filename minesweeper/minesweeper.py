
import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        self.height = height
        self.width = width
        self.mines = set()

        # Create an empty board
        self.board = []

        for i in range(self.height):
            row = []

            for j in range(self.width):
                row.append(False)

            self.board.append(row)

        # Randomly place mines on the board
        while len(self.mines) != mines:

            i = random.randrange(height)
            j = random.randrange(width)

            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        self.mines_found = set()

    def print(self):
        """
        Prints the board with mines visible.
        """

        print()

        for i in range(self.height):
            print("--" * self.width + "-")

            for j in range(self.width):

                if self.board[i][j]:
                    print("|X", end="")

                else:
                    print("| ", end="")

            print("|")

        print("--" * self.width + "-")

    def is_mine(self, cell):
        """
        Returns True if the cell contains a mine.
        """

        row, col = cell

        return self.board[row][col]

    def nearby_mines(self, cell):
        """
        Returns the number of mines surrounding a cell.
        """

        count = 0

        row, col = cell

        for i in range(max(0, row - 1), min(self.height, row + 2)):
            for j in range(max(0, col - 1), min(self.width, col + 2)):

                if (i, j) == cell:
                    continue

                if self.board[i][j]:
                    count += 1

        return count

    def won(self):
        """
        Checks whether all mines have been found.
        """

        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game.
    """

    def __init__(self, cells, count):

        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):

        return self.cells == other.cells and self.count == other.count

    def __str__(self):

        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns cells that must be mines.
        """

        if self.count == len(self.cells):
            return self.cells.copy()

        return set()

    def known_safes(self):
        """
        Returns cells that must be safe.
        """

        if self.count == 0:
            return self.cells.copy()

        return set()

    def mark_mine(self, cell):
        """
        Updates the sentence when a cell is known to be a mine.
        """

        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates the sentence when a cell is known to be safe.
        """

        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    AI that plays Minesweeper using logical knowledge.
    """

    def __init__(self, height=8, width=8):

        self.height = height
        self.width = width

        self.moves_made = set()
        self.mines = set()
        self.safes = set()

        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine and updates knowledge.
        """

        self.mines.add(cell)

        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe and updates knowledge.
        """

        self.safes.add(cell)

        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Adds new information to the AI's knowledge base.
        """

        # 1. Record the move and mark the cell as safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # 2. Find all neighbouring cells
        neighbors = set()

        row, col = cell

        for i in range(max(0, row - 1), min(self.height, row + 2)):
            for j in range(max(0, col - 1), min(self.width, col + 2)):

                if (i, j) == cell:
                    continue

                neighbors.add((i, j))

        # 3. Remove cells already known to be mines or safe
        new_cells = set()
        new_count = count

        for neighbor in neighbors:

            if neighbor in self.mines:
                new_count -= 1

            elif neighbor in self.safes:
                continue

            else:
                new_cells.add(neighbor)

        # 4. Add the new sentence to the knowledge base
        if new_cells:
            self.knowledge.append(Sentence(new_cells, new_count))

        # 5. Keep making deductions until no new information is found
        changed = True

        while changed:

            changed = False

            safes = set()
            mines = set()

            for sentence in self.knowledge:
                safes.update(sentence.known_safes())
                mines.update(sentence.known_mines())

            for safe in safes - self.safes:
                self.mark_safe(safe)
                changed = True

            for mine in mines - self.mines:
                self.mark_mine(mine)
                changed = True

            # 6. Use subset inference to create new sentences
            new_sentences = []

            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:

                    if sentence1 == sentence2:
                        continue

                    if sentence1.cells and sentence1.cells.issubset(sentence2.cells):

                        difference = sentence2.cells - sentence1.cells
                        count_difference = sentence2.count - sentence1.count

                        new_sentence = Sentence(difference, count_difference)

                        if (
                            difference
                            and new_sentence not in self.knowledge
                            and new_sentence not in new_sentences
                        ):
                            new_sentences.append(new_sentence)

            if new_sentences:
                self.knowledge.extend(new_sentences)
                changed = True

            # 7. Remove empty sentences
            self.knowledge = [
                sentence for sentence in self.knowledge
                if sentence.cells
            ]

    def make_safe_move(self):
        """
        Returns a safe move that has not already been made.
        """

        for cell in self.safes:

            if cell not in self.moves_made:
                return cell

        return None

    def make_random_move(self):
        """
        Returns a random move that is not already made
        and is not known to be a mine.
        """

        choices = set()

        for i in range(self.height):
            for j in range(self.width):

                cell = (i, j)

                if cell not in self.moves_made and cell not in self.mines:
                    choices.add(cell)

        if not choices:
            return None

        return random.choice(list(choices))

