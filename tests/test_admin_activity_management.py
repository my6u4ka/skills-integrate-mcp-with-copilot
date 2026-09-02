import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient

import app as app_module


class AdminActivityManagementTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_path = Path(self.temp_dir.name) / "activities.json"
        self.data_path.write_text(
            json.dumps(
                {
                    "Chess Club": {
                        "description": "Learn strategies and compete in chess tournaments",
                        "schedule": "Fridays, 3:30 PM - 5:00 PM",
                        "max_participants": 12,
                        "participants": ["michael@mergington.edu"],
                    }
                }
            ),
            encoding="utf-8",
        )
        os.environ["ACTIVITIES_DATA_FILE"] = str(self.data_path)
        app_module.activities = app_module.load_activities()
        self.client = TestClient(app_module.app)

    def tearDown(self):
        self.temp_dir.cleanup()
        os.environ.pop("ACTIVITIES_DATA_FILE", None)

    def test_create_activity(self):
        response = self.client.post(
            "/activities",
            json={
                "name": "Robotics Club",
                "description": "Build and program robots",
                "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
                "max_participants": 18,
            },
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertEqual(payload["name"], "Robotics Club")
        self.assertIn("Robotics Club", app_module.load_activities())

    def test_update_activity(self):
        response = self.client.put(
            "/activities/Chess Club",
            json={
                "description": "Updated description",
                "schedule": "Mondays, 3:00 PM - 4:30 PM",
                "max_participants": 15,
            },
        )

        self.assertEqual(response.status_code, 200)
        data = app_module.load_activities()
        self.assertEqual(data["Chess Club"]["description"], "Updated description")
        self.assertEqual(data["Chess Club"]["max_participants"], 15)

    def test_delete_activity(self):
        response = self.client.delete("/activities/Chess Club")

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Chess Club", app_module.load_activities())


if __name__ == "__main__":
    unittest.main()
