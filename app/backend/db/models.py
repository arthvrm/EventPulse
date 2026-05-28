from datetime import datetime
from decimal import Decimal
from typing import Any, Dict

from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, JSON, Numeric
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class RawEventModel(Base):
    __tablename__ = "raw_event_table"

    internal_event_id: Mapped[str] = mapped_column(String, primary_key=True)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    external_event_id: Mapped[str | None] = mapped_column(String)
    event_type: Mapped[str | None] = mapped_column(String)
    raw_body: Mapped[bytes] = mapped_column(Text, nullable=False)  # Assuming text for bytes
    headers: Mapped[Dict[str, str]] = mapped_column(JSON, nullable=False)
    query_params: Mapped[Dict[str, str]] = mapped_column(JSON, nullable=False, default=dict)
    signature: Mapped[str | None] = mapped_column(String)
    signature_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    request_id: Mapped[str] = mapped_column(String, nullable=False)
    client_ip: Mapped[str | None] = mapped_column(String)
    payload: Mapped[Dict[str, Any] | None] = mapped_column(JSON)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )


class ProcessedEventModel(Base):
    __tablename__ = "processed_event_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    payment_id: Mapped[str] = mapped_column(String, nullable=False)
    event_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    fee: Mapped[Decimal | None] = mapped_column(Numeric(precision=10, scale=2))
    net_amount: Mapped[Decimal | None] = mapped_column(Numeric(precision=10, scale=2))
    order_id: Mapped[str | None] = mapped_column(String)
    customer_id: Mapped[str | None] = mapped_column(String)
    failure_reason: Mapped[str | None] = mapped_column(String)
    processing_error: Mapped[str | None] = mapped_column(String)
    provider_created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    latency_ms: Mapped[int | None] = mapped_column(Integer)


class PaymentModel(Base):
    __tablename__ = "payment_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    payment_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    fee: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False, default=Decimal("0"))
    net_amount: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    order_id: Mapped[str | None] = mapped_column(String)
    customer_id: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    last_event_id: Mapped[str | None] = mapped_column(String)