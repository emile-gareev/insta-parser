from fastapi.routing import APIRouter

from dependencies import get_user_photos


router = APIRouter()


@router.get('/getPhotos')
async def get_photos(username: str, max_count: int = 100) -> dict:
    photos = await get_user_photos(username, max_count)
    return {'urls': photos}
