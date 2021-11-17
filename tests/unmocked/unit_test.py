import unittest
from flask import url_for, request
from werkzeug.utils import redirect
from routes import get_google_provider_cfg, client
from get_movie import get_movie_details, get_similar, get_upcoming, search
import json
from models import User


class TestStringMethods(unittest.TestCase):
    def test_login(self):
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        self.assertIsNotNone(request_uri)
        self.assertIn("https", request_uri)
        # check that the path changed
        self.assertEqual(request.path == url_for(request_uri))

    def test_save_actor(self):
        user_input = "Russell Brand"
        api_results = search(user_input)
        self.assertIsNotNone(api_results)
        movie_titles_list = []
        for movie in api_results:
            movie_titles_list.append(movie["movie_title"])
        self.assertIsNotNone(movie_titles_list)
        self.assertIn("Despicable Me", movie_titles_list)

    def test_save_text(self):
        user_input = ""
        movie_text = search(user_input)
        self.assertRaises(Exception, search)
        self.assertIsNone(movie_text)

        user_input = "Rush Hour"
        movie_text = search(user_input)
        self.assertIn("Rush Hour", movie_text)

    def test_search(self):
        user_input = "Rush Hour"
        result = search(user_input)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)

    def test_get_movie_details(self):
        user_input = "Rush Hour"
        api_results = get_movie_details(user_input)
        self.assertIsNotNone(api_results)
        self.assertIn("Comedy", api_results)

    def test_get_upcoming(self):
        api_results = get_upcoming()
        self.assertIsNotNone(api_results)
        api_results = json.loads(api_results)
        self.assertNotIn("ValueError", api_results)

    def test_get_similar(self):
        api_results = get_similar("2109")
        self.assertIsNotNone(api_results)
        api_results = json.loads(api_results)
        self.assertNotIn("ValueError", api_results)

    def test_user(self):
        new_user = User()
        new_user.user_id = "00000"
        new_user.username = "jack"
        result = new_user.get_username
        self.assertIsNotNone(result)
        self.assertIn("jack", result)


if __name__ == "__main__":
    unittest.main()
