from app import db

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  
    required = db.Column(db.Boolean, default=True, nullable=False)
    text = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, nullable=False)

    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    survey = db.relationship('Survey', back_populates='questions')

    options = db.relationship('Option', back_populates='question', cascade='all, delete')
    answers = db.relationship('Answer', back_populates='question', cascade='all, delete')


    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'text': self.text,
            'description': self.description,
            'required': self.required,
            'type': self.type,
            'survey_id': self.survey_id,
            'order': self.order,
            'options': [option.serialize() for option in self.options]  
        }
