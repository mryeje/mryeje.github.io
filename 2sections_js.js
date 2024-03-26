// Sketchfab Viewer API: Start/Stop the viewer
var version = '1.12.1';
var uid = '4e23eadc76844c0ebf6582699c9c25b2'; // Replace with your model UID
var iframe = document.getElementById('api-frame');
var client = new window.Sketchfab(version, iframe);
var error = function error() {
    console.error('Sketchfab API error');
};

var annotationsData = []; // Store annotations data
var api; // Define api variable

var success = function success(apiInstance) {
    api = apiInstance; // Assign the api instance to the global variable
    api.start(function () {
        api.addEventListener('viewerready', function () {
            api.getAnnotationList(function (err, annotations) {
                if (!err) {
                    var annotationCount = annotations.length;
                    document.getElementById('count').textContent = annotationCount;
                    annotationsData = annotations;
                }
            });
        });
    });
};

// set zoom speed
client.init(presentationConfig, {
    success: function onSuccess(api) {
        api.start(); // Start the viewer
        api.addEventListener('viewerready', function() {
            // Access the camera controls
            var cameraControls = api.getCameraControls();

            // Set the zoom speed (adjust as needed)
            cameraControls.setZoomSpeed(0.5); // You can adjust the value to control the zoom speed
        });
    },
    error: function onError() {
        console.log('Viewer error');
    }
});

client.init(uid, {
    success: success,
    error: error,
    autostart: 0,
    preload: 1,
    max_texture_size: 512,
    transparent: 1,
    ui_watermark: 0,
    ui_infos: 0,
    ui_controls: 1,
    ui_annotations: 1,
    ui_settings: 0,
    ui_ar_qrcode: 0,
    ui_ar_help: 0,
    ui_help: 0,
    ui_ar: 0,
    ui_vr: 0,
    ui_fullscreen: 0,
    ui_inspector: 0
});

// Function to filter annotations based on search input
function filterAnnotations(api) {
    console.log('Filtering annotations...');
    var searchInput = document.getElementById('searchInput').value.toLowerCase();
    var suggestionBox = document.getElementById('suggestionBox');
    suggestionBox.innerHTML = ''; // Clear previous suggestions
    var filteredAnnotations = annotationsData.filter(function (annotation) {
        return annotation.name.toLowerCase().includes(searchInput);
    });
    filteredAnnotations.forEach(function (annotation, index) {
        var suggestionItem = document.createElement('div');
        suggestionItem.classList.add('suggestion-item');
        suggestionItem.textContent = annotation.name;
        suggestionItem.onclick = function () {
            console.log('Selected annotation:', annotation.name);
            document.getElementById('searchInput').value = annotation.name;
            suggestionBox.innerHTML = ''; // Clear suggestion box after selection
            gotoAnnotationByName(annotation.name, api); // Pass api object as an argument
            //createButton(annotation.name); // Create button corresponding to the selected annotation
        };
        suggestionBox.appendChild(suggestionItem);
    });
}

// Function to goto annotation by name
function gotoAnnotationByName(annotationName, api) {
    console.log('Navigating to annotation:', annotationName);
    var index = annotationsData.findIndex(function (annotation) {
        return annotation.name === annotationName;
    });
    if (index !== -1) {
        api.gotoAnnotation(index, { preventCameraAnimation: false, preventCameraMove: false }, function(err, index) {
            if (!err) {
                console.log('Successfully navigated to annotation:', index + 1);
            } else {
                console.error('Error navigating to annotation:', err);
            }
        });
    } else {
        console.error('Annotation not found:', annotationName);
    }
}

// Function to create a button corresponding to the annotation
function createButton(annotationName) {
    console.log('Creating button for annotation:', annotationName);
    var annotationButtons = document.getElementById('annotation-buttons');
    var button = document.createElement('button');
    button.textContent = annotationName;
    button.onclick = function () {
        console.log('Button clicked for annotation:', annotationName);
        gotoAnnotationByName(annotationName, api); // Go to the annotation when the button is clicked
    };
    annotationButtons.appendChild(button);
}

// Event listener for search input
document.getElementById('searchInput').addEventListener('input', function () {
    console.log('Search input changed.');
    filterAnnotations(api); // Pass api object as an argument
});

// GUI code for generating hide/show buttons
function initGui() {
    console.log('Initializing GUI...');
    var controls = document.getElementById('controls');
    if (!controls) {
        console.error('Controls element not found.');
        return;
    }

    var buttonsText = '';
    buttonsText += '<table style="width:100%">';
    buttonsText += '<tr>';
    buttonsText += '<th>Cabinet & Door Assembly</th>';
    buttonsText += '<th>Drum & Motor Assembly</th>';
    buttonsText += '<th>Control panel</th>';
    buttonsText += '</tr>';
    buttonsText += '<tr>';
    buttonsText += '<td><label class="switch">';
    buttonsText += '<input id="hide1" name="checkbox1" type="checkbox">';
    buttonsText += '<span class="slider round"></span>';
    buttonsText += '</label></td>';
    buttonsText += '<td><label class="switch">';
    buttonsText += '<input id="hide2" name="checkbox2" type="checkbox">';
    buttonsText += '<span class="slider round"></span>';
    buttonsText += '</label></td>';
    buttonsText += '<td><label class="switch">';
    buttonsText += '<input id="hide3" name="checkbox3" type="checkbox">';
    buttonsText += '<span class="slider round"></span>';
    buttonsText += '</label></td>';
    buttonsText += '</tr>';
    buttonsText += '</table>';

    controls.innerHTML = buttonsText;
    console.log('GUI initialized.');

    // Add event listeners for toggle switches
    var toggleSwitches = document.querySelectorAll('.switch input[type="checkbox"]');
    if (toggleSwitches.length === 0) {
        console.error('Toggle switches not found.');
        return;
    }

    toggleSwitches.forEach(function (toggle) {
        toggle.addEventListener('change', function () {
            // Reset all toggles to default except the current one
            document.querySelectorAll('.switch input[type="checkbox"]').forEach(function (otherToggle) {
                if (otherToggle !== toggle) {
                    otherToggle.checked = false;
                }
            });
			  var Cabid = 4;
			  var drumid = 972;
			  var controlpid = 291;
			  var bracketID = 794;

            // Perform the corresponding action based on the toggle
            if (toggle.checked) {
                // Toggle is checked, perform action
                var toggleId = toggle.getAttribute('id');
                var annotationId;
                switch (toggleId) {
                    case 'hide1':
                        annotationId = 4;
						api.show(Cabid);
						api.hide(drumid);
						api.hide(controlpid);
						api.hide(bracketID);
                        break;
                    case 'hide2':
                        annotationId = 972;
						api.hide(Cabid);
						api.show(drumid);
						api.hide(controlpid);
						api.hide(bracketID);
                        break;
                    case 'hide3':
                        annotationId = 291;
						api.hide(Cabid);
						api.hide(drumid);
						api.show(controlpid);
						api.hide(bracketID);
                        break;
                    default:
                        annotationId = null;
                }
                if (annotationId !== null) {
                    api.show(annotationId);
                }
            } else {
                // Toggle is unchecked, perform corresponding action (optional)
                // For example, if you want to hide the annotation when unchecked
                var toggleId = toggle.getAttribute('id');
                var annotationId;
                switch (toggleId) {
                    case 'hide1':
                        api.show(Cabid);
						api.show(drumid);
						api.show(controlpid);
						api.show(bracketID);
                        break;
                    case 'hide2':
                        annotationId = 972;
						api.show(Cabid);
						api.show(drumid);
						api.show(controlpid);
						api.show(bracketID);
                        break;
                    case 'hide3':
                        annotationId = 291;
						api.show(Cabid);
						api.show(drumid);
						api.show(controlpid);
						api.show(bracketID);
                        break;
                    default:
                        annotationId = null;
                }
                if (annotationId !== null) {
                    api.hide(annotationId);
                }
            }
        });
    });

    // Event listener for the reset view button
    var resetViewButton = document.getElementById('resetViewButton');
    if (resetViewButton) {
        resetViewButton.addEventListener('click', function () {
            // Recenter the camera
            api.recenterCamera(function (err) {
                if (!err) {
                    console.log('Camera recentered');
                } else {
                    console.error('Error recentering camera:', err);
                }
            });
        });
    } else {
        console.error('Reset view button not found.');
    }
}

// Call the function to initialize GUI
initGui();
