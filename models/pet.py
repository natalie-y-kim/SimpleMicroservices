from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class PetBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Pet ID (server-generated).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    name: str = Field(
        ...,
        description="Pet NAme",
        json_schema_extra={"example": "Boba"},
    )
    species: str = Field(
        ...,
        description="species of pet",
        json_schema_extra={"example": "Cat"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Boba",
                    "species": "Cat",
                }
            ]
        }
    }


class PetCreate(PetBase):
    """Creation payload; ID is generated server-side but present in the base model."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Boba",
                    "species": "Cat",
                }
            ]
        }
    }


class PetUpdate(BaseModel):
    """Partial update; address ID is taken from the path, not the body."""

    name: Optional[str] = Field(
        None, description="Pet name", json_schema_extra={"name": "Boba"}
    )
    species: Optional[str] = Field(
        None, description="Pet Species", json_schema_extra={"species": "cat"}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Boba",
                    "species": "Cat",
                }
            ]
        }
    }


class PetRead(PetBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Boba",
                    "species": "Cat",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
