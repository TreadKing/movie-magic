import unittest
from flask import url_for, request
from werkzeug.utils import redirect
from routes import get_google_provider_cfg, client
from get_movie import search


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

        user_input = "Rush Hour 3"
        movie_text = search(user_input)
        self.assertIn("Rush Hour 3", movie_text)


if __name__ == "__main__":
    unittest.main()
