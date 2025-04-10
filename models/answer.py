from app import db

class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'), nullable=True)
    response_value = db.Column(db.String(255), nullable=True)

    question = db.relationship('Question', back_populates='answers')
    submission = db.relationship('Submission', back_populates='answers')
    option = db.relationship('Option', back_populates='answers')

    def serialize(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'submission_id': self.submission_id,
            'option_id': self.option_id,
            'response_value': self.response_value,
        }
