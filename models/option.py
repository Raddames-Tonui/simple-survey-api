from app import db

class Option(db.Model):
    __tablename__ = 'options'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255), nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    question = db.relationship('Question', back_populates='options')

    answers = db.relationship('Answer', back_populates='option', cascade='all, delete')

    def serialize(self):
        return {
            'id': self.id,
            'value': self.value,
            'question_id': self.question_id
        }
