from data import teachers as teachers
from app import db, Teacher, Booking

#script for import json data to db
#                       name=teach['name'],
#                       about=teach['about'],
#                       price=teach['price'],
#                       rating=teach['rating'],
#                       picture=teach['picture'],
#                       goals=teach['goals'],
#                       free=teach['free']
for teach in teachers:
    teacher = Teacher(**teach)
    db.session.add(teacher)
db.session.commit()