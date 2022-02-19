import unittest
from oracle import options

class TestMain(unittest.TestCase):
    def test_dieable_ok_exact(self):
        movies = ['exactly', 'six', 'movies', 'in', 'this', 'list']
        assert options.dieable(movies, 6) == movies

    def test_dieable_ok_less_than(self):
        assert options.dieable(['1', '2', '3', '4', '5'], 6) == ['1', '2', '3', '4', '5', '1']
        assert options.dieable(['1', '2', '3', '4'], 6) == ['1', '2', '3', '4', '1', '2']
        assert options.dieable(['1', '2', '3'], 6) == ['1', '2', '3', '1', '2', '3']
        assert options.dieable(['1', '2'], 6) == ['1', '2', '1', '2', '1', '2']
        assert options.dieable(['1'], 6) == ['1', '1', '1', '1', '1', '1']

    def test_dieable_ok_more_than(self):
        movies = ['more', 'than', 'six', 'movies', 'in', 'this', 'list']
        assert options.dieable(movies, 6) == ['more', 'than', 'six', 'movies', 'in', 'this']

if __name__ == '__main__':
    unittest.main()
