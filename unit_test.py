""" This file tests various functions utilized in the project """
import unittest
import unittest.mock as mock
from unittest.mock import patch
from get_movie import get_genres, get_similar, get_upcoming, search
from routes import filter_watchlist


class TestStringMethods(unittest.TestCase):
    """
    Tests for api calls
    """

    def test_save_actor(self):
        """
        GIVEN an actor name
        WHEN a User attempts to save a movie to their list
        THEN check movie is added to list
        """
        user_input = "Russell Brand"
        filters = {
            "genre_filter": "",
            "year_filter": None,
            "year_before_after": False,
            "rating_filter": None,
            "rating_before_after": False,
        }
        api_results = search(user_input, filters)
        self.assertIsNotNone(api_results)
        movie_titles_list = []
        for movie in api_results:
            movie_titles_list.append(movie["movie_title"])
        self.assertIsNotNone(movie_titles_list)
        self.assertIn("Despicable Me", movie_titles_list)

    def test_save_text(self):
        """
        GIVEN a string or blank
        WHEN a User attempts to add a movie to their list
        THEN check valid movie is added to list or exception thrown if blank
        """
        user_input = ""
        filters = {
            "genre_filter": "",
            "year_filter": None,
            "year_before_after": False,
            "rating_filter": None,
            "rating_before_after": False,
        }
        movie_text = search(user_input, filters)
        self.assertRaises(Exception, search)
        self.assertIsNone(movie_text)

        user_input = "Rush Hour"
        movie_text = search(user_input, filters)
        movie_titles = []
        for movie in movie_text:
            movie_titles.append(movie["movie_title"])
        self.assertIn("Rush Hour", movie_titles)

    def test_search(self):
        """
        GIVEN a movie title
        WHEN a User attempts Search
        THEN check valid Search results
        """
        user_input = "Rush Hour"
        filters = {
            "genre_filter": "",
            "year_filter": None,
            "year_before_after": False,
            "rating_filter": None,
            "rating_before_after": False,
        }
        result = search(user_input, filters)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)

    def test_get_movie_details(self):
        """
        GIVEN a movie title
        WHEN a movie details are requested
        THEN check valid results
        """
        movie_id = 2109
        api_results = get_genres(movie_id)
        self.assertIsNotNone(api_results)
        self.assertIn("Comedy", api_results)

    def test_get_upcoming(self):
        """
        WHEN a request is made to get upcoming movies
        THEN check valid results are returned
        """
        api_results = get_upcoming()
        self.assertIsNotNone(api_results)
        self.assertNotIn("ValueError", api_results)

    def test_get_similar(self):
        """
        GIVEN a movieID
        WHEN a User attempts to get similar movies
        THEN check valid results are returned or exception thrown
        """
        api_results = get_similar("2109")
        self.assertIsNotNone(api_results)
        self.assertNotIn("ValueError", api_results)


class MockedTesting(unittest.TestCase):
    def test_filter_watchlist(self):
        """
        GIVEN a userid and a set of results
        WHEN a User performs a search
        THEN check if the movies on a user's watchlist matches the results
        """

        def mock_on_watchlist(l):
            sample_list = [120467]
            return sample_list

        expected_results = [
            {
                "movie_id": 120467,
                "movie_title": "The Grand Budapest Hotel",
                "movie_image": "https://image.tmdb.org/t/p/original/eWdyYQreja6JGCzqHWXpWHDrrPo.jpg",
                "genres": ["Comedy", "Drama"],
                "release_date": "2014-02-26",
                "rating": 8,
                "on_watchlist": True,
            }
        ]

        user_id = "116405330661820156295"
        results = [
            {
                "movie_id": 120467,
                "movie_title": "The Grand Budapest Hotel",
                "movie_image": "https://image.tmdb.org/t/p/original/eWdyYQreja6JGCzqHWXpWHDrrPo.jpg",
                "genres": ["Comedy", "Drama"],
                "release_date": "2014-02-26",
                "rating": 8,
                "on_watchlist": False,
            }
        ]
        with patch("routes.on_watchlist", mock_on_watchlist):
            actual_result = filter_watchlist(user_id, results)
            self.assertNotEqual(actual_result, expected_results)


if __name__ == "__main__":
    unittest.main()
