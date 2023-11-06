from app.model.db_connection import DatabaseConnection
from app.model.pydantic_sqlalchemy.sponsor import Sponsor
from app.model.pydantic_sqlalchemy.highest_holywood_grossing_movie import HighestHolywoodGrossingMovie

from datetime import datetime

# Logger.
from app.logger import configure_log
logger = configure_log()

# GLOBALS
optionals = ['id_sponsor','creation_date','active']

def create_sponsor(session,info_sponsor):
    '''
    Create a new sponsor in the database.

    This function creates a new sponsor entry in the database based on the provided information.

    :param session: SQLAlchemy session object.
    :type session: Session

    :param info_sponsor: A dictionary containing information about the sponsor.
    :type info_sponsor: dict

    :return: The ID of the newly created sponsor entry.
    :rtype: int

    :raises: Exception if there is an error during the creation process.

    Example:
    >>> info = {'name': 'Example Sponsor', 'website': 'https://www.example.com', 'description': 'A sample sponsor.'}
    >>> create_sponsor(session, info)
    '''
    new_sponsor = Sponsor()

    for key,value in info_sponsor.items():
        if (not value) and (key not in optionals):
            str_err = f'{key} no puede ser vacío al crear un nuevo sponsor.'
            logger.error(str_err)
            raise Exception(str_err)
        else:
            setattr(new_sponsor, key, value)
        
    try:
        session.add(new_sponsor)
        session.commit()
        return new_sponsor.id_sponsor
    except Exception as err:
        session.rollback()
        str_err = f'Ocurrió un error al creear Sponsor: {str(err)}.'
        logger.error(str_err)
        raise err
    
def read_sponsor(session,id_sponsor = False):
    '''
    Retrieve sponsors from the database.

    This function retrieves sponsors from the database based on the provided ID or all active sponsors.

    :param session: SQLAlchemy session object.
    :type session: Session

    :param id_sponsor: An optional ID of the sponsor to retrieve. If not provided, all active sponsors are retrieved.
    :type id_sponsor: int, optional

    :return: A list of sponsors matching the query criteria.
    :rtype: list

    :raises: Exception if there is an error during the retrieval process.

    Example:
    >>> # Retrieve all active sponsors
    >>> read_sponsor(session)

    >>> # Retrieve a specific sponsor by ID
    >>> read_sponsor(session, 1)
    '''
    
    if not id_sponsor:
        try:
            filter = Sponsor.active == 1
            sponsors = session.query(Sponsor).filter(filter).all()
        except Exception as err:
            session.rollback()
            str_err = f'Ocurrió un error al leer Sponsor: {str(err)}.'
            logger.error(str_err)
            raise err
    else:
        try:
            sponsors = session.get(Sponsor,id_sponsor)
        except Exception as err:
            session.rollback()
            str_err = f'Ocurrió un error al leer Sponsors: {str(err)}.'
            logger.error(str_err)
            raise err

    return sponsors

def update_sponsor(session,id_sponsor,info_sponsor):
    '''
    Update an existing sponsor in the database.

    This function updates an existing sponsor in the database based on the provided ID and information.

    :param session: SQLAlchemy session object.
    :type session: Session

    :param id_sponsor: The ID of the sponsor to be updated.
    :type id_sponsor: int

    :param info_sponsor: A dictionary containing updated information for the sponsor.
    :type info_sponsor: dict

    :return: The ID of the updated sponsor.
    :rtype: int

    :raises: Exception if there is an error during the update process.

    Example:
    >>> info = {'name': 'Updated Sponsor', 'website': 'https://www.updatedsponsor.com', 'description': 'An updated sponsor.'}
    >>> update_sponsor(session, 1, info)
    '''

    if not id_sponsor:
        str_err = 'Para actualizar, el id_sponsor no debe ser vacío.'
        logger.error(str_err)
        raise Exception(str_err)
    
    sponsor = session.get(Sponsor,id_sponsor)

    if not sponsor:
        str_err = 'El id a actualizar no existe, no se actualiza nada.'
        logger.error(str_err)
        raise Exception(str_err)

    for key,value in info_sponsor.items():
        if getattr(sponsor, key, None):
            setattr(sponsor, key, value)
        else:
            logger.warning(f'El atributo {key} no existe para el objeto de sponsor, se ignora.')

    try:
        session.add(sponsor)
        session.commit()
        return sponsor.id_sponsor
    except Exception as err:
        session.rollback()
        str_err = f'Ocurrió un error al actualizar Sponsor: {str(err)}.'
        logger.error(str_err)
        raise err

def delete_sponsor(session,id_sponsor):
    '''
    Delete a sponsor from the database.

    This function marks a sponsor as inactive in the database based on the provided ID.

    :param session: SQLAlchemy session object.
    :type session: Session

    :param id_sponsor: The ID of the sponsor to be deleted.
    :type id_sponsor: int

    :return: The ID of the sponsor that was marked as inactive.
    :rtype: int

    :raises: Exception if there is an error during the deletion process.

    Example:
    >>> delete_sponsor(session, 1)
    '''
    if not id_sponsor:
        str_err = 'Para eliminar, el id_sponsor no debe ser vacío.'
        logger.error(str_err)
        raise Exception(str_err)
    
    sponsor = session.get(Sponsor,id_sponsor)

    if not sponsor:
        logger.warning('El id a eliminar no existe, no se actualiza nada.')

    try:
        sponsor.active = 0
        session.commit()
        return sponsor.id_sponsor
    except Exception as err:
        session.rollback()
        str_err = f'Ocurrió un error al eliminar Sponsor: {str(err)}.'
        logger.error(str_err)
        raise err
    
if __name__ == "__main__":
    db_conn = DatabaseConnection()
    session = db_conn.get_session()
    print(read_sponsor(session=session))
    db_conn.close_session()