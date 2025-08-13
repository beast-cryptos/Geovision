// GeoVision Map Functionality

let map;
let markers = [];
let userMarker;

// Initialize results map
function initializeResultsMap(mapData) {
    try {
        // Initialize map centered on first result or default location
        const center = mapData.results.length > 0 
            ? [mapData.results[0].lat, mapData.results[0].lng]
            : [20, 0]; // Default world center
        
        map = L.map('map').setView(center, 3);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 18
        }).addTo(map);
        
        // Add satellite layer as an option
        const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
            maxZoom: 18
        });
        
        // Add layer control
        const baseMaps = {
            "Street Map": L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }),
            "Satellite": satelliteLayer
        };
        
        L.control.layers(baseMaps).addTo(map);
        
        // Add result markers
        addResultMarkers(mapData.results);
        
        // Try to add user location if available
        addUserLocation();
        
        // Fit map to show all markers
        if (markers.length > 0) {
            const group = new L.featureGroup(markers);
            map.fitBounds(group.getBounds().pad(0.1));
        }
        
    } catch (error) {
        console.error('Error initializing map:', error);
        showMapError();
    }
}

// Add markers for search results
function addResultMarkers(results) {
    results.forEach((result, index) => {
        const confidenceColor = getMarkerColor(result.confidence);
        
        // Create custom icon based on confidence
        const icon = L.divIcon({
            className: 'custom-div-icon',
            html: `
                <div style="
                    background-color: ${confidenceColor};
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    border: 3px solid white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    color: white;
                    font-size: 14px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
                ">
                    ${index + 1}
                </div>
            `,
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        });
        
        // Create marker
        const marker = L.marker([result.lat, result.lng], { icon: icon }).addTo(map);
        
        // Create popup content
        const popupContent = createPopupContent(result, index + 1);
        marker.bindPopup(popupContent, {
            maxWidth: 300,
            className: 'custom-popup'
        });
        
        markers.push(marker);
    });
}

// Get marker color based on confidence
function getMarkerColor(confidence) {
    if (confidence >= 0.9) return '#28a745'; // Green for high confidence
    if (confidence >= 0.8) return '#ffc107'; // Yellow for medium confidence
    return '#dc3545'; // Red for low confidence
}

// Create popup content for markers
function createPopupContent(result, rank) {
    const distance = result.distance > 0 
        ? `<br><strong>Distance:</strong> ${result.distance.toFixed(1)} km`
        : '';
    
    const bearing = result.bearing > 0
        ? `<br><strong>Bearing:</strong> ${result.bearing.toFixed(1)}°`
        : '';
    
    return `
        <div class="map-popup">
            <h6 class="mb-2">
                <span class="badge bg-primary">#${rank}</span>
                ${result.name}
            </h6>
            <p class="mb-1">
                <strong>Confidence:</strong> 
                <span class="badge" style="background-color: ${getMarkerColor(result.confidence)}">
                    ${(result.confidence * 100).toFixed(1)}%
                </span>
            </p>
            <p class="mb-1">
                <strong>Coordinates:</strong><br>
                <code>${result.lat.toFixed(4)}, ${result.lng.toFixed(4)}</code>
                ${distance}
                ${bearing}
            </p>
        </div>
    `;
}

// Add user location marker if coordinates are available
function addUserLocation() {
    const userLat = document.getElementById('userLat');
    const userLon = document.getElementById('userLon');
    
    if (userLat && userLon && userLat.value && userLon.value) {
        const lat = parseFloat(userLat.value);
        const lng = parseFloat(userLon.value);
        
        // Create user location icon
        const userIcon = L.divIcon({
            className: 'user-location-icon',
            html: `
                <div style="
                    background-color: #007bff;
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                    border: 3px solid white;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
                    position: relative;
                ">
                    <div style="
                        position: absolute;
                        top: -8px;
                        left: -8px;
                        width: 36px;
                        height: 36px;
                        border-radius: 50%;
                        background-color: rgba(0, 123, 255, 0.2);
                        animation: pulse 2s infinite;
                    "></div>
                </div>
            `,
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        });
        
        userMarker = L.marker([lat, lng], { icon: userIcon }).addTo(map);
        userMarker.bindPopup(`
            <div class="map-popup">
                <h6 class="mb-2">
                    <i class="fas fa-user-location text-primary"></i>
                    Your Location
                </h6>
                <p class="mb-0">
                    <code>${lat.toFixed(6)}, ${lng.toFixed(6)}</code>
                </p>
            </div>
        `);
        
        markers.push(userMarker);
    }
}

// Show map error message
function showMapError() {
    const mapContainer = document.getElementById('map');
    if (mapContainer) {
        mapContainer.innerHTML = `
            <div class="d-flex align-items-center justify-content-center h-100 bg-light">
                <div class="text-center">
                    <i class="fas fa-exclamation-triangle fa-3x text-warning mb-3"></i>
                    <h5>Map Loading Error</h5>
                    <p class="text-muted">Unable to load the interactive map. Please refresh the page.</p>
                </div>
            </div>
        `;
    }
}

// Initialize basic map for upload page (if needed)
function initializeUploadMap() {
    // This could be used for a preview map on the upload page
    // Currently not implemented but structure is here for future enhancement
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% {
            transform: scale(1);
            opacity: 1;
        }
        100% {
            transform: scale(1.5);
            opacity: 0;
        }
    }
    
    .custom-popup .leaflet-popup-content {
        margin: 8px 12px;
    }
    
    .custom-popup .leaflet-popup-content-wrapper {
        border-radius: 8px;
    }
`;
document.head.appendChild(style);

// Export functions for global use
window.MapFunctions = {
    initializeResultsMap,
    initializeUploadMap
};
