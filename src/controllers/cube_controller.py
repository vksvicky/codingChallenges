class CubeController:
    def __init__(self, window, cube):
        self.window = window
        self.cube = cube

    def make_move(self, move):
        self.cube.make_move(move)

    def scramble(self):
        self.cube.scramble()

    def solve(self):
        self.cube.solve()

    def stop_solving(self):
        self.cube.stop_solving()

    def resume_solving(self):
        self.cube.resume_solving()

    def change_size(self, size):
        self.cube.change_size(size)