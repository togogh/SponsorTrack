from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.all import GeneratedSponsorship, Sponsorship
from backend.schemas.generated_sponsorship import (
    GeneratedSponsorshipCreate,
    GeneratedSponsorshipUpdate,
)
from sqlalchemy import select, update
from pydantic import UUID4


class GeneratedSponsorshipRepository:
    async def get_by_id(self, id: UUID4, session: AsyncSession):
        stmt = select(GeneratedSponsorship).where(GeneratedSponsorship.id == id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_sponsorship_id(self, sponsorship_id: UUID4, session: AsyncSession):
        stmt = (
            select(GeneratedSponsorship).join(Sponsorship).where(Sponsorship.id == sponsorship_id)
        )
        result = await session.execute(stmt)
        segments = result.scalars().all()
        return segments

    async def add(self, data: GeneratedSponsorshipCreate, session: AsyncSession):
        sponsored_segment = GeneratedSponsorship(**data.model_dump())
        session.add(sponsored_segment)
        await session.commit()
        await session.refresh(sponsored_segment)
        return sponsored_segment

    async def update(self, id: UUID4, data: GeneratedSponsorshipUpdate, session: AsyncSession):
        values = data.model_dump(exclude_unset=True)
        if not values:
            return
        await session.execute(
            update(GeneratedSponsorship)
            .where(GeneratedSponsorship.id == id)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        await session.commit()
