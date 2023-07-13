from flask_shop import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(36), unique = True, nullable = False)
    email_address = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(72), nullable = False)
    phone_number = db.Column(db.String(10), nullable = True)
    full_address = db.Column(db.String(72), nullable = True)
    
    def __repr__(self):
        return f"User id:{self.id} ('{self.username}', '{self.email_address}', '{self.phone_number}'.)"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String(120), nullable = False)
    product_description = db.Column(db.String(320), nullable = False)
    product_image = db.Column(db.String(72), nullable = False)
    product_price = db.Column(db.Double(), nullable = False)

    def __repr__(self):
        return f"Product('{self.product_name}', '{self.product_description}', '{self.product_price}'.)"
    
    
class Service(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    service_provided = db.Column(db.String(120), unique = True, nullable = False)
   
    def __repr__(self):
        return f"Service('{self.service_provided}'.)"
    
    
class Carts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default = 1)
    
    user = db.relationship("User", backref = db.backref("request", uselist=False))
    product = db.relationship("Product", backref = db.backref("product", uselist=False))
    
    