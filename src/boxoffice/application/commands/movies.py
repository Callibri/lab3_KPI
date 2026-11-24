from dataclasses import dataclass
from datetime import date

from boxoffice.domain.errors import NotFoundError
from boxoffice.domain.factories import MovieFactory
from boxoffice.domain.repositories import MovieRepository
from boxoffice.domain.value_objects import Money


@dataclass(frozen=True)
class CreateMovieCommand:
    title: str
    genre: str
    release_date: date
    budget_usd: int


@dataclass(frozen=True)
class UpdateMovieCommand:
    movie_id: int
    title: str
    genre: str
    release_date: date
    budget_usd: int


@dataclass(frozen=True)
class DeleteMovieCommand:
    movie_id: int


class CreateMovieHandler:
    def __init__(self, factory: MovieFactory, movies: MovieRepository):
        self._factory, self._movies = factory, movies

    def handle(self, cmd: CreateMovieCommand) -> int:
        movie = self._factory.create(cmd.title, cmd.genre, cmd.release_date, cmd.budget_usd)
        return self._movies.add(movie).id


class UpdateMovieHandler:
    def __init__(self, factory: MovieFactory, movies: MovieRepository):
        self._factory, self._movies = factory, movies

    def handle(self, cmd: UpdateMovieCommand) -> None:
        movie = self._movies.get(cmd.movie_id)
        if movie is None:
            raise NotFoundError("Movie not found")
        movie.update(
            title=cmd.title, genre=cmd.genre, release_date=cmd.release_date,
            budget=Money(cmd.budget_usd),
        )
        self._factory.ensure_unique(movie)
        self._movies.update(movie)


class DeleteMovieHandler:
    def __init__(self, movies: MovieRepository):
        self._movies = movies

    def handle(self, cmd: DeleteMovieCommand) -> None:
        if self._movies.get(cmd.movie_id) is None:
            raise NotFoundError("Movie not found")
        self._movies.delete(cmd.movie_id)
