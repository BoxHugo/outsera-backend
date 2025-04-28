from app.infra.db.award_entity import AwardDB
from app.infra.db.producer_entity import ProducerDB
from app.infra.db.movie_entity import MovieDB
from app.infra.db.movie_x_producers_entity import movie_producers_db
from app.infra.db.session import db_session
from app.domain.models.movie_award_model import MovieAwardModel


class IntervalsController:

    @classmethod
    def get_award_intervals(cls):

        try:
            producer_wins = {}
            intervals = []

            query = (
                db_session.query(ProducerDB.name, AwardDB.year)
                .join(movie_producers_db, ProducerDB.id == movie_producers_db.c.producer_id)
                .join(MovieDB, MovieDB.id == movie_producers_db.c.movie_id)
                .join(AwardDB, AwardDB.movie_id == MovieDB.id)
                .filter(AwardDB.winner == "yes")
            )

            rows = query.all()

            for producer_name, year in rows:

                if producer_name not in producer_wins:
                    producer_wins[producer_name] = []

                producer_wins[producer_name].append(year)

            for producer, years in producer_wins.items():

                if len(years) < 2:
                    continue

                years.sort()

                for i in range(len(years) - 1):

                    interval = years[i + 1] - years[i]

                    intervals.append(
                        MovieAwardModel(
                            producer=producer,
                            interval=interval,
                            previousWin=years[i],
                            followingWin=years[i + 1]
                        )
                    )

            if not intervals:
                return {"min": [], "max": []}

            min_interval_value = min(interval.interval for interval in intervals)
            max_interval_value = max(interval.interval for interval in intervals)

            min_list = [i for i in intervals if i.interval == min_interval_value]
            max_list = [i for i in intervals if i.interval == max_interval_value]

            return {
                "min": [i.dict() for i in min_list],
                "max": [i.dict() for i in max_list]
            }

        finally:
            db_session.close()
