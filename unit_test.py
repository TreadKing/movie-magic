""" This file tests various functions utilized in the project """
import unittest
import unittest.mock as mock
from unittest.mock import patch

# pylint: disable=E0401
from get_movie import get_genres, get_similar, get_upcoming, search
from routes import filter_watchlist

test_filters = {
    "genre_filter": "",
    "year_filter": None,
    "year_before_after": False,
    "rating_filter": None,
    "rating_before_after": False,
}


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
        api_results = search(user_input, test_filters)
        self.assertIsNotNone(api_results)
        movie_titles_list = []
        for movie in api_results:
            movie_titles_list.append(movie["movie_title"])
        self.assertIsNotNone(movie_titles_list)
        self.assertIn("Despicable Me", movie_titles_list)

    def test_save_movie(self):
        """
        GIVEN a string or blank
        WHEN a User attempts to add a movie to their list
        THEN check valid movie is added to list or exception thrown if blank
        """
        user_input = ""
        movie_text = search(user_input, test_filters)
        self.assertRaises(Exception, search)
        self.assertIsNone(movie_text)

        user_input = "Rush Hour"
        movie_text = search(user_input, test_filters)
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
        result = search(user_input, test_filters)
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
        Checks if the function filter_watchlist will correctly
        change the status of on_watchlist given that the movie id
        is already on the watchlist
        """

        def mock_on_watchlist(l):
            sample_list = ["120467"]
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

        user_id = "2IjhH2mMvdgqCSxUBPi6lcwLKI23"
        test_results = [
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
            actual_result = filter_watchlist(user_id, test_results)
            self.assertEqual(actual_result, expected_results)

    def test_search(self):
        """
        GIVEN a movie title
        WHEN a User attempts Search
        THEN check valid Search results
        """
        user_input = "Russel Brand"
        filters = {
            "genre_filter": "",
            "year_filter": None,
            "year_before_after": False,
            "rating_filter": None,
            "rating_before_after": False,
        }
        expected_result = [
            {
                "movie_id": 20352,
                "movie_title": "Despicable Me",
                "movie_image": "https://image.tmdb.org/t/p/original/fb9zF01GKOkNziYVusg20laWsGh.jpg",
                "genres": ["Family", "Animation", "Comedy"],
                "release_date": "2010-07-08",
                "rating": 7.2,
                "on_watchlist": False,
            },
            {
                "movie_id": 93456,
                "movie_title": "Despicable Me 2",
                "movie_image": "https://image.tmdb.org/t/p/original/5Fh4NdoEnCjCK9wLjdJ9DJNFl2b.jpg",
                "genres": ["Animation", "Comedy", "Family"],
                "release_date": "2013-06-26",
                "rating": 6.9,
                "on_watchlist": False,
            },
        ]

        def mock_search_movie(l, s):
            return []

        def mock_search_actor(l, s):
            return []

        with patch("get_movie.search_movie", mock_search_movie):
            actual_result = search(user_input, filters)
            self.assertEqual(actual_result, expected_result)

        user_input = "Edward Scissorhands"
        expected_result = [
            {
                "movie_id": 162,
                "movie_title": "Edward Scissorhands",
                "movie_image": "https://image.tmdb.org/t/p/original/1RFIbuW9Z3eN9Oxw2KaQG5DfLmD.jpg",
                "genres": ["Fantasy", "Drama", "Romance"],
                "release_date": "1990-12-05",
                "rating": 7.7,
                "on_watchlist": False,
            },
            {
                "movie_id": 683841,
                "movie_title": "The Making of Edward Scissorhands",
                "movie_image": "https://image.tmdb.org/t/p/original/pNllsZFsXiLAerWVQAY47RXjj4N.jpg",
                "genres": ["Documentary", "Drama", "Fantasy"],
                "release_date": "1990-12-14",
                "rating": 7.8,
                "on_watchlist": False,
            },
        ]
        with patch("get_movie.search_actor", mock_search_actor):
            actual_result = search(user_input, filters)
            self.assertEqual(expected_result, actual_result)


if __name__ == "__main__":
    unittest.main()
