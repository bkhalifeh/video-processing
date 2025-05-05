from datetime import datetime
from pydantic import BaseModel
from ulid import ULID

from app.enums.video_process_status import VideoProcessStatus


class VideoResponse(BaseModel):
    id: ULID
    created_at: datetime
    path: str
    process_status: VideoProcessStatus
