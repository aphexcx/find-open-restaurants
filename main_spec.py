import pytest

from main import *
#pytest tests to exercise main.py

class TestMain:
    def test_find_open_restaurants_weekday(self):
        #12:40PM on Monday
        assert (find_open_restaurants("rest_hours.csv",
                                      datetime.datetime(2014, 7, 14, 12, 40, 0, 0))
                ==
                ['Kushi Tsuru', 'Osakaya Restaurant', 'The Stinking Rose', "McCormick & Kuleto's", 'Mifune Restaurant',
                 'The Cheesecake Factory', 'New Delhi Indian Restaurant', 'Iroha Restaurant', 'Rose Pistola',
                 "Alioto's Restaurant", 'Canton Seafood & Dim Sum Restaurant', 'All Season Restaurant',
                 'Bombay Indian Restaurant', "Sam's Grill & Seafood Restaurant", '2G Japanese Brasserie',
                 'Restaurant Lulu', 'Herbivore', 'Penang Garden', "John's Grill", 'Quan Bac', 'Burger Bar',
                 'Blu Restaurant', 'Shanghai China Restaurant', 'Tres', 'Isobune Sushi', 'Far East Cafe', 'Parallel 37',
                 'Bai Thong Thai Cuisine', 'Alhamra', 'A-1 Cafe Restaurant', "Nick's Lighthouse",
                 'Paragon Restaurant & Bar', 'Chili Lemon Garlic', 'Bow Hon Restaurant', 'San Dong House', "Cesario's",
                 'Colombini Italian Cafe Bistro', 'Sabella & La Torre', 'Soluna Cafe and Lounge', 'Tong Palace',
                 'India Garden Restaurant', 'Sapporo-Ya Japanese Restaurant', "Santorini's Mediterranean Cuisine",
                 'Kyoto Sushi']
        )

    def test_find_open_restaurants_weekend(self):
        #9:40PM on Sunday
        assert (find_open_restaurants("rest_hours.csv",
                                      datetime.datetime(2014, 7, 13, 22, 40, 0, 0))
                ==
                ['The Cheesecake Factory', 'Rose Pistola', "Alioto's Restaurant", 'Sudachi', 'Penang Garden', 'Alhamra',
                 'San Dong House', 'India Garden Restaurant']

        )

    def test_is_open(self):
        r = Restaurant("Soup Nazi", "Mon-Sat 11:30 am - 9 pm")
        # Monday 12:40PM is within open days and hours
        assert r.is_open(datetime.datetime(2014, 7, 14, 12, 40, 0, 0)) == True
        # Saturday 10:40PM is within open days, but outside of hours ()
        assert r.is_open(datetime.datetime(2014, 7, 12, 22, 40, 0, 0)) == False
        # Sunday 12:40PM is not within open days or hours
        assert r.is_open(datetime.datetime(2014, 7, 13, 12, 40, 0, 0)) == False

    def test_parse_hours(self):
        # simple hours string
        r = Restaurant("Top of the Muffin to You!", "Mon-Sun 11:30 am - 9 pm")
        assert r.daily_hours == [((11, 30), (21, 0)), ((11, 30), (21, 0)), ((11, 30), (21, 0)), ((11, 30), (21, 0)),
                                 ((11, 30), (21, 0)), ((11, 30), (21, 0)), ((11, 30), (21, 0))]
        #complex hours string
        r = Restaurant("Soup Nazi",
                       "Mon-Thu 11 am - 10:30 pm  / Fri 11 am - 11 pm  / Sat 11:30 am - 11 pm  / Sun 4:30 pm - 10:30 pm")
        assert r.daily_hours == [((11, 0), (22, 30)), ((11, 0), (22, 30)), ((11, 0), (22, 30)), ((11, 0), (22, 30)),
                                 ((11, 0), (23, 0)), ((11, 30), (23, 0)), ((16, 30), (22, 30))]
        # bad hours string
        with pytest.raises(RestaurantInitializationException):
            Restaurant("Soup Nazi", "No soup for you")
