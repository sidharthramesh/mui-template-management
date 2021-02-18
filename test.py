from sqlalchemy.orm.session import Session
import models
from database import SessionLocal


db: Session = SessionLocal()

t = models.WebTemplate(data="1234")
db.add(t)
db.commit()
db.refresh(t)

print(db.query(models.WebTemplate).count())

print(t.id)