import db, models

db.create_db_and_tables()

with db.Session(db.engine) as s:
    # s.add(models.Hero(name="My hero", secret_name="her0"))
    # c1=models.Category(name="Электроника")
    # c2=models.Category(name="Еда")
    # s.add(c1)
    # s.add(c2)
    s.add(models.User(login="admin", password="123"))
    s.add(models.User(login="Alex", password="qwerty"))
    s.add(models.User(login="Sergey", password="54321"))
    s.commit()