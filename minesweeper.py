import itertools
import random


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
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else: 
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if(cell in self.cells):
            self.count -= 1
            self.cells.remove(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if(cell in self.cells):
            self.cells.remove(cell)


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
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

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
        # mark the cell as a move that has been made
        self.moves_made.add(cell)

        # mark the cell as safe
        self.mark_safe(cell)

        # add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        # if my cell has know_mines around then adjust cells
        all_cells_around = [(i,j) for i in range(cell[0]-1, cell[0]+2) for j in range(cell[1]-1, cell[1]+2)]
        adjusted_cells = set()
        adjusted_count = count

        for neighbor in all_cells_around:
            if neighbor == cell or neighbor[0] < 0 or neighbor[0] >= self.height or neighbor[1] < 0 or neighbor[1] >= self.height:
                continue
            elif neighbor in self.mines:
                adjusted_count -= 1
            elif neighbor not in self.moves_made and neighbor not in self.mines and neighbor not in self.safes:
                adjusted_cells.add(neighbor) #just list of possible mines


        # add knowledge
        if adjusted_cells:
            self.knowledge.append(Sentence(adjusted_cells, adjusted_count))
            print(f"added sentence: cells: {adjusted_cells} count: {adjusted_count}")            

        # mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        repeat = True

        while(repeat):
            repeat = False

            adjusted_mines = set()
            adjusted_safes = set()

            for sentence in self.knowledge:
                if sentence.known_mines():
                    adjusted_mines.update(sentence.known_mines())
                if sentence.known_safes():
                    adjusted_safes.update(sentence.known_safes())

            for mine in adjusted_mines:
                if mine not in self.mines:
                    self.mark_mine(mine)
                    repeat = True

            for safe in adjusted_safes:
                if safe not in self.safes:
                    self.mark_safe(safe)
                    repeat = True

            #infer new knowledge based on existing one
            #iterate over all sentences
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1 == sentence2:
                        continue
                    
                    cells1 = sentence1.cells
                    cells2 = sentence2.cells
                    if len(cells1) > 0 and len(cells2) > 0 and cells1.issubset(cells2):
                        sentence2.cells = cells2 - cells1
                        count1 = sentence1.count
                        count2 = sentence2.count
                        sentence2.count = count2 - count1
                        repeat = True
                        print(f"updated sentence: old cells: {cells2} new cells: {sentence2.cells} old count: {count2} new count: {sentence2.count}")


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if self.safes:
            for move in self.safes:
                if move not in self.moves_made:
                    return move
        else: 
            return None
        

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        #get all cells
        possible_moves = [(i,j) for i in range(self.height) for j in range(self.width)]

        #subtract maden moves
        possible_moves = [cell for cell in possible_moves if cell not in self.moves_made]

        #subtract known_mines
        possible_moves = [cell for cell in possible_moves if cell not in self.mines]

        if possible_moves:
            return random.choice(possible_moves)
        else:
            return None
