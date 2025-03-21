from app.models.user import User, Customer
from app import db

class UserRepository:
    def __init__(self):
        self.model = User

    def find_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
    
    def create(self, user: User):
        db.session.add(user)
        db.session.commit()
        return user
    
    def find_by_id(self, id):
        return self.model.query.get(id)
    
    def all(self):
        return self.model.query.all()
    
    def delete(self, id):
        user = self.model.query.get(id)
        db.session.delete(user)
        db.session.commit()

class CustomerRepository:
    def __init__(self):
        self.model = Customer

    def create(self, customer: Customer):       
        db.session.add(customer)
        db.session.commit()
        return customer
    
    def delete(self, id):
        customer = self.model.query.get(id)
        db.session.delete(customer)
        db.session.commit() 

    def all(self):
        return self.model.query.all()
