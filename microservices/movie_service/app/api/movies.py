from microservices.movie_service.app.api.models import MovieUpdate
from typing import List, cast
from fastapi import Header, APIRouter, HTTPException

from app.api.models import MovieIn, MovieOut
from app.api import db_manager


movies = APIRouter()


@movies.get('/', response_model=List[MovieOut])
async def index():
    return await db_manager.get_all_movies()


@movies.get('/{id}/', response_model=MovieOut)
async def get_movie(id: int):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@movies.post('/', response_model=MovieOut, status_code=201)
async def add_movie(payload: MovieIn):
    for cast_id in payload.casts_id:
        if not is_cast_present(cast_id):
            raise HTTPException(status_code=404, detail=f'Cast with id:{cast_id} not found')
    movie_id = await db_manager.add_movie(payload)
    response = {
        'id': movie_id,
        **payload.dict()
    }
    return response


@movies.put('/{id}', response_model=MovieOut)
async def update_movie(id: int, payload: MovieUpdate):
    movie = await db_manager.get_movie(id)
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with given id not found")

    update_data = payload.dict(exclude_unset=True)

    if 'casts_id' in update_data:
        for cast_id in payload.casts_id:
            if not is_cast_present(cast_id):
                raise HTTPException(status_code=404, detail=f'Cast with given id:{cast_id} not found')
    
    movie_in_db = MovieIn(**movie)

    update_movie = movie_in_db.copy(update=update_data)

    return await db_manager.update_movie(id, update_movie)


@movies.delete('/{id}')
async def delete_movie(id: int):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with given id not found")
    return await db_manager.delete_movie(id)
