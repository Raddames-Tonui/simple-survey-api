from app import db

class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('User', back_populates='surveys')

    questions = db.relationship('Question', back_populates='survey', cascade='all, delete')
    submissions = db.relationship('Submission', back_populates='survey', cascade='all, delete')

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_published': self.is_published,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'creator_id': self.created_by,
        }
