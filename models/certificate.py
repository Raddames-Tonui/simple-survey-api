from app import db
import uuid
from werkzeug.utils import secure_filename

class Certificate(db.Model):
    __tablename__ = 'certificates'

    id = db.Column(db.Integer, primary_key=True)
    file_url = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    submission = db.relationship('Submission', back_populates='certificates')

    def save_metadata(self, file_url, file_name=None):
        # If no file_name is passed, generate a unique name
        if not file_name:
            original_name = secure_filename(file_url.split("/")[-1])  # Get the file name from the URL
            unique_filename = f"{uuid.uuid4().hex}_{original_name}"  # Add UUID for uniqueness
        else:
            unique_filename = file_name

        # Save the metadata
        self.file_url = file_url
        self.file_name = unique_filename

    def serialize(self):
        return {
            'id': self.id,
            'file_url': self.file_url,
            'submission_id': self.submission_id
        }
