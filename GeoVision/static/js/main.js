// GeoVision Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('GeoVision System Initialized');
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize file upload enhancements
    initializeFileUpload();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Enhanced form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

// File upload enhancements
function initializeFileUpload() {
    const fileInput = document.getElementById('imageFile');
    const dropZone = document.getElementById('dropZone');
    
    if (!fileInput || !dropZone) return;
    
    // File input change handler
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            validateAndDisplayFile(file);
        }
    });
    
    // Drag and drop handlers
    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });
    
    dropZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        if (!dropZone.contains(e.relatedTarget)) {
            dropZone.classList.remove('drag-over');
        }
    });
    
    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            fileInput.files = e.dataTransfer.files;
            validateAndDisplayFile(file);
        }
    });
}

// Validate and display selected file
function validateAndDisplayFile(file) {
    const maxSize = 50 * 1024 * 1024; // 50MB
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/tiff'];
    
    // Validate file type
    if (!allowedTypes.includes(file.type)) {
        showAlert('Invalid file type. Please select a JPEG, PNG, or TIFF image.', 'danger');
        return false;
    }
    
    // Validate file size
    if (file.size > maxSize) {
        showAlert('File too large. Maximum size is 50MB.', 'danger');
        return false;
    }
    
    // Display file info
    displayFileInfo(file);
    return true;
}

// Display file information
function displayFileInfo(file) {
    const fileSize = (file.size / 1024 / 1024).toFixed(2);
    const fileInfo = `
        <div class="alert alert-info mt-3" role="alert">
            <i class="fas fa-file-image me-2"></i>
            <strong>${file.name}</strong> (${fileSize} MB)
            <div class="progress mt-2" style="height: 4px;">
                <div class="progress-bar bg-success" role="progressbar" style="width: 100%"></div>
            </div>
        </div>
    `;
    
    // Remove existing file info
    const existingInfo = document.querySelector('.file-info');
    if (existingInfo) {
        existingInfo.remove();
    }
    
    // Add new file info
    const dropZone = document.getElementById('dropZone');
    dropZone.insertAdjacentHTML('afterend', fileInfo);
    document.querySelector('.alert.alert-info').classList.add('file-info');
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="fas fa-${type === 'danger' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const container = document.querySelector('.container');
    const firstChild = container.firstElementChild;
    firstChild.insertAdjacentHTML('beforebegin', alertHtml);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        const alert = document.querySelector('.alert');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

// Get current location with enhanced error handling
function getCurrentLocation() {
    if (!navigator.geolocation) {
        showAlert('Geolocation is not supported by this browser.', 'warning');
        return;
    }
    
    // Show loading state
    const button = event.target;
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Getting Location...';
    button.disabled = true;
    
    const options = {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000 // 5 minutes
    };
    
    navigator.geolocation.getCurrentPosition(
        function(position) {
            const lat = position.coords.latitude.toFixed(6);
            const lon = position.coords.longitude.toFixed(6);
            
            document.getElementById('userLat').value = lat;
            document.getElementById('userLon').value = lon;
            
            showAlert(`Location acquired: ${lat}, ${lon}`, 'success');
            
            // Restore button
            button.innerHTML = originalText;
            button.disabled = false;
        },
        function(error) {
            let message = 'Error getting location: ';
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    message += 'Location access denied by user.';
                    break;
                case error.POSITION_UNAVAILABLE:
                    message += 'Location information unavailable.';
                    break;
                case error.TIMEOUT:
                    message += 'Location request timed out.';
                    break;
                default:
                    message += 'Unknown error occurred.';
                    break;
            }
            
            showAlert(message, 'danger');
            
            // Restore button
            button.innerHTML = originalText;
            button.disabled = false;
        },
        options
    );
}

// Format coordinates for display
function formatCoordinates(lat, lon) {
    const latDir = lat >= 0 ? 'N' : 'S';
    const lonDir = lon >= 0 ? 'E' : 'W';
    return `${Math.abs(lat).toFixed(4)}°${latDir}, ${Math.abs(lon).toFixed(4)}°${lonDir}`;
}

// Format distance for display
function formatDistance(km) {
    if (km < 1) {
        return `${(km * 1000).toFixed(0)} m`;
    } else if (km < 100) {
        return `${km.toFixed(1)} km`;
    } else {
        return `${km.toFixed(0)} km`;
    }
}

// Format bearing with cardinal direction
function formatBearing(bearing) {
    const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                       'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
    const index = Math.round(bearing / 22.5) % 16;
    return `${bearing.toFixed(1)}° (${directions[index]})`;
}

// Confidence level color coding
function getConfidenceClass(confidence) {
    if (confidence >= 0.9) return 'confidence-high';
    if (confidence >= 0.7) return 'confidence-medium';
    return 'confidence-low';
}

// Export functions for use in other scripts
window.GeoVision = {
    formatCoordinates,
    formatDistance,
    formatBearing,
    getConfidenceClass,
    showAlert
};
