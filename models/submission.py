from app import db

class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    date_submitted = db.Column(db.DateTime, server_default=db.func.now())

    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    email_address = db.Column(db.String(255), nullable=True)  

    survey = db.relationship('Survey', back_populates='submissions')
    user = db.relationship('User', back_populates='submissions')

    certificates = db.relationship('Certificate', back_populates='submission', cascade='all, delete')
    answers = db.relationship('Answer', back_populates='submission', cascade='all, delete')

    def serialize(self):
        return {
            'id': self.id,
            'date_submitted': self.date_submitted,
            'survey_id': self.survey_id,
            'user_id': self.user_id,
            'email_address': self.email_address  
        }
