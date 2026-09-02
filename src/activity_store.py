import json
import os
from copy import deepcopy
from pathlib import Path

DEFAULT_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"],
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"],
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"],
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"],
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"],
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"],
    },
}


def get_data_file_path() -> Path:
    env_path = os.getenv("ACTIVITIES_DATA_FILE")
    if env_path:
        return Path(env_path)
    return Path(__file__).resolve().parent / "activities.json"


def save_activities(activities):
    data_file = get_data_file_path()
    data_file.parent.mkdir(parents=True, exist_ok=True)
    with data_file.open("w", encoding="utf-8") as file:
        json.dump(activities, file, indent=2)
    return activities


def load_activities():
    data_file = get_data_file_path()
    if not data_file.exists():
        return save_activities(deepcopy(DEFAULT_ACTIVITIES))

    with data_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def create_activity(name, description, schedule, max_participants):
    activities = load_activities()
    if name in activities:
        raise ValueError(f"Activity '{name}' already exists")

    activity = {
        "description": description,
        "schedule": schedule,
        "max_participants": max_participants,
        "participants": [],
    }
    activities[name] = activity
    save_activities(activities)
    return activity


def update_activity(name, description=None, schedule=None, max_participants=None):
    activities = load_activities()
    if name not in activities:
        raise KeyError(f"Activity '{name}' not found")

    activity = activities[name]
    if description is not None:
        activity["description"] = description
    if schedule is not None:
        activity["schedule"] = schedule
    if max_participants is not None:
        activity["max_participants"] = max_participants

    save_activities(activities)
    return activity


def delete_activity(name):
    activities = load_activities()
    if name not in activities:
        raise KeyError(f"Activity '{name}' not found")

    del activities[name]
    save_activities(activities)
    return activities


def signup_for_activity(activity_name, email):
    activities = load_activities()
    if activity_name not in activities:
        raise KeyError(f"Activity '{activity_name}' not found")

    activity = activities[activity_name]
    if email in activity["participants"]:
        raise ValueError("Student is already signed up")

    activity["participants"].append(email)
    save_activities(activities)
    return {"message": f"Signed up {email} for {activity_name}"}


def unregister_from_activity(activity_name, email):
    activities = load_activities()
    if activity_name not in activities:
        raise KeyError(f"Activity '{activity_name}' not found")

    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise ValueError("Student is not signed up for this activity")

    activity["participants"].remove(email)
    save_activities(activities)
    return {"message": f"Unregistered {email} from {activity_name}"}
