from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime  

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(50), nullable=False, default='viewer')

    surveys = db.relationship('Survey', back_populates='creator', cascade='all, delete')
    submissions = db.relationship('Submission', back_populates='user', cascade='all, delete')
    date_created = db.Column(db.DateTime, server_default=db.func.now())

    def serialize(self):
        """Convert the datetime to string before serializing."""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'date_created': self.date_created.isoformat() 
        }

    def set_password(self, password):
        """Hashes the password before saving to the database."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the given password matches the stored hash."""
        return check_password_hash(self.password_hash, password)
