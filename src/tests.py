import unittest

class KingTestCase(unittest.TestCase):
    def set_up(self):
        self.king1 = King([5,5], "White")
        self.king2 = King([5,5], "Black")

    def test_calculation_of_possible_moves(self):
        test_data = [
            [[6, 6], [6, 4], [6, 5], [4, 6], [4, 4], [4, 5], [5, 6], [5, 4]]
            ]
        
