from fastapi import APIRouter, Form, Path
from typing import Annotated

from ulid import ULID
from app.schemas.request.body.enqueue_body import EnQueueBody
from app.schemas.response.video_response import VideoResponse
from app.services.video_service import VideoServiceDep

router = APIRouter(prefix="/video", tags=["Video"])


@router.post(path="")
async def enqueue_video(
    body: Annotated[EnQueueBody, Form(media_type="multipart/form-data")],
    video_service: VideoServiceDep,
):
    return await video_service.enqueue(body)


@router.delete(path="")
async def dequeue_video(
    video_service: VideoServiceDep,
):
    return await video_service.dequeue()


@router.get(path="", response_model=list[VideoResponse])
async def get_all_videos(video_service: VideoServiceDep):
    return await video_service.get_all_videos()


@router.get(path="/{video_id}")
async def get_one_video(
    video_id: Annotated[ULID, Path()], video_service: VideoServiceDep
):
    return await video_service.get_one_video(str(video_id))
