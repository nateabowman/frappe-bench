// Form Enhancements for Construction Management

frappe.provide("nexelya.forms");

// Initialize form enhancements
nexelya.forms.init = function() {
  // Enhance all forms on page
  nexelya.forms.enhanceFormControls();
  nexelya.forms.addPhotoUpload();
  nexelya.forms.addLocationCapture();
  nexelya.forms.addSignatureCapture();
  nexelya.forms.addAutoSave();
  nexelya.forms.addProgressIndicator();
  
  // Watch for dynamically added forms
  if (window.MutationObserver) {
    const observer = new MutationObserver(() => {
      nexelya.forms.enhanceFormControls();
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }
};

// Enhance form controls
nexelya.forms.enhanceFormControls = function() {
  // Add design system classes to form controls
  const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="number"], input[type="date"], textarea, select');
  inputs.forEach(input => {
    if (!input.classList.contains('form-control')) {
      input.classList.add('form-control');
    }
    
    // Ensure minimum height for mobile
    if (window.innerWidth <= 768) {
      input.style.minHeight = 'var(--touch-target-comfortable)';
    }
  });
  
  // Enhance labels
  const labels = document.querySelectorAll('label');
  labels.forEach(label => {
    if (!label.classList.contains('field-label')) {
      label.classList.add('field-label');
    }
  });
};

// Add photo upload functionality
nexelya.forms.addPhotoUpload = function() {
  // Find file upload fields that should support photos
  const fileFields = document.querySelectorAll('input[type="file"][data-fieldtype="Attach Image"], input[type="file"][accept*="image"]');
  
  fileFields.forEach(field => {
    if (field.dataset.nexelyaEnhanced) return;
    field.dataset.nexelyaEnhanced = 'true';
    
    // Add camera button for mobile
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const wrapper = field.closest('.form-group') || field.parentElement;
      const cameraBtn = document.createElement('button');
      cameraBtn.type = 'button';
      cameraBtn.className = 'btn btn-secondary camera-button';
      cameraBtn.innerHTML = '<i class="fa fa-camera"></i>';
      cameraBtn.title = 'Take Photo';
      cameraBtn.style.marginLeft = 'var(--spacing-sm)';
      
      cameraBtn.addEventListener('click', () => {
        nexelya.forms.capturePhoto(field);
      });
      
      wrapper.appendChild(cameraBtn);
    }
  });
};

// Capture photo from camera
nexelya.forms.capturePhoto = function(inputField) {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    frappe.show_alert({
      message: 'Camera not available on this device',
      indicator: 'orange'
    });
    return;
  }
  
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      // Create video element for preview
      const video = document.createElement('video');
      video.srcObject = stream;
      video.autoplay = true;
      video.style.width = '100%';
      video.style.maxWidth = '400px';
      video.style.borderRadius = 'var(--radius-md)';
      
      // Create modal for camera preview
      const modal = nexelya.forms.createCameraModal(video, stream, inputField);
      document.body.appendChild(modal);
    })
    .catch(err => {
      frappe.show_alert({
        message: 'Could not access camera: ' + err.message,
        indicator: 'red'
      });
    });
};

// Create camera modal
nexelya.forms.createCameraModal = function(video, stream, inputField) {
  const modal = document.createElement('div');
  modal.className = 'nexelya-camera-modal';
  modal.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 10000;
    padding: var(--spacing-lg);
  `;
  
  const container = document.createElement('div');
  container.style.cssText = 'background: white; border-radius: var(--radius-lg); padding: var(--spacing-lg); max-width: 500px; width: 100%;';
  
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  
  const captureBtn = document.createElement('button');
  captureBtn.className = 'btn btn-primary';
  captureBtn.textContent = 'Capture Photo';
  captureBtn.style.cssText = 'width: 100%; margin-top: var(--spacing-md);';
  
  const cancelBtn = document.createElement('button');
  cancelBtn.className = 'btn btn-secondary';
  cancelBtn.textContent = 'Cancel';
  cancelBtn.style.cssText = 'width: 100%; margin-top: var(--spacing-sm);';
  
  captureBtn.addEventListener('click', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);
    
    canvas.toBlob(blob => {
      const file = new File([blob], 'photo.jpg', { type: 'image/jpeg' });
      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(file);
      inputField.files = dataTransfer.files;
      
      // Trigger change event
      inputField.dispatchEvent(new Event('change', { bubbles: true }));
      
      // Stop stream and remove modal
      stream.getTracks().forEach(track => track.stop());
      modal.remove();
    }, 'image/jpeg', 0.9);
  });
  
  cancelBtn.addEventListener('click', () => {
    stream.getTracks().forEach(track => track.stop());
    modal.remove();
  });
  
  container.appendChild(video);
  container.appendChild(captureBtn);
  container.appendChild(cancelBtn);
  modal.appendChild(container);
  
  return modal;
};

// Add location capture
nexelya.forms.addLocationCapture = function() {
  // Find location-related fields
  const locationFields = document.querySelectorAll('input[data-fieldname*="location"], input[data-fieldname*="gps"], input[data-fieldname*="coordinates"]');
  
  locationFields.forEach(field => {
    if (field.dataset.nexelyaEnhanced) return;
    field.dataset.nexelyaEnhanced = 'true';
    
    const wrapper = field.closest('.form-group') || field.parentElement;
    const locationBtn = document.createElement('button');
    locationBtn.type = 'button';
    locationBtn.className = 'btn btn-secondary location-button';
    locationBtn.innerHTML = '<i class="fa fa-map-marker"></i> Get Location';
    locationBtn.style.marginLeft = 'var(--spacing-sm)';
    
    locationBtn.addEventListener('click', () => {
      nexelya.forms.captureLocation(field);
    });
    
    wrapper.appendChild(locationBtn);
  });
};

// Capture GPS location
nexelya.forms.captureLocation = function(inputField) {
  if (!navigator.geolocation) {
    frappe.show_alert({
      message: 'Geolocation not supported',
      indicator: 'orange'
    });
    return;
  }
  
  locationBtn.disabled = true;
  locationBtn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Getting Location...';
  
  navigator.geolocation.getCurrentPosition(
    position => {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;
      inputField.value = `${lat}, ${lng}`;
      inputField.dispatchEvent(new Event('change', { bubbles: true }));
      
      locationBtn.disabled = false;
      locationBtn.innerHTML = '<i class="fa fa-map-marker"></i> Get Location';
      
      frappe.show_alert({
        message: 'Location captured',
        indicator: 'green'
      });
    },
    error => {
      frappe.show_alert({
        message: 'Could not get location: ' + error.message,
        indicator: 'red'
      });
      
      locationBtn.disabled = false;
      locationBtn.innerHTML = '<i class="fa fa-map-marker"></i> Get Location';
    }
  );
};

// Add signature capture (placeholder - would need signature pad library)
nexelya.forms.addSignatureCapture = function() {
  // This would integrate with a signature pad library
  // For now, just mark signature fields
  const signatureFields = document.querySelectorAll('input[data-fieldname*="signature"], textarea[data-fieldname*="signature"]');
  signatureFields.forEach(field => {
    field.closest('.form-group')?.classList.add('signature-field');
  });
};

// Add auto-save functionality
nexelya.forms.addAutoSave = function() {
  let autoSaveTimer;
  const forms = document.querySelectorAll('form[data-doctype]');
  
  forms.forEach(form => {
    const inputs = form.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
      input.addEventListener('input', () => {
        clearTimeout(autoSaveTimer);
        autoSaveTimer = setTimeout(() => {
          nexelya.forms.autoSaveForm(form);
        }, 2000); // Auto-save after 2 seconds of inactivity
      });
    });
  });
};

// Auto-save form data
nexelya.forms.autoSaveForm = function(form) {
  // This would save to localStorage or send to server
  const formData = new FormData(form);
  const data = {};
  for (let [key, value] of formData.entries()) {
    data[key] = value;
  }
  
  // Save to localStorage
  const doctype = form.dataset.doctype;
  const name = form.dataset.name || 'new';
  localStorage.setItem(`nexelya_autosave_${doctype}_${name}`, JSON.stringify(data));
  
  // Show auto-save indicator
  nexelya.forms.showAutoSaveIndicator();
};

// Show auto-save indicator
nexelya.forms.showAutoSaveIndicator = function() {
  let indicator = document.querySelector('.nexelya-autosave-indicator');
  if (!indicator) {
    indicator = document.createElement('div');
    indicator.className = 'nexelya-autosave-indicator';
    indicator.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: var(--nexelya-success);
      color: white;
      padding: var(--spacing-sm) var(--spacing-md);
      border-radius: var(--radius-full);
      font-size: var(--font-size-sm);
      z-index: 1000;
      opacity: 0;
      transition: opacity var(--transition-base);
    `;
    indicator.textContent = 'Saved';
    document.body.appendChild(indicator);
  }
  
  indicator.style.opacity = '1';
  setTimeout(() => {
    indicator.style.opacity = '0';
  }, 2000);
};

// Add progress indicator for multi-step forms
nexelya.forms.addProgressIndicator = function() {
  const multiStepForms = document.querySelectorAll('form[data-steps]');
  
  multiStepForms.forEach(form => {
    const steps = parseInt(form.dataset.steps) || 0;
    if (steps > 1) {
      const progressBar = document.createElement('div');
      progressBar.className = 'nexelya-form-progress';
      progressBar.style.cssText = `
        margin-bottom: var(--spacing-lg);
        padding: var(--spacing-md);
        background: var(--bg-secondary);
        border-radius: var(--radius-md);
      `;
      
      const progress = document.createElement('div');
      progress.className = 'progress progress-lg';
      
      const progressBarInner = document.createElement('div');
      progressBarInner.className = 'progress-bar';
      progressBarInner.style.width = '0%';
      
      progress.appendChild(progressBarInner);
      progressBar.appendChild(progress);
      
      form.insertBefore(progressBar, form.firstChild);
      
      // Update progress based on filled fields
      const updateProgress = () => {
        const inputs = form.querySelectorAll('input, textarea, select');
        const filled = Array.from(inputs).filter(i => i.value && i.value.trim()).length;
        const percentage = (filled / inputs.length) * 100;
        progressBarInner.style.width = percentage + '%';
      };
      
      form.querySelectorAll('input, textarea, select').forEach(input => {
        input.addEventListener('input', updateProgress);
      });
      
      updateProgress();
    }
  });
};

// Initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', nexelya.forms.init);
} else {
  nexelya.forms.init();
}

// Also initialize when forms are loaded dynamically
if (frappe.router) {
  frappe.router.on("change", () => {
    setTimeout(nexelya.forms.init, 500);
  });
}

