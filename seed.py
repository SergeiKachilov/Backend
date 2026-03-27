import db, models

db.create_db_and_tables()

with db.Session(db.engine) as s:
    # s.add(models.Hero(name="My hero", secret_name="her0"))
    c1=models.Category(name="Электроника")
    c2=models.Category(name="Еда")
    s.add(c1)
    s.add(c2)
    s.add(models.Product(name="Телевизор Hisense 65E7Q", description="Телевизор 65 дюймов", price=66700, category=c1))
    s.add(models.Product(name="Монитор Xiaomi", price=25000, category=c1))
    s.add(models.Product(name="Шоколад Аленка", price=120, category=c2))
    s.add(models.Product(name="Напиток Pepsi", price=90, category=c2))
    s.commit()