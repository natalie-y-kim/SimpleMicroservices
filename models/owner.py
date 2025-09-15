from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, StringConstraints

from .pet import PetBase

class OwnerBase(BaseModel):
    first_name: str = Field(
        ...,
        description="Given name.",
        json_schema_extra={"example": "Ada"},
    )
    last_name: str = Field(
        ...,
        description="Family name.",
        json_schema_extra={"example": "Lovelace"},
    )
    
    phone: str = Field(
        ...,
        description="Contact phone number in any reasonable format.",
        json_schema_extra={"example": "+1-212-555-0199"},
    )

    email: Optional[EmailStr] = Field(
        None,
        description="Primary email address.",
        json_schema_extra={"example": "ada@example.com"},
    )

    birth_date: Optional[date] = Field(
        None,
        description="Date of birth (YYYY-MM-DD).",
        json_schema_extra={"example": "1815-12-10"},
    )

    # Embed pets (each with persistent ID)
    pets: List[PetBase] = Field(
        default_factory=list,
        description="Pets owned by this owner (each carries a persistent ID).",
        json_schema_extra={
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Boba",
                    "species": "Cat",
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Ada",
                    "last_name": "Lovelace",
                    "phone": "+1-212-555-0199",
                    "email": "ada@example.com",
                    "birth_date": "1815-12-10",
                    "pets": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "name": "Boba",
                            "species": "Cat",
                        }
                    ]
                }
            ]
        }
    }


class OwnerCreate(OwnerBase):
    """Creation payload for an Owner."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Ada",
                    "last_name": "Lovelace",
                    "phone": "+1-212-555-0199",
                    "email": "ada@example.com",
                    "birth_date": "1815-12-10",
                    "pets": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "name": "Boba",
                            "species": "Cat",
                        }
                    ]
                }
            ]
        }
    }

class OwnerUpdate(BaseModel):
    """Partial update for an Owner; supply only fields to change."""
    first_name: Optional[str] = Field(None, json_schema_extra={"example": "Augusta"})
    last_name: Optional[str] = Field(None, json_schema_extra={"example": "King"})
    phone: Optional[str] = Field(None, json_schema_extra={"example": "+44 20 7946 0958"})
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "ada@newmail.com"})
    birth_date: Optional[date] = Field(None, json_schema_extra={"example": "1815-12-10"})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"first_name": "Ada", "last_name": "Byron"},
                {"phone": "+1-415-555-0199"}
            ]
        }
    }


class OwnerRead(OwnerBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Owner ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
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
                    "id": "99999999-9999-4999-8999-999999999999",
                    "first_name": "Ada",
                    "last_name": "Lovelace",
                    "phone": "+1-212-555-0199",
                    "email": "ada@example.com",
                    "birth_date": "1815-12-10",
                    "pets": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "name": "Boba",
                            "species": "Cat",
                        }
                    ],
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
