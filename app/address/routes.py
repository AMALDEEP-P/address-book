from typing import List
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status, Query
from loguru import logger
from app.address.models import Address
from app.address.schemas import AddressCreate, AddressUpdate, AddressOut
from app.db.session import get_db
from app.address.helpers import AddressHelper as address_helper

router = APIRouter(prefix="/address")


@router.post("/", response_model=AddressOut, status_code=status.HTTP_201_CREATED)
async def create_address(address_in: AddressCreate, db: Session = Depends(get_db)):
    """
    Create a new address in the database.
    """
    logger.info(f"Attempting to create address: {address_in}")
    await address_helper.check_for_existing_address(address_in, db)
    address = Address(**address_in.model_dump())
    db.add(address)
    try:
        await db.commit()
        await db.refresh(address)
        logger.info(f"Address created successfully with id={address.id}")
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Integrity error while creating address: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error"
        )
    return address


@router.patch("/{address_id}", response_model=AddressOut)
async def patch_address(
    address_id: int, address_in: AddressUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing address by ID.
    """
    logger.info(f"Attempting to update address id={address_id} with data: {address_in}")
    address = await address_helper.get_address(address_id, db)
    if address_in.latitude is not None and address_in.longitude is not None:
        await address_helper.check_for_existing_address(
            address_in, db, exclude_id=address_id
        )
    for field, value in address_in.model_dump(exclude_unset=True).items():
        setattr(address, field, value)
    await db.commit()
    await db.refresh(address)
    logger.info(f"Address id={address_id} updated successfully")
    return address


@router.delete("/{address_id}", status_code=status.HTTP_200_OK)
async def delete_address(address_id: int, db: Session = Depends(get_db)):
    """
    Soft delete an address by setting is_deleted to True.
    """
    logger.info(f"Attempting to soft delete address id={address_id}")
    address = await address_helper.get_address(address_id, db)
    address.is_deleted = True
    await db.commit()
    logger.info(f"Address id={address_id} soft deleted successfully")
    return {"message": "Address deleted"}


@router.get("/", response_model=List[AddressOut])
async def list_addresses(db: Session = Depends(get_db)):
    """
    List all non-deleted addresses.
    """
    logger.info("Listing all non-deleted addresses")
    addresses = await address_helper.get_address(None, db)
    logger.info(f"Found {len(addresses)} addresses")
    return addresses


@router.get("/nearby/", response_model=List[AddressOut])
async def get_addresses_within_distance(
    latitude: float = Query(..., description="Latitude of the center point"),
    longitude: float = Query(..., description="Longitude of the center point"),
    distance_km: float = Query(..., description="Distance in kilometers"),
    db: Session = Depends(get_db),
):
    """
    Retrieve all addresses within a given distance (in km) from the specified coordinates.
    """
    logger.info(
        f"Finding addresses within {distance_km} km of ({latitude}, {longitude})"
    )
    stmt = select(Address).where(Address.is_deleted == False)
    result = await db.execute(stmt)
    addresses = result.scalars().all()
    filtered = [
        address
        for address in addresses
        if address_helper.haversine(latitude, longitude, address.latitude, address.longitude)
        <= distance_km
    ]
    logger.info(f"Found {len(filtered)} addresses within {distance_km} km")
    return filtered
