from app import db
from datetime import datetime
import uuid

class Image(db.Model):
    __tablename__ = 'images'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    file_name = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.Text, nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    mime_type = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    feature_vector = db.Column(db.JSON)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by = db.Column(db.String)

class SearchResult(db.Model):
    __tablename__ = 'search_results'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query_image_id = db.Column(db.String, nullable=False)
    match_image_id = db.Column(db.String, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    distance = db.Column(db.Float)
    bearing = db.Column(db.Float)
    distance_from_north_pole = db.Column(db.Float)
    distance_from_south_pole = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AnalysisSession(db.Model):
    __tablename__ = 'analysis_sessions'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    image_id = db.Column(db.String, nullable=False)
    mode = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False, default='processing')
    processing_time = db.Column(db.Float)
    total_matches = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
