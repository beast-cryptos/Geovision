from app import db
from models import Image, AnalysisSession, SearchResult
import uuid

def create_image(file_name, file_path, file_size, mime_type, latitude=None, longitude=None, feature_vector=None, uploaded_by=None):
    """Create a new image record in the database"""
    try:
        image = Image(
            id=str(uuid.uuid4()),
            file_name=file_name,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type,
            latitude=latitude,
            longitude=longitude,
            feature_vector=feature_vector,
            uploaded_by=uploaded_by
        )
        db.session.add(image)
        db.session.commit()
        return image.id
    except Exception as e:
        db.session.rollback()
        raise e

def get_all_images():
    """Retrieve all images from the database"""
    return Image.query.all()

def get_image(image_id):
    """Get a specific image by ID"""
    return Image.query.get(image_id)

def create_analysis_session(image_id, mode):
    """Create a new analysis session"""
    try:
        session = AnalysisSession(
            id=str(uuid.uuid4()),
            image_id=image_id,
            mode=mode,
            status='processing'
        )
        db.session.add(session)
        db.session.commit()
        return session.id
    except Exception as e:
        db.session.rollback()
        raise e

def create_search_result(query_image_id, match_image_id, confidence, distance=None, bearing=None, distance_from_north_pole=None, distance_from_south_pole=None):
    """Create a new search result record"""
    try:
        result = SearchResult(
            id=str(uuid.uuid4()),
            query_image_id=query_image_id,
            match_image_id=match_image_id,
            confidence=confidence,
            distance=distance,
            bearing=bearing,
            distance_from_north_pole=distance_from_north_pole,
            distance_from_south_pole=distance_from_south_pole
        )
        db.session.add(result)
        db.session.commit()
        return result.id
    except Exception as e:
        db.session.rollback()
        raise e

def get_search_results_by_query(query_image_id):
    """Get all search results for a specific query image"""
    return SearchResult.query.filter_by(query_image_id=query_image_id).all()
