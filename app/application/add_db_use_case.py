from typing import Union
from app.infra.db.session import db_session
from app.infra.db.award_entity import AwardDB
from app.infra.db.movie_entity import MovieDB
from app.infra.db.producer_entity import ProducerDB
from app.infra.db.studio_entity import StudioDB
from app.infra.db.movie_x_producers_entity import movie_producers_db


class AddDB:

    @classmethod
    def get_all_awards(cls):

        try:
            # Consulta todos os registros
            awards = db_session.query(AwardDB).all()

            # Imprime resultados
            for award in awards:
                print(f"ID: {award.id}, Year: {award.year}, Winner: {award.winner}, Movie ID: {award.movie_id}")
        finally:
            db_session.close()

    @classmethod
    def get_or_create(
        cls, 
        cache: dict[str, Union[ProducerDB, StudioDB]], 
        name: str,
        table_obj: any
    ) -> any:
        
        if name in cache:
            return cache[name]

        response = db_session.query(table_obj).filter_by(name=name).first()

        if not response:
            entity = table_obj(name=name)
            db_session.add(entity)
            db_session.flush()
        else:
            entity = response

        cache[name] = entity

        return entity

    @classmethod
    def run(cls, log: 'LogUtils', rows: list[dict]):

        studios_cache = {}
        producers_cache = {}
        movies_bulk = []
        awards_bulk = []
        movie_producers_bulk = []

        for row in rows:

            log.info(f"Validando filme {row['title']} no ano {row['year']}")

            studio = cls.get_or_create(studios_cache, row['studios'], StudioDB)

            movie = MovieDB(title=row['title'], studio_id=studio.id)

            db_session.add(movie)
            db_session.flush()

            for producer_name in row['producers']:
                producer = cls.get_or_create(producers_cache, producer_name, ProducerDB)

                movie_producers_bulk.append({
                    "movie_id": movie.id,
                    "producer_id": producer.id,
                })

            award = AwardDB(
                movie_id=movie.id,
                year=row['year'],
                winner=row['winner']
            )

            movies_bulk.append(movie)
            awards_bulk.append(award)

        log.info("Carregando todos os dados...")
        db_session.bulk_save_objects(movies_bulk)
        db_session.bulk_save_objects(awards_bulk)
        db_session.execute(movie_producers_db.insert(), movie_producers_bulk)

        log.info("Realizando commit...")
        db_session.commit()
        db_session.close()        
