import data
import json
from app import db, Teacher, Goal
# #script for import json data to db

goals = {"travel": "⛱ Для путешествий", "study": "🏫 Для учебы", "work": "🏢 Для работы", "relocate": "🚜 Для переезда"}

for teach in data.teachers:
    teacher = Teacher(t_id=teach['t_id'],
                      name=teach['name'],
                      about=teach['about'],
                      price=teach['price'],
                      rating=teach['rating'],
                      picture=teach['picture'],
                      free=json.dumps(teach['free'])
                      )
    db.session.add(teacher)
    for i in teach['goals']:
        goal = Goal(goal_name=goals[i],
                    teacher=teacher)
        db.session.add(goal)
db.session.commit()
