// Sketchfab Viewer API: Start/Stop the viewer
var version = '1.12.1';
var uid = '4e23eadc76844c0ebf6582699c9c25b2'; // Replace with your model UID
var iframe = document.getElementById('api-frame');
var client = new window.Sketchfab(version, iframe);
var error = function error() {
    console.error('Sketchfab API error');
};

var annotationsData = []; // Store annotations data
var api; // Variable to store the Sketchfab API instance

var success = function success(sketchfabApi) {
    api = sketchfabApi;
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
function filterAnnotations() {
    var searchInput = document.getElementById('searchInput').value.toLowerCase();
    var suggestionBox = document.getElementById('suggestionBox');
    suggestionBox.innerHTML = ''; // Clear previous suggestions
    var suggestions = annotationsData.filter(function (annotation) {
        return annotation.name.toLowerCase().includes(searchInput);
    });
    suggestions.forEach(function (annotation) {
        var suggestionItem = document.createElement('div');
        suggestionItem.classList.add('suggestion-item');
        suggestionItem.textContent = annotation.name;
        suggestionItem.onclick = function () {
            document.getElementById('searchInput').value = annotation.name;
            suggestionBox.innerHTML = ''; // Clear suggestion box after selection
            showAnnotationByName(annotation.name);
        };
        suggestionBox.appendChild(suggestionItem);
    });
}

// Function to show annotation by name
function showAnnotationByName(annotationName) {
    var index = annotationsData.findIndex(function (annotation) {
        return annotation.name === annotationName;
    });
    if (index !== -1) {
        api.showAnnotation(index);
        createButton(annotationName); // Create a button corresponding to the annotation
    }
}

// Function to create a button corresponding to the annotation
function createButton(annotationName) {
    var annotationButtons = document.getElementById('annotation-buttons');
    var button = document.createElement('button');
    button.textContent = annotationName;
    button.onclick = function () {
        showAnnotationByName(annotationName); // Show the annotation when the button is clicked
    };
    annotationButtons.appendChild(button);
}

// Event listener for search input
document.getElementById('searchInput').addEventListener('input', function () {
    filterAnnotations();
});

// GUI code for generating hide/show buttons
function initGui() {
    var controls = document.getElementById('controls');
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
}

// Call the function to initialize GUI
initGui();

// Event listeners for original hide/show buttons
document.getElementById('hide1').addEventListener('change', function () {
    var id = 4;
    if (this.checked) {
        api.show(id);
    } else {
        api.hide(id);
    }
});

document.getElementById('hide2').addEventListener('change', function () {
    var drumid = 972;
    if (this.checked) {
        api.show(drumid);
    } else {
        api.hide(drumid);
    }
});

document.getElementById('hide3').addEventListener('change', function () {
    var controlpid = 291;
    if (this.checked) {
        api.show(controlpid);
    } else {
        api.hide(controlpid);
    }
});