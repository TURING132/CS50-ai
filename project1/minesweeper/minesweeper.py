import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
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
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
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
        Returns the set of all cells in self.cells known to be mines.
        How to confirm a cell is mine?
            1. count == number fo cells
            2. count == 0
        """
        mines_set = set()
        if len(self.cells) == self.count:
            mines_set = self.cells.copy()
        return mines_set  # if count == 0, just return empty set

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        How to confirm a cell is safe?
            1. count == 0
            2. count == number of cells
        """
        safe_set = set()
        if self.count == 0:
            safe_set = self.cells.copy()
        return safe_set  # if count == number of cells, just return emptu set

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # for c in self.cells:
        #     if c == cell:
        #         self.cells.remove(cell)
        #         self.count -= 1
        #         break
        new_cells = self.cells.copy()
        new_cells.remove(cell)
        self.cells = new_cells
        self.count -= 1

    def mark_safe(self, cell):
        """
            Updates internal knowledge representation given the fact that
            a cell is known to be safe.
            """
        new_cells = self.cells.copy()
        new_cells.remove(cell)
        self.cells = new_cells


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.mark_safe(cell)

    def infer(self):
        """
        infer new sentence by sub
        """
        updated = False
        old_knowledge = copy.deepcopy(self.knowledge)
        for x in old_knowledge:
            for y in old_knowledge:
                # setx - sety = countx - county
                if x != y and y.cells.issubset(x.cells):
                    new_cells = x.cells - y.cells
                    new_count = x.count - y.count
                    new_sentence = Sentence(new_cells, new_count)
                    if new_sentence not in old_knowledge:
                        self.knowledge.append(new_sentence)
                        updated = True
        if updated:
            self.infer()

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        x, y = cell[0], cell[1]
        neighbors = (
            (x - 1, y), (x + 1, y),
            (x, y - 1), (x, y + 1),
            (x - 1, y - 1), (x - 1, y + 1),
            (x + 1, y - 1), (x + 1, y + 1)
        )
        # only include cells whose state is still undetermined in the sentence.
        for n in neighbors:
            if n in self.mines:
                count -= 1
        valid_neighbors = ((i, j) for i, j in neighbors if 0 <= i < self.width and 0 <= j < self.width
                           and (i, j) not in self.moves_made and (i, j) not in self.safes and (i, j) not in self.mines)
        self.knowledge.append(Sentence(valid_neighbors, count))

        # infer new sentence
        self.infer()

        # mark new known cells
        for sentence in self.knowledge:
            if sentence.count == 0:
                for c in sentence.cells:
                    self.mark_safe(c)
            if sentence.count == len(sentence.cells):
                for c in sentence.cells:
                    self.mark_mine(c)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for m in self.safes:
            if m not in self.moves_made:
                return m
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        if len(self.moves_made) + len(self.mines) == self.height * self.width:
            return None  # not possible move

        move = (random.randrange(self.height), random.randrange(self.width))
        while move in self.moves_made or move in self.mines:
            move = (random.randrange(self.height), random.randrange(self.width))

        return move
