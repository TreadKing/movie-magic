""" This file tests various functions utilized in the project """
import unittest

# pylint: disable=E0401
from get_movie import get_genres, get_similar, get_upcoming, search
# pylint: disable=R0801
filters = {
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


if __name__ == "__main__":
    unittest.main()
