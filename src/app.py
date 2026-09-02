"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

from activity_store import (
    create_activity,
    delete_activity,
    load_activities,
    signup_for_activity,
    unregister_from_activity,
    update_activity,
)

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Load activities from the dedicated persistence module.
activities = load_activities()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return load_activities()


@app.post("/activities")
def add_activity(payload: dict):
    try:
        activity = create_activity(
            payload["name"],
            payload["description"],
            payload["schedule"],
            payload["max_participants"],
        )
        return activity
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.put("/activities/{activity_name}")
def update_activity_endpoint(activity_name: str, payload: dict):
    try:
        return update_activity(
            activity_name,
            description=payload.get("description"),
            schedule=payload.get("schedule"),
            max_participants=payload.get("max_participants"),
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.delete("/activities/{activity_name}")
def delete_activity_endpoint(activity_name: str):
    try:
        delete_activity(activity_name)
        return {"message": f"Deleted activity {activity_name}"}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/activities/{activity_name}/signup")
def signup_for_activity_endpoint(activity_name: str, email: str):
    """Sign up a student for an activity"""
    try:
        return signup_for_activity(activity_name, email)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Activity not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity_endpoint(activity_name: str, email: str):
    """Unregister a student from an activity"""
    try:
        return unregister_from_activity(activity_name, email)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Activity not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
