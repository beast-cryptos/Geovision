from storage import create_image, get_all_images
from image_processor import generate_feature_vector
import logging


def init_sample_data():
    """Initialize sample satellite image data with landmark locations"""

    # Check if sample data already exists
    existing_images = get_all_images()
    if len(existing_images) >= 8:
        logging.info("Sample data already initialized")
        return

    sample_locations = [{
        'name': 'Pentagon',
        'latitude': 38.8719,
        'longitude': -77.0563,
        'file_name': 'pentagon_satellite.jpg'
    }, {
        'name': 'Mount Everest',
        'latitude': 27.9881,
        'longitude': 86.9250,
        'file_name': 'mount_everest_satellite.jpg'
    }, {
        'name': 'Dubai Port',
        'latitude': 25.2048,
        'longitude': 55.2708,
        'file_name': 'dubai_port_satellite.jpg'
    }, {
        'name': 'Golden Gate Bridge',
        'latitude': 37.8199,
        'longitude': -122.4783,
        'file_name': 'golden_gate_satellite.jpg'
    }, {
        'name': 'Taj Mahal',
        'latitude': 27.1751,
        'longitude': 78.0421,
        'file_name': 'taj_mahal_satellite.jpg'
    }, {
        'name': 'Sydney Harbor',
        'latitude': -33.8568,
        'longitude': 151.2153,
        'file_name': 'sydney_harbor_satellite.jpg'
    }, {
        'name': 'Pyramids of Giza',
        'latitude': 29.9792,
        'longitude': 31.1342,
        'file_name': 'pyramids_giza_satellite.jpg'
    }, {
        'name': 'Big Ben',
        'latitude': 51.5007,
        'longitude': -0.1246,
        'file_name': 'big_ben_satellite.jpg'
    }]

    try:
        for location in sample_locations:
            # Generate feature vector for each location
            feature_vector = generate_feature_vector()

            # Create image record
            create_image(
                file_name=location['file_name'],
                file_path=
                f"sample_{location['name'].lower().replace(' ', '_')}.jpg",
                file_size=512000,  # Mock file size
                mime_type='image/jpeg',
                latitude=location['latitude'],
                longitude=location['longitude'],
                feature_vector=feature_vector,
                uploaded_by='system')

        logging.info(f"Initialized {len(sample_locations)} sample locations")

    except Exception as e:
        logging.error(f"Error initializing sample data: {str(e)}")
