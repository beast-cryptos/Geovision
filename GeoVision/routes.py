import os
import time
from flask import render_template, request, redirect, url_for, flash, jsonify, send_file
from werkzeug.utils import secure_filename
from app import app, db
from models import Image, AnalysisSession, SearchResult
from image_processor import process_uploaded_image, generate_feature_vector
from geospatial import calculate_distance, calculate_bearing, calculate_polar_distances
from storage import create_image, create_analysis_session, create_search_result, get_all_images, get_image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tiff', 'tif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            flash('No image file provided', 'error')
            return redirect(url_for('index'))
        
        file = request.files['image']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload JPEG, PNG, or TIFF images.', 'error')
            return redirect(url_for('index'))
        
        # Get form data
        mode = request.form.get('mode', 'civil')
        user_lat = request.form.get('userLat', type=float)
        user_lon = request.form.get('userLon', type=float)
        
        # Process the image
        filename = secure_filename(file.filename)
        processed_image_path, file_size, mime_type = process_uploaded_image(file, filename)
        
        # Generate feature vector
        feature_vector = generate_feature_vector()
        
        # Create image record
        image_id = create_image(
            file_name=filename,
            file_path=processed_image_path,
            file_size=file_size,
            mime_type=mime_type,
            feature_vector=feature_vector
        )
        
        # Create analysis session
        session_id = create_analysis_session(image_id, mode)
        
        # Perform similarity search
        start_time = time.time()
        matches = perform_similarity_search(image_id, feature_vector, user_lat, user_lon)
        processing_time = time.time() - start_time
        
        # Update session status
        session = AnalysisSession.query.get(session_id)
        session.status = 'completed'
        session.processing_time = processing_time
        session.total_matches = len(matches)
        db.session.commit()
        
        flash(f'Analysis completed! Found {len(matches)} similar locations.', 'success')
        return redirect(url_for('results', session_id=session_id))
        
    except Exception as e:
        app.logger.error(f"Upload error: {str(e)}")
        flash('An error occurred during image processing. Please try again.', 'error')
        return redirect(url_for('index'))

def perform_similarity_search(query_image_id, query_vector, user_lat=None, user_lon=None):
    """Perform visual similarity search against database images"""
    try:
        # Get all sample images with coordinates
        sample_images = get_all_images()
        matches = []
        
        for image in sample_images:
            if image.latitude is None or image.longitude is None:
                continue
                
            # Calculate similarity score (mock implementation)
            import random
            confidence = round(random.uniform(0.7, 0.95), 3)
            
            # Calculate geospatial metrics
            distance = None
            bearing = None
            if user_lat is not None and user_lon is not None:
                distance = calculate_distance(user_lat, user_lon, image.latitude, image.longitude)
                bearing = calculate_bearing(user_lat, user_lon, image.latitude, image.longitude)
            
            # Calculate polar distances
            north_pole_dist, south_pole_dist = calculate_polar_distances(image.latitude, image.longitude)
            
            # Create search result record
            result_id = create_search_result(
                query_image_id=query_image_id,
                match_image_id=image.id,
                confidence=confidence,
                distance=distance,
                bearing=bearing,
                distance_from_north_pole=north_pole_dist,
                distance_from_south_pole=south_pole_dist
            )
            
            matches.append({
                'id': result_id,
                'image': image,
                'confidence': confidence,
                'distance': distance,
                'bearing': bearing,
                'north_pole_distance': north_pole_dist,
                'south_pole_distance': south_pole_dist
            })
        
        # Sort by confidence and return top 5
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        return matches[:5]
        
    except Exception as e:
        app.logger.error(f"Similarity search error: {str(e)}")
        return []

@app.route('/results/<session_id>')
def results(session_id):
    try:
        session = AnalysisSession.query.get_or_404(session_id)
        image = get_image(session.image_id)
        
        # Get search results
        search_results = SearchResult.query.filter_by(query_image_id=session.image_id).all()
        
        # Enrich results with image data
        enriched_results = []
        for result in search_results:
            match_image = get_image(result.match_image_id)
            enriched_results.append({
                'result': result,
                'image': match_image
            })
        
        return render_template('results.html', 
                             session=session, 
                             image=image, 
                             results=enriched_results)
    except Exception as e:
        app.logger.error(f"Results error: {str(e)}")
        flash('Error loading results. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/image/<image_id>')
def serve_image(image_id):
    try:
        image = get_image(image_id)
        if not image:
            return "Image not found", 404
        
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], image.file_path)
        if not os.path.exists(full_path):
            return "Image file not found", 404
            
        return send_file(full_path, mimetype=image.mime_type)
    except Exception as e:
        app.logger.error(f"Serve image error: {str(e)}")
        return "Error serving image", 500

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Maximum size is 50MB.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    app.logger.error(f"Server error: {str(e)}")
    flash('An internal server error occurred. Please try again.', 'error')
    return redirect(url_for('index'))
