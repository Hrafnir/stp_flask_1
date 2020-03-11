import data
from app import db, Teacher, Goal

# #script for import json data to db
#                       name=teach['name'],
#                       about=teach['about'],
#                       price=teach['price'],
#                       rating=teach['rating'],
#                       picture=teach['picture'],
#                       goals=teach['goals'],
#                       free=teach['free']
for teach in data.teachers:
    teacher = Teacher(t_id=teach['t_id'],
                      name=teach['name'],
                      about=teach['about'],
                      price=teach['price'],
                      rating=teach['rating'],
                      picture=teach['picture'],
                      free=str(teach['free'])
                      )
    db.session.add(teacher)

    for i in teach['goals']:
        goal = Goal(goal_name=i,
                    teacher_id=teach['t_id']
                    )
        db.session.add(goal)

