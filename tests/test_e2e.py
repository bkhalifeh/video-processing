from httpx import Client
from sqlalchemy import delete
from app.models import VideoModel
from app.core.database import get_db_session
import os

client = Client()


def test_list_videos():
    response = client.get("http://127.0.0.1:8000/api/video?page=1&size=50")
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list)


def test_enqueue_video():
    response = client.post(
        "http://127.0.0.1:8000/api/video",
        files={
            "video": open(os.path.join(os.path.dirname(__file__), "video.mp4"), "rb")
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    for key in ["id", "created_at", "path", "process_status"]:
        assert key in response_json


def test_dequeue_video():
    for session in get_db_session():
        session.execute(delete(VideoModel))
        session.commit()
    response = client.post(
        "http://127.0.0.1:8000/api/video",
        files={
            "video": open(os.path.join(os.path.dirname(__file__), "video.mp4"), "rb")
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    for key in ["id", "created_at", "path", "process_status"]:
        assert key in response_json
    last_video_id = response_json["id"]

    response = client.delete(
        "http://127.0.0.1:8000/api/video",
    )
    assert response.status_code == 200
    response_json = response.json()
    assert last_video_id == response_json["id"]
