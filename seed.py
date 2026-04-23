import db
import models as m
from datetime import datetime
import bcrypt

m.SQLModel.metadata.drop_all(db.engine)
m.SQLModel.metadata.create_all(db.engine)

with db.Session(db.engine) as session:
    session.add(m.Status(name="Ожидает выполнения"))
    s2=m.Status(name="Готово")
    session.add(s2)
    session.add(m.Status(name="Возникли проблемы"))
    u1=m.User(login="admin", password="12345678")
    session.add(u1)

    session.add(m.Task(name="Задача 1", description="Описание", deadline=datetime.now(), status=s2, user=u1))

    session.commit()