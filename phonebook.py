from app import app, db
from app.models import User, Book

# u = User(username='max', email='max@example.com')
# u.set_password("pax")
# db.session.add(u)
# db.session.commit()

# u = User.query.get(1)
# p = Book(person='my first book!')
# db.session.add(p)
# db.session.commit()

#clear database==================
# users = User.query.all()
# for u in users:
#     db.session.delete(u)
# books = Book.query.all()
# for p in books:
#     db.session.delete(p)
#     db.session.commit()
#================================

if __name__ == '__main__':
    app.run() 