from datetime import datetime
from sqlalchemy import CHAR, TIMESTAMP, func, text, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ulid import ULID
from .sqlalchemy_base_model import SQLAlchemyBaseModel
from app.enums.video_process_status import VideoProcessStatus


class VideoModel(SQLAlchemyBaseModel):
    __tablename__ = "videos"

    id: Mapped[ULID] = mapped_column(
        name="id",
        type_=CHAR(length=26),
        primary_key=True,
        server_default=text("generate_ulid()"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        name="created_at",
        type_=TIMESTAMP(),
        server_default=func.current_timestamp(),
        nullable=False,
    )

    path: Mapped[str] = mapped_column(name="path", type_=CHAR(30), nullable=False)

    process_status: Mapped[VideoProcessStatus] = mapped_column(
        name="process_status",
        type_=Enum(VideoProcessStatus),
        server_default=VideoProcessStatus.PENDING,
        nullable=False,
        index=True,
    )

    frames: Mapped[list["VideoFrameModel"]] = relationship(  # noqa: F821 # type: ignore
        back_populates="video",
    )
