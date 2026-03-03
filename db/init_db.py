# db/init_db.py
from db.base import Base
from db.session import engine
import models # noqa: F401 (모델 impport로 테이블 등록)

def init_db() -> None:
    Base.metadata.create_all(bind=engine)