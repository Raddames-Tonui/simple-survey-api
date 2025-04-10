from flask import Blueprint, jsonify
from models.certificate import Certificate

certificates = Blueprint('certificates', __name__)

# Route to get certificate details by ID (for download and viewing)
@certificates.route('/api/questions/responses/certificates/<int:certificate_id>', methods=["GET"])
def get_certificate(certificate_id):
    try:
        # Retrieve the certificate from the database using the ID
        certificate = Certificate.query.get(certificate_id)
        
        if not certificate:
            return jsonify({"error": "Certificate not found"}), 404
        
        # Get the file URL and file name
        file_url = certificate.file_url
        file_name = certificate.file_name
        
        return jsonify({
            'file_url': file_url,
            'file_name': file_name
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
