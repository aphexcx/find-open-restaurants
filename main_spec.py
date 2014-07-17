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
                                      datetime.datetime(2014, 7, 13, 21, 40, 0, 0))
                ==
                ['The Cheesecake Factory', 'Rose Pistola', "Alioto's Restaurant", 'Sudachi', 'Penang Garden', 'Alhamra',
                 'San Dong House', 'India Garden Restaurant']
        )

    def test_is_open(self):
        #
        r = Restaurant("", "Mon-Sun 11:30 am - 9 pm")
        assert r.is_open(datetime.datetime(2014, 7, 14, 12, 40, 0, 0)) == True
        assert r.is_open(datetime.datetime(2014, 7, 13, 22, 40, 0, 0)) == False