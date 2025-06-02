from fastapi import HTTPException, status
from sqlalchemy import select
from .models import Address
import math


class AddressHelper:
    """
    Helper class for address-related operations.
    """

    @staticmethod
    async def check_for_existing_address(address_in, db, exclude_id=None):
        """
        Checks if an address with the same latitude and longitude already exists in the database.
        Args:
            address_in: An object containing the latitude and longitude attributes to check.
            db: The async database session used to perform the query.
            exclude_id: Optional address ID to exclude from the check (for updates).
        Raises:
            HTTPException: If an address with the same latitude and longitude already exists.
        Returns:
            The existing address object if found, otherwise None.
        """
        stmt = select(Address).where(
            Address.latitude == address_in.latitude,
            Address.longitude == address_in.longitude,
            Address.is_deleted == False,
        )
        if exclude_id is not None:
            stmt = stmt.where(Address.id != exclude_id)
        result = await db.execute(stmt)
        existing = result.scalars().first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Address with same latitude and longitude already exists",
            )
        return existing

    @staticmethod
    async def get_address(address_id, db):
        """
        Retrieve an address from the database by its ID or fetch all the non-deleted address.
        Args:
            address_id (int or None): The ID of the address to retrieve. If None, retrieves the first non-deleted address.
            db (AsyncSession): The asynchronous database session to use for the query.
        Returns:
            Address: The address object retrieved from the database.
        Raises:
            HTTPException: If the address with the given ID is not found.
        """
        if address_id:
            stmt = select(Address).where(
                Address.id == address_id, Address.is_deleted == False
            )
            result = await db.execute(stmt)
            address = result.scalars().first()
            if not address:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
                )

        else:
            stmt = select(Address).where(Address.is_deleted == False)
            result = await db.execute(stmt)
            address = result.scalars().all()

        return address

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        """
        
        Calculates the great-circle distance between two points on the Earth's surface using the Haversine formula.

        Args:
            lat1 (float): Latitude of the first point in decimal degrees.
            lon1 (float): Longitude of the first point in decimal degrees.
            lat2 (float): Latitude of the second point in decimal degrees.
            lon2 (float): Longitude of the second point in decimal degrees.

        Returns:
            float: Distance between the two points in kilometers.
        """
        R = 6371  # Earth radius in kilometers
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lambda = math.radians(lon2 - lon1)
        a = (
            math.sin(d_phi / 2) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
