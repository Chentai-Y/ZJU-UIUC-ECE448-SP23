import numpy as np

def solve(board, tiles):
    # Convert board to numpy array for easier manipulation
    board = np.array(board)

    # Define functions to rotate and flip tiles
    def rotate(tile):
        return np.rot90(tile)

    def flip(tile):
        return np.fliplr(tile)

    # Define function to check if a tile fits on the board at a given position
    def check_tile(tile, pos):
        if np.any(pos < 0) or np.any(pos + np.shape(tile) > np.shape(board)):
            return False
        if np.any(np.logical_and(tile, board[pos[0]:pos[0]+np.shape(tile)[0], pos[1]:pos[1]+np.shape(tile)[1]])):
            return False
        return True

    # Define function to place a tile on the board at a given position
    def place_tile(tile, pos):
        board[pos[0]:pos[0]+np.shape(tile)[0], pos[1]:pos[1]+np.shape(tile)[1]] += tile

    # Define recursive function to solve the board
    def solve_recursive():
        # Find first empty cell on board
        pos = np.argwhere(board == 0)
        if len(pos) == 0:
            return True

        # Try each tile in each possible orientation and position
        for tile in tiles:
            for rotation in range(4):
                for flip in range(2):
                    rotated_tile = tile
                    for i in range(rotation):
                        rotated_tile = rotate(rotated_tile)
                    if flip:
                        rotated_tile = flip(rotated_tile)

                    if check_tile(rotated_tile, pos[0]):
                        place_tile(rotated_tile, pos[0])
                        if solve_recursive():
                            return True
                        place_tile(-rotated_tile, pos[0])

        # No solution found
        return False

    # Call recursive function to solve the board
    solve_recursive()

    # Return solution as list of lists
    return board.tolist()
