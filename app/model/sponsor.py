from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, SmallInteger, text
from sqlalchemy.orm import relationship
from app.model.pydantic_sqlalchemy.base import Base

# SqlAlchemy Class.
class Sponsor(Base):
    '''
    Represents a model for a sponsor in a database.

    This class defines the structure of the "sponsor" table, including its columns,
    relationships, and default values.

    Attributes:
        id_sponsor (int): The primary key for the sponsor record.
        movie_id (int): The foreign key referencing the associated movie's ID.
        sponsor_name (str): The name of the sponsor.
        sponsor_description (str): A description of the sponsor.
        creation_date (datetime): The timestamp of when the sponsor record was created.
        active (int): Flag indicating the status of the sponsor record (default is 1, which means active).

    Relationships:
        movie (relationship): A relationship to the "HighestHolywoodGrossingMovie" model,
        indicating the movie associated with this sponsor.

    '''
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