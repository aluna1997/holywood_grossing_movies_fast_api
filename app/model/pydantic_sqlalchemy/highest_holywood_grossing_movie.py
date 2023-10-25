from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, text
from sqlalchemy.orm import relationship
from app.model.pydantic_sqlalchemy.base import Base

class HighestHolywoodGrossingMovie(Base):
    __tablename__ = "highest_holywood_grossing_movie"

    id_movie = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    movie_info = Column(String, nullable=False)
    distributor = Column(String, nullable=False)
    release_date = Column(String, nullable=False)
    domestic_sales = Column(Integer, nullable=False)
    international_sales = Column(Integer, nullable=False)
    world_sales = Column(Integer, nullable=False)
    genere = Column(String, nullable=False)
    movie_runtime = Column(String, nullable=False)
    license = Column(String, nullable=False)
    creation_date = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    active = Column(SmallInteger, nullable=False, default=1)

    # Relations.
    sponsors = relationship('Sponsor', back_populates="movie")