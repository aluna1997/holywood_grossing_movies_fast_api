from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, SmallInteger, text
from sqlalchemy.orm import relationship
from app.model.pydantic_sqlalchemy.base import Base

# SqlAlchemy Class.
class Sponsor(Base):
    __tablename__ = "sponsor"
    
    id_sponsor = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("highest_holywood_grossing_movie.id_movie"), nullable=False)
    sponsor_name = Column(String, nullable=False)
    sponsor_description = Column(String, nullable=False)
    creation_date = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    active = Column(SmallInteger, nullable=False, default=1)

    # Relations.
    movie = relationship('HighestHolywoodGrossingMovie', back_populates='sponsors')

# Pydantic Class.
PydanticSponsor = sqlalchemy_to_pydantic(Sponsor)