from sqlalchemy.orm import sessionmaker
from ..database.config import create_db_engine
from ..database.models import Base, Product

def save_to_postgresql(data):
    if data is None or not isinstance(data, list):
        raise ValueError("Empty input data")
    if not data:
        raise ValueError("Empty input data")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Invalid input data")

    engine = create_db_engine()
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        for item in data:
            try:
                product = Product(**item)
                session.merge(product)
            except TypeError as e:
                session.rollback()
                raise ValueError(f"Invalid product data: {str(e)}")
        
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise Exception(f"Error saving to database: {str(e)}")
    finally:
        session.close()