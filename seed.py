import db, models
from datetime import datetime
import bcrypt

db.create_db_and_tables()

with db.Session(db.engine) as s:
    # s.add(models.Hero(name="My hero", secret_name="her0"))
    # c1=models.Category(name="Электроника")
    # c2=models.Category(name="Еда")
    # s.add(c1)
    # s.add(c2)
    user = models.User(login="Alex", password=bcrypt.hashpw(b"qwerty123", bcrypt.gensalt()))
    user1 = models.User(login="qwerty", password=bcrypt.hashpw(b"123qwe", bcrypt.gensalt()))

    low = models.Priority(name="Low")
    medium = models.Priority(name="Medium")
    high = models.Priority(name="High")

    in_progress = models.Status(name="In Progress")
    completed = models.Status(name="Completed")
    cancelled = models.Status(name="Cancelled")

    s.add(user)
    s.add(user1)

    s.add(low)
    s.add(medium)
    s.add(high)

    s.add(in_progress)
    s.add(completed)
    s.add(cancelled)

    s.commit()

    s.add(models.Task(name="Врач",
                      description="Записаться к врачу на июнь",
                      deadline=datetime.strptime("31.05.2026", "%d.%m.%Y").timestamp(),
                      priority_id=high.id,
                      status_id=in_progress.id,
                      user_id=user.id))
    
    s.add(models.Task(name="Магазин",
                      description="Купить молока",
                      deadline=datetime.strptime("30.04.2026", "%d.%m.%Y").timestamp(),
                      priority_id=low.id,
                      status_id=cancelled.id,
                      user_id=user.id))
    
    s.add(models.Task(name="Звонок",
                      description="Позвонить в отдел кадров",
                      deadline=datetime.strptime("23.03.2026", "%d.%m.%Y").timestamp(),
                      priority_id=medium.id,
                      status_id=completed.id,
                      user_id=user.id))
    
    s.add(models.Task(name="Заказ",
                      description="Забрать заказ с WB",
                      deadline=datetime.strptime("22.02.2026", "%d.%m.%Y").timestamp(),
                      priority_id=low.id,
                      status_id=completed.id,
                      user_id=user.id))
    
    s.add(models.Task(name="Работа",
                      description="Доделать проект",
                      deadline=datetime.strptime("08.06.2026", "%d.%m.%Y").timestamp(),
                      priority_id=high.id,
                      status_id=in_progress.id,
                      user_id=user.id))
    
    s.add(models.Task(name="Кино",
                      description="Купить билеты",
                      deadline=datetime.strptime("30.04.2026", "%d.%m.%Y").timestamp(),
                      priority_id=medium.id,
                      status_id=in_progress.id,
                      user_id=user.id))
    
    s.add(models.Task(name="Магазин",
                      description="Купить хлеба",
                      priority_id=low.id,
                      status_id=completed.id,
                      user_id=user1.id))

    s.commit()