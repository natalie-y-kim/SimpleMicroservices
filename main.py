from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.owner import OwnerCreate, OwnerRead, OwnerUpdate
from models.pet import PetCreate, PetRead, PetUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))
# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
OWNERS: Dict[UUID, OwnerRead] = {}
PETS: Dict[UUID, PetRead] = {}

app = FastAPI(
    title="Owner/Pet API",
    description="Demo FastAPI app using Pydantic v2 models for Owner and Pet",
    version="0.1.0",
)

def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

# ---------------- Health ----------------
@app.get("/health", tags=["health"])
def health(echo: Optional[str] = Query(default=None)):
    return {
        "status": 200,
        "status_message": "OK",
        "timestamp": now_iso(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "echo": echo,
    }

# ---------------- Owners ----------------
@app.post("/owners", response_model=OwnerRead, status_code=201, tags=["owners"])
def create_owner(payload: OwnerCreate):
    owner = OwnerRead(**payload.model_dump())
    OWNERS[owner.id] = owner
    return owner

@app.get("/owners", response_model=List[OwnerRead], tags=["owners"])
def list_owners():
    for o in OWNERS.values():
        o.pets = [p for p in PETS.values() if p.owner_id == o.id]
    return list(OWNERS.values())

@app.get("/owners/{owner_id}", response_model=OwnerRead, tags=["owners"])
def get_owner(owner_id: UUID = Path(..., description="Owner ID")):
    owner = OWNERS.get(owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    owner.pets = [p for p in PETS.values() if p.owner_id == owner.id]
    return owner

@app.patch("/owners/{owner_id}", response_model=OwnerRead, tags=["owners"])
def patch_owner(owner_id: UUID, payload: OwnerUpdate):
    owner = OWNERS.get(owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    data = owner.model_dump()
    data.update({k: v for k, v in payload.model_dump(exclude_unset=True).items()})
    data["updated_at"] = datetime.utcnow()
    updated = OwnerRead(**data)
    updated.pets = [p for p in PETS.values() if p.owner_id == owner_id]
    OWNERS[owner_id] = updated
    return updated

@app.put("/owners/{owner_id}", tags=["owners"])
def put_owner_placeholder(owner_id: UUID):
    raise HTTPException(status_code=501, detail="Not implemented")

@app.delete("/owners/{owner_id}", status_code=204, tags=["owners"])
def delete_owner(owner_id: UUID):
    if owner_id not in OWNERS:
        raise HTTPException(status_code=404, detail="Owner not found")
    for pid in [pid for pid, pet in PETS.items() if pet.owner_id == owner_id]:
        del PETS[pid]
    del OWNERS[owner_id]
    return

# ---------------- Pets ----------------
@app.post("/pets", response_model=PetRead, status_code=201, tags=["pets"])
def create_pet(payload: PetCreate):
    if payload.owner_id not in OWNERS:
        raise HTTPException(status_code=400, detail="owner_id does not exist")
    pet = PetRead(**payload.model_dump())
    PETS[pet.id] = pet
    return pet

@app.get("/pets", response_model=List[PetRead], tags=["pets"])
def list_pets():
    return list(PETS.values())

@app.get("/pets/{pet_id}", response_model=PetRead, tags=["pets"])
def get_pet(pet_id: UUID):
    pet = PETS.get(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

@app.patch("/pets/{pet_id}", response_model=PetRead, tags=["pets"])
def patch_pet(pet_id: UUID, payload: PetUpdate):
    pet = PETS.get(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    data = pet.model_dump()
    data.update({k: v for k, v in payload.model_dump(exclude_unset=True).items()})
    data["updated_at"] = datetime.utcnow()
    updated = PetRead(**data)
    PETS[pet_id] = updated
    return updated

@app.put("/pets/{pet_id}", tags=["pets"])
def put_pet_placeholder(pet_id: UUID):
    raise HTTPException(status_code=501, detail="Not implemented")

@app.delete("/pets/{pet_id}", status_code=204, tags=["pets"])
def delete_pet(pet_id: UUID):
    if pet_id not in PETS:
        raise HTTPException(status_code=404, detail="Pet not found")
    del PETS[pet_id]
    return

# ---------------- Root ----------------
@app.get("/")
def root():
    return {"message": "See /docs for OpenAPI UI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
