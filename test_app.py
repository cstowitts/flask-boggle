from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            #bo
            self.assertIn('<!-- boggle-homepage: used in test -->', html)
            # test that you're getting a template

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            resp = client.post('api/new-game')
            parsed = resp.get_json()

            board = parsed.get("board")
            list_in_board = board[0]
            game_id = parsed.get("game_id")

            #tests if: 
            # -the object is a dict 
            # -each key return the correct value type
            self.assertIs(list, type(board))
            self.assertIs(list, type(list_in_board))
            self.assertIs(str, type(game_id))

            #tests if:
            #route stores new game in the games dict
            self.assertIn(game_id, games)

    def test_api_score_word(self):
        """Test if user input is:
        a valid word
        and on board"""

        with self.client as client:
            resp = client.post("api/score-word")
            parsed = resp.get_json()

            game_id = parsed.get("game_id")
            word = parsed.get("word")

        #mutate board using game_id to extract the words you want
            
