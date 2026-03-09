from app.db.base import Base
from uuid import uuid4, UUID
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import enum

class ExtractionStatus(str, enum.Enum):
  PENDING = 'PENDING'
  QUEUED = 'QUEUED'
  RUNNING = 'RUNNING'
  SUCCEEDED = 'SUCCEEDED'
  FAILED = 'FAILED'


class ExtractionRun(Base):
  __tablename__ = "extraction_runs"

  __table_args__ = (
    sa.UniqueConstraint("user_id", "idempotency_key", name="uq_extraction_runs_user_idempotency"),
    sa.Index("ix_extraction_runs_user_created", "user_id", "created_at"),
    sa.CheckConstraint("char_length(input_text) <= 20000", name="ck_extraction_runs_input_text_len")
  )

  id: Mapped[UUID] = mapped_column(
    PG_UUID(as_uuid=True), 
    primary_key=True, 
    default=uuid4
  )
  user_id: Mapped[str] = mapped_column(
    sa.String(128), 
    nullable=False
  )
  input_text: Mapped[str] = mapped_column(
    sa.Text, 
    nullable=False
  )
  input_sha256: Mapped[str] = mapped_column(
    sa.String(64), 
    nullable=False
  )
  status: Mapped[ExtractionStatus] = mapped_column(
    sa.Enum(ExtractionStatus, 
    name="extraction_status"), 
    nullable=False, 
    default=ExtractionStatus.PENDING, 
    server_default=sa.text("'PENDING'")
  )
  created_at: Mapped[datetime] = mapped_column(
    sa.DateTime(timezone=True), 
    server_default=sa.func.now(), 
    nullable=False
  )
  updated_at: Mapped[datetime] = mapped_column(
    sa.DateTime(timezone=True),
    server_default=sa.func.now(),
    onupdate=sa.func.now(),
    nullable=False
  )
  queued_at: Mapped[datetime | None] = mapped_column(
    sa.DateTime(timezone=True),
    nullable=True
  )
  started_at: Mapped[datetime | None] = mapped_column(
    sa.DateTime(timezone=True),
    nullable=True
  )
  finished_at: Mapped[datetime | None] = mapped_column(
    sa.DateTime(timezone=True),
    nullable=True
  )
  idempotency_key: Mapped[str | None] = mapped_column(
    sa.String(128),
    nullable=True
  )
  attempt: Mapped[int] = mapped_column(
    sa.Integer,
    nullable=False,
    default=0,
    server_default=sa.text("0")
  )
  result_json: Mapped[dict | None] = mapped_column(
    JSONB,
    nullable=True
  )
  error_message: Mapped[str | None] = mapped_column(
    sa.Text,
    nullable=True
  )
  