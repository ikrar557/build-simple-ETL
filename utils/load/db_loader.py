from sqlalchemy.orm import sessionmaker
from ..database.config import create_db_engine
from ..database.models import Base, Product

def save_to_postgresql(data):
    engine = create_db_engine()
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        for item in data:
            product = Product(**item)
            session.merge(product)
        
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()