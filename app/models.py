from app import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

association_table = db.Table('laundried_clothes',
    db.Column('laundry_id', db.Integer, db.ForeignKey('laundry.id')),
    db.Column('clothes_id', db.Integer, db.ForeignKey('clothes.id')),
    db.Column('returned', db.Boolean, default=False)
)

class Clothes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    c_type = db.Column(db.String(50))
    color = db.Column(db.String(50))
    owner = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    cloth_pic = db.Column(db.String(200))
    desc = db.Column(db.String(200))
    inputted_at = db.Column(db.DateTime)
    
    def __init__(self, c_type, color, owner, cloth_pic, inputted_at, desc):
        self.c_type = c_type
        self.color = color
        self.owner = owner
        self.desc = desc
        self.cloth_pic = cloth_pic
        self.inputted_at = inputted_at
        
class Launderer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(200))
    l_pic = db.Column(db.String(200))
    phone_num = db.Column(db.String(50))
    desc = db.Column(db.String(200))
    has_whatsapp = db.Column(db.Boolean)
    has_delivery = db.Column(db.Boolean)
    inputted_at = db.Column(db.DateTime)
    
    def __init__(self, name, address, l_pic, phone_num, has_whatsapp, has_delivery, inputted_at, desc):
        self.name = name
        self.address = address
        self.l_pic = l_pic
        self.phone_num = phone_num
        self.has_whatsapp = has_whatsapp
        self.desc = desc
        self.has_delivery = has_delivery
        self.inputted_at = inputted_at
        
class Laundry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    launderer = db.Column(db.Integer, db.ForeignKey('launderer.id'))
    clothes = db.relationship('Clothes', secondary=association_table, backref='laundry_ref')
    bill_pic = db.Column(db.String(200))
    laundered_at = db.Column(db.DateTime)
    laundry_days = db.Column(db.Integer())
    status = db.Column(db.String(50), default='ongoing')
    owner = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    
    def __init__(self, launderer, bill_pic, laundered_at, laundry_days, status, owner):
        self.launderer = launderer
        self.bill_pic = bill_pic
        self.laundered_at = laundered_at
        self.laundry_days = laundry_days
        self.status = status
        self.owner = owner