from data.database import Database

db = Database()

db.update_balance(625558881, 500)
db.update_ref_balance(625558881, 500)
db.update_balance(2093027799, 500)
db.update_ref_balance(2093027799, 500)

__all__ = ['db']
