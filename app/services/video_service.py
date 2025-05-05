from asyncio import create_task, gather
import os
import aiofiles
from sqlalchemy import insert, select, update

from fastapi import Depends, HTTPException, UploadFile
from ulid import ULID
from typing import Annotated

from app.core.database import AsyncDBSessionDep
from app.core.settings import SettingsDep
from app.models import VideoModel
from app.schemas.request.body.enqueue_body import EnQueueBody
from app.enums.video_process_status import VideoProcessStatus
from app.tasks.video_tasks import video_process


class VideoService:
    session: AsyncDBSessionDep
    settings: SettingsDep

    def __init__(
        self,
        session: AsyncDBSessionDep,
        settings: SettingsDep,
    ) -> None:
        self.session = session
        self.settings = settings

    async def enqueue(self, body: EnQueueBody):
        video_id = ULID()
        video_filename = f"{video_id}{os.path.splitext(body.video.filename)[1]}"
        task_save_db = create_task(self.save_db(video_filename, str(video_id)))
        video_path = os.path.join(self.settings.videos_path, video_filename)
        task_save_file = create_task(self.save_file(body.video, video_path))
        video, _ = await gather(task_save_db, task_save_file)
        return video

    async def save_file(self, video: UploadFile, video_path: str):
        async with aiofiles.open(video_path, "wb") as out_file:
            while content := await video.read(1024 * 1024):
                await out_file.write(content)

    async def save_db(self, video_filename: str, video_id: ULID):
        video = (
            (
                await self.session.execute(
                    insert(VideoModel)
                    .values(id=str(video_id), path=video_filename)
                    .returning(*VideoModel.__table__.columns)
                )
            )
            .mappings()
            .one_or_none()
        )
        await self.session.commit()
        return video

    async def dequeue(
        self,
    ):
        video = (
            (
                await self.session.execute(
                    update(VideoModel)
                    .where(
                        VideoModel.id
                        == select(VideoModel.id)
                        .where(VideoModel.process_status == VideoProcessStatus.PENDING)
                        .order_by(VideoModel.created_at)
                        .limit(1)
                    )
                    .values(process_status=VideoProcessStatus.PROCESSING)
                    .returning(VideoModel.__table__.columns)
                )
            )
            .mappings()
            .one_or_none()
        )
        print(video)
        if not video:
            raise HTTPException(404, "not found any video")
        # await self.session.commit()
        video_process.delay(video.id, video.path)
        return video

    async def get_one_video(self, video_id: str):
        video = (
            await self.session.execute(
                select(VideoModel).where(VideoModel.id == video_id)
            )
        ).scalar_one_or_none()
        return video

    async def get_all_videos(self):
        videos = await self.session.scalars(select(VideoModel))
        return videos


VideoServiceDep = Annotated[VideoService, Depends(VideoService)]
