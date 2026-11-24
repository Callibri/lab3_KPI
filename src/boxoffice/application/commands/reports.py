from dataclasses import dataclass
from datetime import date

from boxoffice.domain.errors import NotFoundError
from boxoffice.domain.factories import ReportFactory
from boxoffice.domain.repositories import MovieRepository, ReportRepository
from boxoffice.domain.value_objects import Money


@dataclass(frozen=True)
class AddReportCommand:
    movie_id: int
    report_date: date
    region: str
    revenue_usd: int
    tickets_sold: int


@dataclass(frozen=True)
class UpdateReportCommand:
    report_id: int
    revenue_usd: int
    tickets_sold: int


@dataclass(frozen=True)
class DeleteReportCommand:
    report_id: int


class AddReportHandler:
    def __init__(self, movies: MovieRepository, reports: ReportRepository, factory: ReportFactory):
        self._movies, self._reports, self._factory = movies, reports, factory

    def handle(self, cmd: AddReportCommand) -> int:
        movie = self._movies.get(cmd.movie_id)
        if movie is None:
            raise NotFoundError("Movie not found")
        report = self._factory.create(
            movie, cmd.report_date, cmd.region, cmd.revenue_usd, cmd.tickets_sold
        )
        return self._reports.add(report).id


class UpdateReportHandler:
    def __init__(self, reports: ReportRepository):
        self._reports = reports

    def handle(self, cmd: UpdateReportCommand) -> None:
        report = self._reports.get(cmd.report_id)
        if report is None:
            raise NotFoundError("Report not found")
        report.correct(revenue=Money(cmd.revenue_usd), tickets_sold=cmd.tickets_sold)
        self._reports.update(report)


class DeleteReportHandler:
    def __init__(self, reports: ReportRepository):
        self._reports = reports

    def handle(self, cmd: DeleteReportCommand) -> None:
        if self._reports.get(cmd.report_id) is None:
            raise NotFoundError("Report not found")
        self._reports.delete(cmd.report_id)
