from app import app, db
from app.models import User, Note

# u = User(username='Max', email='max@example.com')
# u.set_password("123")
# db.session.add(u)
# db.session.commit()

# u = User.query.get(1)
# n = Note(name='Eugene', last_name='Zaycev', phone='88005553535')
# db.session.add(p)
# db.session.commit()

# users = User.query.all()
# for u in users:
#     print(u.id, u.username)

#clear database==================
# def clear_data(session):
#     meta = db.metadata
#     for table in reversed(meta.sorted_tables):
#         print('Clear table %s' % table)
#         session.execute(table.delete())
#     session.commit()

# clear_data(db.session)
#================================

if __name__ == '__main__':
    app.run() 