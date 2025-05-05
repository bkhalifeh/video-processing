import os

from sqlalchemy import insert, update
from ulid import ULID
from app.core.settings import settings
from app.core.database import get_db_session
import cv2
from app.enums.video_process_status import VideoProcessStatus
from app.models.video_frame_model import VideoFrameModel
from app.models.video_model import VideoModel
from celery import Celery

celery_app = Celery(
    "video_tasks",
    broker=str(settings.celery.broker),
    backend=str(settings.celery.backend),
)

celery_conf = settings.celery.model_dump(
    exclude_none=True, exclude={"broker", "backend"}
)
if len(celery_conf) > 0:
    celery_app.conf.update(celery_conf)


@celery_app.task
def video_process(video_id: ULID, video_path: str):
    for session in get_db_session():
        try:
            cap = cv2.VideoCapture(os.path.join(settings.videos_path, video_path))
            if not cap.isOpened():
                raise ValueError("Could not open video file")
            frames = []
            frame_number = 0
            fps = cap.get(cv2.CAP_PROP_FPS)
            base_frame_path = os.path.join(settings.frames_path, str(video_id))
            os.makedirs(base_frame_path)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                timestamp = frame_number / fps
                frame_number += 1
                if timestamp % 120 == 0:
                    frames.append(
                        {
                            "video_id": video_id,
                            "frame_number": frame_number,
                            "timestamp": timestamp,
                        }
                    )
                    frame_path = os.path.join(base_frame_path, f"{frame_number}.jpg")
                    cv2.imwrite(frame_path, frame)
            session.execute(insert(VideoFrameModel).values(frames))
            session.execute(
                update(VideoModel)
                .where(VideoModel.id == str(video_id))
                .values(process_status=VideoProcessStatus.COMPLETED)
            )
        except Exception as _:
            session.execute(
                update(VideoModel)
                .where(VideoModel.id == str(video_id))
                .values(process_status=VideoProcessStatus.FAILED)
            )
        session.commit()
