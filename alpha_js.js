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
                    //document.getElementById('count').textContent = annotationCount;
                    annotationsData = annotations;
                }
            });
        });
    });
};

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


// Function to show a specific annotation based on index
function showSpecificAnnotation(api, annotationIndex, option) {
    // Define the allowedIndices arrays for each possibility
    var allowedIndices = [];
    switch (option) {
        case 1:
            allowedIndices = [23, 24, 25, 26, 27, 28];
            break;
        case 2:
            allowedIndices =  [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18];
            break;
        case 3:
            allowedIndices = [19, 20, 21, 22, 25, 29];
            break;
        default:
            console.error('Invalid option:', option);
            return; // Exit the function if the option is invalid
    }

    // Ensure that annotationIndex is a valid number
    if (isNaN(annotationIndex) || annotationIndex < 0 || annotationIndex >= allowedIndices.length) {
        console.error('Invalid annotation index:', annotationIndex);
        return;
    }

    // Check if the api object is defined and has the showAnnotation method
    if (!api || typeof api.showAnnotation !== 'function') {
        console.error('Sketchfab API is not properly initialized or does not support showAnnotation method.');
        return;
    }

    // Get the actual annotation index from the allowedIndices array
    var actualIndex = allowedIndices[annotationIndex];

    // Hide all annotations except the specified index and allowed indices
    for (var i = 0; i < 50; i++) { // Assuming there are 50 annotations in total
        if (i !== actualIndex && !allowedIndices.includes(i)) {
            api.hideAnnotation(i);
        }
    }

    // Show the specified annotation if it's a valid index
    if (!isNaN(actualIndex)) {
        api.showAnnotation(actualIndex, function(err, index) {
            if (!err) {
                console.log('Showing annotation', actualIndex + 1);
            } else {
                console.error('Error showing annotation:', err);
                // Log the error without interrupting the page execution
                setTimeout(function() {
                    console.error('Annotation error:', err);
                }, 0);
            }
        });
    } else {
        console.error('Invalid annotation index:', annotationIndex);
    }
}



// Function to show all annotations
function showAllAnnotations(api) {
    for (var i = 0; i < 50; i++) { // Assuming there are 50 annotations in total
        api.showAnnotation(i, function(err, index) {
            if (!err) {
                console.log('Showing annotation', index + 1);
            } else {
                console.error('Error showing annotation:', err);
            }
        });
    }
}


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
					showAllAnnotations(api);
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
						showSpecificAnnotation(api, 0,1);
                        break;
                    case 'hide2':
                        annotationId = 972;
						api.hide(Cabid);
						api.show(drumid);
						api.hide(controlpid);
						api.hide(bracketID);
						showSpecificAnnotation(api, 0,2);
                        break;
                    case 'hide3':
                        annotationId = 291;
						api.hide(Cabid);
						api.hide(drumid);
						api.show(controlpid);
						api.hide(bracketID);
						showSpecificAnnotation(api, 0,3);
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
						showAllAnnotations(api)
                        break;
                    case 'hide2':
                        annotationId = 972;
						api.show(Cabid);
						api.show(drumid);
						api.show(controlpid);
						api.show(bracketID);
						showAllAnnotations(api)
                        break;
                    case 'hide3':
                        annotationId = 291;
						api.show(Cabid);
						api.show(drumid);
						api.show(controlpid);
						api.show(bracketID);
						showAllAnnotations(api)
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
