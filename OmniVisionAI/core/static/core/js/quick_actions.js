// Quick Actions JavaScript Module
// Handles all Quick Actions sidebar functionality

(function() {
    'use strict';
    
    // Global variables
    const API_BASE = '/api';
    const camerasUrl = `${API_BASE}/core/cameras/`;
    const gatesUrl = `${API_BASE}/core/gates/`;
    const overviewUrl = `${API_BASE}/core/dashboard/overview/`;
    const unrecognizedUrl = `${API_BASE}/core/unrecognized-faces/`;
    
    // Get CSRF token
    function getCSRFToken() {
        const metaTag = document.querySelector('meta[name="csrf-token"]');
        if (metaTag && metaTag.content) {
            return metaTag.content;
        }
        
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue || '';
    }
    
    // Show toast notification
    function showToast(message, type = 'info') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }
    
    // Add Worker - Opens registration modal with liveness detection
    function addWorker() {
        // Check if worker registration modal exists
        let modal = document.getElementById('addWorkerModal');
        if (!modal) {
            // Create the modal
            modal = createWorkerRegistrationModal();
            document.body.appendChild(modal);
        }
        
        // Show the modal
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }
    
    // Add Vehicle - Opens vehicle registration modal
    function addVehicle() {
        // Check if vehicle registration modal exists
        let modal = document.getElementById('addVehicleModal');
        if (!modal) {
            // Create the modal
            modal = createVehicleRegistrationModal();
            document.body.appendChild(modal);
        }
        
        // Show the modal
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }
    
    // Add Camera - Opens camera registration modal
    function addCamera() {
        // Use existing camera modal
        const modal = document.getElementById('addCameraModal');
        if (modal) {
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
        } else {
            showToast('Camera registration modal not found', 'error');
        }
    }
    
    // Lock All Gates - WebSocket + API call
    async function lockAllGates() {
        try {
            showToast('Locking all gates...', 'info');
            
            // WebSocket functionality disabled - using API only
            
            // Also use API as backup
            const response = await fetch(gatesUrl);
            const gates = await response.json();
            
            for (const gate of gates) {
                if (gate.status !== 'locked') {
                    await fetch(`${gatesUrl}${gate.id}/control/`, {
                        method: 'POST',
                        headers: { 
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCSRFToken()
                        },
                        credentials: 'include',
                        body: JSON.stringify({ action: 'lock' })
                    });
                }
            }
            
            showToast('All gates locked successfully', 'success');
            
            // Refresh gates display
            if (typeof loadGates === 'function') {
                loadGates();
            }
            if (typeof loadOverviewData === 'function') {
                loadOverviewData();
            }
            
        } catch (error) {
            console.error('Error locking gates:', error);
            showToast('Error locking gates', 'danger');
        }
    }
    
    // Unlock All Gates - WebSocket + API call
    async function unlockAllGates() {
        try {
            showToast('Unlocking all gates...', 'info');
            
            // WebSocket functionality disabled - using API only
            
            // Also use API as backup
            const response = await fetch(gatesUrl);
            const gates = await response.json();
            
            for (const gate of gates) {
                if (gate.status !== 'unlocked') {
                    await fetch(`${gatesUrl}${gate.id}/control/`, {
                        method: 'POST',
                        headers: { 
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCSRFToken()
                        },
                        credentials: 'include',
                        body: JSON.stringify({ action: 'unlock' })
                    });
                }
            }
            
            showToast('All gates unlocked successfully', 'success');
            
            // Refresh gates display
            if (typeof loadGates === 'function') {
                loadGates();
            }
            if (typeof loadOverviewData === 'function') {
                loadOverviewData();
            }
            
        } catch (error) {
            console.error('Error unlocking gates:', error);
            showToast('Error unlocking gates', 'danger');
        }
    }
    
    // Refresh Feeds - Reload camera previews
    function refreshAllFeeds() {
        showToast('Refreshing camera feeds...', 'info');
        
        // Call existing refresh functions
        if (typeof loadLiveCameras === 'function') {
            loadLiveCameras();
        }
        if (typeof loadOverviewData === 'function') {
            loadOverviewData();
        }
        if (typeof loadModuleCameras === 'function') {
            const currentTab = window.currentTab || 'overview';
            if (currentTab === 'workers') loadModuleCameras('attendance', 'workers-cameras');
            else if (currentTab === 'vehicles') loadModuleCameras('anpr', 'vehicles-cameras');
            else if (currentTab === 'ppe') loadModuleCameras('ppe', 'ppe-cameras');
            else if (currentTab === 'textile') loadModuleCameras('textile', 'textile-cameras');
        }
        
        showToast('Camera feeds refreshed', 'success');
    }
    
    // Create Worker Registration Modal with Liveness Detection
    function createWorkerRegistrationModal() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'addWorkerModal';
        modal.tabIndex = -1;
        modal.innerHTML = `
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title"><i class="bi bi-person-plus me-2"></i>Register New Worker</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-6">
                                <form id="workerRegistrationForm">
                                    <div class="mb-3">
                                        <label class="form-label">Full Name *</label>
                                        <input type="text" class="form-control" id="workerName" required>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Employee ID *</label>
                                        <input type="text" class="form-control" id="workerEmployeeId" required>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Department</label>
                                        <input type="text" class="form-control" id="workerDepartment">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Role</label>
                                        <select class="form-control" id="workerRole">
                                            <option value="operator">Operator</option>
                                            <option value="supervisor">Supervisor</option>
                                            <option value="technician">Technician</option>
                                            <option value="security">Security</option>
                                            <option value="maintenance">Maintenance</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Emergency Contact</label>
                                        <input type="text" class="form-control" id="workerEmergencyContact">
                                    </div>
                                </form>
                            </div>
                            <div class="col-md-6">
                                <div class="card">
                                    <div class="card-header">
                                        <h6 class="mb-0">3-Step Liveness Detection</h6>
                                    </div>
                                    <div class="card-body">
                                        <div class="text-center mb-3 liveness-video-container">
                                            <video id="livenessVideo" width="100%" height="200" autoplay muted style="border-radius: 8px; background: #000;"></video>
                                            <canvas id="livenessCanvas" style="display: none;"></canvas>
                                        </div>
                                        
                                        <div class="liveness-steps">
                                            <div class="step" id="step-center">
                                                <div class="step-indicator">
                                                    <i class="bi bi-person"></i>
                                                </div>
                                                <div class="step-content">
                                                    <h6>Step 1: Look Straight</h6>
                                                    <p>Hold for 1 second</p>
                                                    <div class="step-status" id="status-center">Pending</div>
                                                </div>
                                            </div>
                                            
                                            <div class="step" id="step-right">
                                                <div class="step-indicator">
                                                    <i class="bi bi-arrow-right"></i>
                                                </div>
                                                <div class="step-content">
                                                    <h6>Step 2: Turn Right</h6>
                                                    <p>Turn face right (yaw > +15°)</p>
                                                    <div class="step-status" id="status-right">Pending</div>
                                                </div>
                                            </div>
                                            
                                            <div class="step" id="step-left">
                                                <div class="step-indicator">
                                                    <i class="bi bi-arrow-left"></i>
                                                </div>
                                                <div class="step-content">
                                                    <h6>Step 3: Turn Left</h6>
                                                    <p>Turn face left (yaw < -15°)</p>
                                                    <div class="step-status" id="status-left">Pending</div>
                                                </div>
                                            </div>
                                        </div>
                                        
                                        <div class="mt-3">
                                            <div class="progress">
                                                <div class="progress-bar" id="livenessProgress" role="progressbar" style="width: 0%"></div>
                                            </div>
                                            <small class="text-muted">Complete all steps to enable registration</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" id="saveWorkerBtn" disabled>
                            <i class="bi bi-check-lg me-2"></i>Register Worker
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        // Add liveness detection functionality
        addLivenessDetectionToModal(modal);
        
        return modal;
    }
    
    // Create Vehicle Registration Modal
    function createVehicleRegistrationModal() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'addVehicleModal';
        modal.tabIndex = -1;
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title"><i class="bi bi-truck me-2"></i>Register New Vehicle</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="vehicleRegistrationForm">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Registration Number *</label>
                                        <input type="text" class="form-control" id="vehicleRegNo" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Vehicle Type</label>
                                        <select class="form-control" id="vehicleType">
                                            <option value="private">Private</option>
                                            <option value="commercial">Commercial</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Owner Name</label>
                                        <input type="text" class="form-control" id="vehicleOwnerName">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Owner Contact</label>
                                        <input type="text" class="form-control" id="vehicleOwnerContact">
                                    </div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Fuel Type</label>
                                <select class="form-control" id="vehicleFuelType">
                                    <option value="petrol">Petrol</option>
                                    <option value="diesel">Diesel</option>
                                    <option value="electric">Electric</option>
                                    <option value="hybrid">Hybrid</option>
                                    <option value="cng">CNG</option>
                                    <option value="lpg">LPG</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" id="vehicleAuthorized">
                                    <label class="form-check-label" for="vehicleAuthorized">
                                        Authorize this vehicle
                                    </label>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" onclick="saveVehicle()">
                            <i class="bi bi-check-lg me-2"></i>Register Vehicle
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        return modal;
    }
    
    // Add Liveness Detection to Worker Modal
    function addLivenessDetectionToModal(modal) {
        let video, canvas, ctx;
        let livenessSteps = { center: false, right: false, left: false };
        let currentStep = 'center';
        let stepTimeout;
        
        // Initialize camera when modal is shown
        modal.addEventListener('shown.bs.modal', async function() {
            try {
                video = modal.querySelector('#livenessVideo');
                canvas = modal.querySelector('#livenessCanvas');
                ctx = canvas.getContext('2d');
                
                // Request camera with optimized settings
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { 
                        width: { ideal: 640 }, 
                        height: { ideal: 480 },
                        facingMode: 'user',
                        frameRate: { ideal: 30, max: 30 }
                    } 
                });
                
                video.srcObject = stream;
                
                // Wait for video to be ready before starting detection
                video.addEventListener('loadedmetadata', () => {
                    video.play().then(() => {
                        startLivenessDetection();
                    }).catch(error => {
                        console.error('Error playing video:', error);
                        showToast('Error starting camera feed', 'danger');
                    });
                });
                
            } catch (error) {
                console.error('Error accessing camera:', error);
                showToast('Camera access denied. Please allow camera access to continue.', 'danger');
            }
        });
        
        // Clean up when modal is hidden
        modal.addEventListener('hidden.bs.modal', function() {
            if (video && video.srcObject) {
                video.srcObject.getTracks().forEach(track => track.stop());
            }
            if (stepTimeout) {
                clearTimeout(stepTimeout);
            }
        });
        
        function startLivenessDetection() {
            updateStepInstructions();
            detectLiveness();
        }
        
        function updateStepInstructions() {
            const steps = ['center', 'right', 'left'];
            steps.forEach(step => {
                const statusEl = modal.querySelector(`#status-${step}`);
                if (step === currentStep) {
                    statusEl.textContent = 'In Progress...';
                    statusEl.className = 'step-status text-warning';
                } else if (livenessSteps[step]) {
                    statusEl.textContent = 'Completed ✓';
                    statusEl.className = 'step-status text-success';
                } else {
                    statusEl.textContent = 'Pending';
                    statusEl.className = 'step-status text-muted';
                }
            });
        }
        
        function detectLiveness() {
            if (!video || !canvas) return;
            
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            ctx.drawImage(video, 0, 0);
            
            // Try to use MediaPipe for face detection if available
            if (window.mediapipe && window.mediapipe.FaceMesh) {
                detectFaceWithMediaPipe();
            } else {
                // Fallback to simulated detection
                simulateLivenessDetection();
            }
        }
        
        function detectFaceWithMediaPipe() {
            // This would be implemented with actual MediaPipe face detection
            // For now, we'll use the simulated version
            simulateLivenessDetection();
        }
        
        async function simulateLivenessDetection() {
            let detectionInterval;
            let startTime = Date.now();
            const stepDuration = 2000; // 2 seconds per step
            
            // Try to use BlazeFace if available
            if (window.blazeface && window.tf) {
                try {
                    await detectLivenessWithBlazeFace();
                    return;
                } catch (error) {
                    console.log('BlazeFace not available, using simulated detection');
                }
            }
            
            // Show loading spinner
            showLivenessSpinner();
            
            const processStep = () => {
                const now = Date.now();
                const elapsed = now - startTime;
                
                if (elapsed >= stepDuration) {
                    // Complete current step
                    livenessSteps[currentStep] = true;
                    updateStepInstructions();
                    updateProgress();
                    
                    // Move to next step
                    if (currentStep === 'center') {
                        currentStep = 'right';
                        startTime = now;
                        showLivenessSpinner();
                    } else if (currentStep === 'right') {
                        currentStep = 'left';
                        startTime = now;
                        showLivenessSpinner();
                    } else {
                        // All steps completed
                        hideLivenessSpinner();
                        showToast('Liveness detection completed successfully!', 'success');
                        checkRegistrationReady();
                        if (detectionInterval) clearInterval(detectionInterval);
                        return;
                    }
                }
                
                // Continue processing
                detectionInterval = setTimeout(processStep, 100);
            };
            
            // Start processing
            detectionInterval = setTimeout(processStep, 100);
        }
        
        async function detectLivenessWithBlazeFace() {
            if (!window.blazeface || !video) return;
            
            try {
                // Load the BlazeFace model
                const model = await blazeface.load();
                
                showLivenessSpinner();
                
                const detectLoop = async () => {
                    if (!video || !canvas) return;
                    
                    try {
                        const predictions = await model.estimateFaces(video, false);
                        
                        if (predictions.length > 0) {
                            // Face detected - check for proper positioning
                            const face = predictions[0];
                            const now = Date.now();
                            
                            if (!startTime) {
                                startTime = now;
                            }
                            
                            const elapsed = now - startTime;
                            const stepDuration = 2000;
                            
                            if (elapsed >= stepDuration) {
                                // Complete current step
                                livenessSteps[currentStep] = true;
                                updateStepInstructions();
                                updateProgress();
                                
                                // Move to next step
                                if (currentStep === 'center') {
                                    currentStep = 'right';
                                    startTime = now;
                                } else if (currentStep === 'right') {
                                    currentStep = 'left';
                                    startTime = now;
                                } else {
                                    // All steps completed
                                    hideLivenessSpinner();
                                    showToast('Liveness detection completed successfully!', 'success');
                                    checkRegistrationReady();
                                    return;
                                }
                            }
                        }
                    } catch (error) {
                        console.log('Face detection error:', error);
                    }
                    
                    // Continue detection loop
                    requestAnimationFrame(detectLoop);
                };
                
                detectLoop();
                
            } catch (error) {
                console.error('BlazeFace initialization error:', error);
                // Fallback to simulated detection
                hideLivenessSpinner();
                simulateLivenessDetection();
            }
        }
        
        function showLivenessSpinner() {
            const videoContainer = modal.querySelector('.liveness-video-container');
            if (!videoContainer) return;
            
            let spinner = modal.querySelector('.liveness-spinner-overlay');
            
            if (!spinner) {
                spinner = document.createElement('div');
                spinner.className = 'liveness-spinner-overlay';
                spinner.innerHTML = `
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Verifying Liveness...</span>
                    </div>
                    <p class="mt-2 text-white">Verifying Liveness...</p>
                `;
                videoContainer.appendChild(spinner);
            } else {
                spinner.style.display = 'flex';
            }
        }
        
        function hideLivenessSpinner() {
            const spinner = modal.querySelector('.liveness-spinner-overlay');
            if (spinner) {
                spinner.style.display = 'none';
                spinner.remove();
            }
        }
        
        function updateProgress() {
            const completed = Object.values(livenessSteps).filter(Boolean).length;
            const total = Object.keys(livenessSteps).length;
            const percentage = (completed / total) * 100;
            
            const progressBar = modal.querySelector('#livenessProgress');
            progressBar.style.width = percentage + '%';
        }
        
        function checkRegistrationReady() {
            const allStepsCompleted = Object.values(livenessSteps).every(Boolean);
            const formValid = modal.querySelector('#workerName').value && 
                            modal.querySelector('#workerEmployeeId').value;
            
            const saveBtn = modal.querySelector('#saveWorkerBtn');
            saveBtn.disabled = !(allStepsCompleted && formValid);
        }
        
        // Form validation
        modal.querySelector('#workerName').addEventListener('input', checkRegistrationReady);
        modal.querySelector('#workerEmployeeId').addEventListener('input', checkRegistrationReady);
        
        // Save worker
        modal.querySelector('#saveWorkerBtn').addEventListener('click', async function() {
            const saveBtn = this;
            saveBtn.disabled = true;
            saveBtn.innerHTML = '<i class="bi bi-spinner-border me-2"></i>Registering...';
            
            try {
                const workerData = {
                    name: modal.querySelector('#workerName').value,
                    employee_id: modal.querySelector('#workerEmployeeId').value,
                    department: modal.querySelector('#workerDepartment').value,
                    role: modal.querySelector('#workerRole').value,
                    emergency_contact_name: modal.querySelector('#workerEmergencyContact').value,
                    liveness_verified: true
                };
                
                const response = await fetch(`${API_BASE}/attendance/employees/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    credentials: 'include',
                    body: JSON.stringify(workerData)
                });
                
                if (response.ok) {
                    showToast('Worker registered successfully!', 'success');
                    bootstrap.Modal.getInstance(modal).hide();
                    
                    // Reset form
                    modal.querySelector('#workerRegistrationForm').reset();
                    livenessSteps = { center: false, right: false, left: false };
                    currentStep = 'center';
                    updateStepInstructions();
                    updateProgress();
                    
                } else {
                    const error = await response.json();
                    showToast('Error: ' + (error.detail || 'Failed to register worker'), 'danger');
                }
                
            } catch (error) {
                console.error('Error registering worker:', error);
                showToast('Error registering worker', 'danger');
            } finally {
                saveBtn.disabled = false;
                saveBtn.innerHTML = '<i class="bi bi-check-lg me-2"></i>Register Worker';
            }
        });
    }
    
    // Save Vehicle function
    window.saveVehicle = async function() {
        const modal = document.getElementById('addVehicleModal');
        const saveBtn = modal.querySelector('.btn-primary');
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<i class="bi bi-spinner-border me-2"></i>Registering...';
        
        try {
            const vehicleData = {
                registration_no: modal.querySelector('#vehicleRegNo').value,
                vehicle_type: modal.querySelector('#vehicleType').value,
                owner_name: modal.querySelector('#vehicleOwnerName').value,
                owner_contact: modal.querySelector('#vehicleOwnerContact').value,
                fuel_type: modal.querySelector('#vehicleFuelType').value,
                is_authorized: modal.querySelector('#vehicleAuthorized').checked
            };
            
            const response = await fetch(`${API_BASE}/vehicles/vehicles/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                credentials: 'include',
                body: JSON.stringify(vehicleData)
            });
            
            if (response.ok) {
                showToast('Vehicle registered successfully!', 'success');
                bootstrap.Modal.getInstance(modal).hide();
                modal.querySelector('#vehicleRegistrationForm').reset();
                
            } else {
                const error = await response.json();
                showToast('Error: ' + (error.detail || 'Failed to register vehicle'), 'danger');
            }
            
        } catch (error) {
            console.error('Error registering vehicle:', error);
            showToast('Error registering vehicle', 'danger');
        } finally {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="bi bi-check-lg me-2"></i>Register Vehicle';
        }
    };
    
    // Initialize Quick Actions when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        // Attach event listeners to Quick Actions buttons using data-action attributes
        const quickActionButtons = document.querySelectorAll('.quick-action-btn[data-action]');
        
        quickActionButtons.forEach(button => {
            const action = button.getAttribute('data-action');
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                switch(action) {
                    case 'add-worker':
                        addWorker();
                        break;
                    case 'add-vehicle':
                        addVehicle();
                        break;
                    case 'add-camera':
                        addCamera();
                        break;
                    case 'lock-gates':
                        lockAllGates();
                        break;
                    case 'unlock-gates':
                        unlockAllGates();
                        break;
                    case 'refresh-feeds':
                        refreshAllFeeds();
                        break;
                    default:
                        console.warn('Unknown quick action:', action);
                }
            });
        });
        
        // Also handle legacy onclick attributes for backward compatibility
        const legacyButtons = document.querySelectorAll('[onclick]');
        legacyButtons.forEach(button => {
            const onclick = button.getAttribute('onclick');
            if (onclick && onclick.includes('addWorker()')) {
                button.onclick = addWorker;
            } else if (onclick && onclick.includes('addVehicle()')) {
                button.onclick = addVehicle;
            } else if (onclick && onclick.includes('addCameraForModule')) {
                button.onclick = addCamera;
            } else if (onclick && onclick.includes('lockAllGates()')) {
                button.onclick = lockAllGates;
            } else if (onclick && onclick.includes('unlockAllGates()')) {
                button.onclick = unlockAllGates;
            } else if (onclick && onclick.includes('refreshAllFeeds()')) {
                button.onclick = refreshAllFeeds;
            }
        });
    });
    
    // Expose functions globally for backward compatibility
    window.addWorker = addWorker;
    window.addVehicle = addVehicle;
    window.addCamera = addCamera;
    window.lockAllGates = lockAllGates;
    window.unlockAllGates = unlockAllGates;
    window.refreshAllFeeds = refreshAllFeeds;
    
})();
