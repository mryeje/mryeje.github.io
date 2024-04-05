import tkinter as tk
from tkinter import filedialog
import webbrowser
import os
import json  # Add this line to import the json module

def load_and_parse_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not filepath:
        return

    model_id = os.path.splitext(os.path.basename(filepath))[0]
    model_data = parse_file(filepath)
    generated_html = generate_html(model_id, model_data)
    html_text.delete("1.0", tk.END)
    html_text.insert(tk.END, generated_html)

def parse_file(filepath):
    model_data = {}
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                part_name = parts[0].strip()
                vertices = [int(v.strip()) for v in parts[1].split(',')]
                model_data[part_name] = vertices
    return model_data
def generate_html(model_id, model_data):
    # Construct JavaScript code for hiding/showing parts and annotation search
    js_code = """
    // Hide Function
    function hideout(item, index) {
        api.hide(item);
    }

    // Show Function
    function showdown(item, index) {
        api.show(item);
    }

    // Parts data
    var parts = {};

    // Function to populate the dropdown menu
    function populateDropdown() {
        var select = document.getElementById("partSelect");

        // Clear existing options
        select.innerHTML = "";

        // Create an option for each part
        var optionAll = document.createElement("option");
        optionAll.text = "All Parts";
        optionAll.value = "All Parts";
        select.add(optionAll);

        for (var part in parts) {
            var option = document.createElement("option");
            option.text = part;
            option.value = part;
            select.add(option);
        }
    }

    // Function to filter annotations based on search input and display limited number of suggestions
function filterAnnotations(api, annotationsData) {
    console.log('Filtering annotations...');
    var searchInput = document.getElementById('searchInput');
    var suggestionBox = document.getElementById('suggestionBox');

    // Function to handle displaying suggestions
    function displaySuggestions(filteredAnnotations) {
        // Clear previous suggestions
        suggestionBox.innerHTML = '';

        // Limit the number of suggestions to display
        const maxSuggestions = 5; // For example, limit to 5 suggestions

        // Display limited number of suggestions
        filteredAnnotations.slice(0, maxSuggestions).forEach(function(annotation, index) {
            var suggestionItem = document.createElement('div');
            suggestionItem.classList.add('suggestion-item');
            suggestionItem.textContent = annotation.name;
            suggestionItem.onclick = function() {
                console.log('Selected annotation:', annotation.name);
                searchInput.value = annotation.name;
                suggestionBox.innerHTML = ''; // Clear suggestion box after selection
                navigateToAnnotation(annotation.name); // Navigate to the selected annotation
            };
            suggestionBox.appendChild(suggestionItem);
        });
    }

    // Improved event listener for search input change to support continuous search
    searchInput.addEventListener('input', function() {
        var searchValue = this.value.toLowerCase();
        var filteredAnnotations = annotationsData.filter(function(annotation) {
            return annotation.name.toLowerCase().includes(searchValue);
        });

        displaySuggestions(filteredAnnotations);
    });
}


    // Function to navigate to the annotation
    function navigateToAnnotation(annotationName) {
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

    // Success function to handle Sketchfab API initialization
    var success = function success(apiInstance) {
        api = apiInstance; // Assign the api instance to the global variable
        api.start(function () {
            api.addEventListener('viewerready', function () {
                api.getAnnotationList(function (err, annotations) {
                    if (!err) {
                        var annotationCount = annotations.length;
                        annotationsData = annotations;
                        filterAnnotations(api, annotations);
                    } else {
                        console.error('Error fetching annotations data:', err);
                    }
                });
            });
        });
    };
    
    

    // Populate the dropdown menu on page load
    window.onload = function() {
        populateDropdown();

        // Initialize the Sketchfab API and handle success
        var iframe = document.getElementById("api-frame");
        var uid = '""" + model_id + """';
        var client = new Sketchfab(iframe);
        client.init(uid, {
            success: success,
            error: function (err) {
                console.error('Sketchfab API error:', err);
            },
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
    };

    // Event listener for dropdown change
    document.getElementById("partSelect").addEventListener("change", function() {
        var selectedPart = this.value;
        if (selectedPart === "All Parts") {
            api.show();
        } else {
            api.hide();
            parts[selectedPart].forEach(hideout);
            
        }
    });

    // Event listener for hide button
    document.getElementById("hideButton").addEventListener("click", function() {
        var selectedPart = document.getElementById("partSelect").value;
        if (selectedPart !== "All Parts") {
            api.hide();
            showSpecificAnnotation(api, 0,1);
            console.log(selectedPart);
            parts[selectedPart].forEach(hideout);
            switch (selectedPart) {
                    case 'Fridge door':
                        showSpecificAnnotation(api, 0,1);
                        break;
                    case 'Freezer Door':
                      showSpecificAnnotation(api, 0,2);
                        break;
                    case 'Refrigeration Unit':
                        showSpecificAnnotation(api, 0,3);
                        break;
                    default:
                         console.log(selectedPart);}
        }
    });

    // Event listener for show button
    document.getElementById("showButton").addEventListener("click", function() {
        var selectedPart = document.getElementById("partSelect").value;
        if (selectedPart !== "All Parts") {
            api.show();
            showAllAnnotations(api);
            parts[selectedPart].forEach(showdown);
        }
    });

    // Reset view button event listener
    document.getElementById('resetViewButton').addEventListener('click', function() {
        var selectedPart = document.getElementById("partSelect").value;
        api.recenterCamera(function(err) {
            if (!err) {
                console.log('Camera recentered');
                showAllAnnotations(api);
                parts[selectedPart].forEach(showdown);
            } else {
                console.error('Error recentering camera:', err);
            }
        });
    });
    
    // Function to show a specific annotation based on index
function showSpecificAnnotation(api, annotationIndex, option) {
    // Define the allowedIndices arrays for each possibility
    var allowedIndices = [];
    switch (option) {
   case 1:
            allowedIndices = [2,3,4,5,6,7,8,9,10,11,12,13,14];
            break;
        case 2:
            allowedIndices =  [0,1,4,5,6,7,8,9,10,11,12,13,14];
        case 3:
            allowedIndices = [0,1,2,3,4,10,11,12,13,14];
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

    
    """

    # Write JavaScript code with model_data
    js_code = js_code.replace('var parts = {};', f'var parts = {json.dumps(model_data)};')

    # Construct HTML content with embedded JavaScript and CSS
    html_content = f"""
    <!DOCTYPE HTML>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Sketchfab Viewer API example</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f5f5f5;
                font-family: Arial, sans-serif; /* Use a web-safe font */
                color: #333; /* Adjust the color to match the primary text color */
            }}
            #viewer-container {{
                width: 100%;
                max-width: 800px;
                height: 600px;
                position: relative;
                background-color: #ccc; /* Adjust the background color */
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                margin: 20px auto;
                padding: 20px;
            }}
            #api-frame {{
                width: 100%;
                height: 100%;
            }}
            #partSelect, #searchInput {{
                margin-top: 20px;
                padding: 2px;
                font-size: 16px;
                width: 100%;
                border: 1px solid #ccc; /* Add border for input fields */
                border-radius: 5px; /* Add border radius for input fields */
            }}
            #buttonContainer {{
                margin-top: 20px;
                display: flex;
                justify-content: center;
            }}
            #hideButton, #showButton, #resetViewButton {{
                margin: 0 10px;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                background-color: #007bff; /* Adjust button background color */
                color: #fff; /* Adjust button text color */
                border: none; /* Remove button border */
                border-radius: 5px; /* Add border radius to buttons */
            }}
            #suggestionBox {{
                max-height: 200px;
                overflow-y: auto;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                background-color: #fff; /* Adjust suggestion box background color */
            }}
            .suggestion-item {{
                padding: 5px 10px;
                cursor: pointer;
            }}
              #annotationContainer {{
        position: absolute;
        top: 5%; /* Keep the same vertical position */
        left: 50%; /* Keep the same horizontal position */
        transform: translate(-50%, -50%); /* Center horizontally and vertically */
        max-width: 400px; /* Adjust the max-width as needed */
        padding: 50px;
        background-color: #f9f9f9; /* Light gray background */
        border-radius: 10px; /* Rounded corners */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        z-index: 999; /* Ensure it's above other elements */
            }}
            
            #resetViewButton {{
						  position: absolute;
						  top: 20%;
                          left:10%;
						background-color: #007bff; /* Adjust button background color */
							color: #fff; /* Adjust button text color */
							font-size: 16px;
							padding: 10px 20px;
						 border: none;
							border-radius: 5px;
							cursor: pointer;
							}}
        </style>
    </head>
    <body>
        <div id="annotationContainer">
            <!-- Search input for annotations -->
            <input type="text" id="searchInput" placeholder="Search for a part...">
            <!-- Suggestions box for search input -->
            <div id="suggestionBox"></div>
        </div>
        <div id="viewer-container">
            <!-- Insert an empty iframe with attributes -->
            <iframe src="" id="api-frame" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking execution-while-out-of-viewport execution-while-not-rendered web-share allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
            <!-- Dropdown menu for parts -->
            <select id="partSelect">
                <!-- Options will be populated by JavaScript -->
            </select>
            <!-- Button container for hide/show buttons -->
            <div id="buttonContainer">
                <button id="hideButton">Hide</button>
                <button id="showButton">Show</button>
                <button id="resetViewButton">Reset View</button>
            </div>
        </div>
        <!-- Embedded JavaScript -->
        <script type="text/javascript" src="https://static.sketchfab.com/api/sketchfab-viewer-1.12.1.js"></script>
        <script type="text/javascript">
            {js_code}
        </script>
    </body>
    </html>
    """

    return html_content



def open_in_browser():
    # Save the generated HTML to a temporary file
    with open("temp.html", "w") as f:
        f.write(html_text.get("1.0", tk.END))

    # Open the temporary HTML file in the default web browser
    webbrowser.open(f'file://{os.path.realpath("temp.html")}')

app = tk.Tk()
app.title("Sketchfab Viewer API Example")

load_button = tk.Button(app, text="Load File", command=load_and_parse_file)
load_button.pack()

html_text = tk.Text(app, height=30, width=100)
html_text.pack()

open_browser_button = tk.Button(app, text="Open in Browser", command=open_in_browser)
open_browser_button.pack()

app.mainloop()
