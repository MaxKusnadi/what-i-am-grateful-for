import unittest

# Models
from test_cases.gratitude.models import TestGratitudeModel, TestGratitudeDatabaseController
from test_cases.prayer.models import TestPrayerModel, TestPrayerDatabaseController

# Controllers
from test_cases.gratitude.controller import TestGratitudeController
from test_cases.prayer.controller import TestPrayerController

# Views
from test_cases.gratitude.views import TestGratitudeView
from test_cases.prayer.views import TestPrayerView


if __name__ == '__main__':
    unittest.main()
