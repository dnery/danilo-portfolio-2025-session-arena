from sqlalchemy.ext.asyncio import AsyncSession

from app.models import FeatureFlag


async def set_flag(session: AsyncSession, key: str, enabled: bool) -> FeatureFlag:
    flag = await session.get(FeatureFlag, key)
    if flag is not None:
        flag.enabled = enabled
    else:
        flag = FeatureFlag(key=key, enabled=enabled)
        session.add(flag)
    return flag

