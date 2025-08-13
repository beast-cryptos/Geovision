# GeoVision: AI-Powered Visual Search & Geolocation System

## Overview

GeoVision is a military and disaster response application that performs visual similarity matching on satellite, drone, or camera images. The system accepts image uploads, processes them for geospatial analysis, and returns matching results with geographic coordinates, distances, and bearings. It's designed to support both civil disaster response operations and military intelligence applications.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with Python
- **Database**: PostgreSQL with SQLAlchemy ORM using DeclarativeBase
- **Image Processing**: PIL (Python Imaging Library) for image resizing and optimization
- **File Handling**: Werkzeug secure filename handling with configurable upload limits (50MB max)
- **Session Management**: Flask sessions with configurable secret keys
- **Geospatial Calculations**: Custom Haversine formula implementation for distance and bearing calculations

### Data Storage Design
The system uses three main database tables:
- **Images**: Stores uploaded images with metadata, coordinates, and feature vectors
- **SearchResults**: Records similarity matches between query and reference images
- **AnalysisSessions**: Tracks processing sessions and performance metrics

### Image Processing Pipeline
Images are automatically processed upon upload:
- Resized to 800x600 pixels maintaining aspect ratio
- Converted to RGB format and saved as JPEG with 85% quality
- Centered on black background for consistent dimensions
- Feature vectors generated for similarity matching (currently mock data)

### Geospatial Analysis
The system calculates:
- Haversine distances between coordinate pairs
- Bearing angles from one location to another
- Distances from North and South poles
- Geographic relationships between matched locations

### Frontend Architecture
- **Templates**: Jinja2 HTML templates with Bootstrap 5 styling
- **Styling**: Custom CSS with military/tactical color schemes
- **Interactive Maps**: Leaflet.js integration for displaying results geographically
- **Form Handling**: Multi-mode operation selection (civil/military)
- **File Upload**: Drag-and-drop interface with real-time validation

### Application Structure
- **Modular Design**: Separate modules for routes, models, storage, image processing, and geospatial calculations
- **Sample Data**: Automatic initialization with landmark locations (Pentagon, Mount Everest, Dubai Port, etc.)
- **Error Handling**: Comprehensive logging and user feedback systems
- **Security**: File type validation, secure filename handling, and proxy-aware configuration

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web framework and request handling
- **SQLAlchemy**: Database ORM and connection management
- **PostgreSQL**: Primary database with connection pooling
- **Werkzeug**: WSGI utilities and security features

### Image Processing Libraries
- **PIL (Pillow)**: Image manipulation and optimization
- **NumPy**: Numerical operations for feature vector generation

### Frontend Libraries
- **Bootstrap 5**: CSS framework and responsive design
- **Font Awesome**: Icon library for UI elements
- **Leaflet.js**: Interactive mapping and geospatial visualization
- **OpenStreetMap**: Base map tiles and geographic data
- **ArcGIS**: Satellite imagery tiles for enhanced map views

### Development Tools
- **UUID**: Unique identifier generation for database records
- **Logging**: Application monitoring and debugging
- **OS/Path**: File system operations and path management

The system is designed to be deployment-ready with environment variable configuration for database connections, session secrets, and file storage paths.