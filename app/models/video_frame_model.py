from sqlalchemy import CHAR, INTEGER, ForeignKey, text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ulid import ULID
from .sqlalchemy_base_model import SQLAlchemyBaseModel


class VideoFrameModel(SQLAlchemyBaseModel):
    __tablename__ = "video_frames"

    timestamp: Mapped[int] = mapped_column(
        name="timestamp",
        type_=INTEGER,
        nullable=False,
    )

    frame_number: Mapped[int] = mapped_column(
        name="frame_number", type_=INTEGER, nullable=False, primary_key=True
    )

    video_id: Mapped[str] = mapped_column(
        ForeignKey("videos.id", ondelete="CASCADE"),
        name="video_id",
        type_=CHAR(length=26),
        nullable=False,
        primary_key=True,
    )

    video: Mapped["VideoModel"] = relationship(back_populates="frames")  # type: ignore # noqa: F821
