import tkinter as tk
from tkinter import filedialog
import webbrowser
import os
import json

# ---------------------------------------------------------------------
# If you have a separate module to convert HTML paths:
# from html_converter import convert_to_relative_paths
# For now, define a placeholder function:
def convert_to_relative_paths(html_content):
    # Your logic goes here, or just return html_content as-is
    return html_content
# ---------------------------------------------------------------------

def convert_and_update():
    html_content = html_text.get("1.0", tk.END)
    converted_content = convert_to_relative_paths(html_content)
    html_text.delete("1.0", tk.END)
    html_text.insert(tk.INSERT, converted_content)

def get_uid(filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    return filename

def load_and_parse_file():
    """
    Prompts user to pick the exported .txt file. Reads lines:
      - "GroupName: ..." => model_data
      - "*SymptomName: ..." => symptom_data
    Then generates the final HTML string.
    """
    filepath = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not filepath:
        return

    model_id = get_uid(filepath)
    # Parse the .txt into two dictionaries
    model_data, symptom_data = parse_file(filepath)
    # Generate HTML from them
    generated_html = generate_html(model_id, model_data, symptom_data)

    # Insert into the big text box
    html_text.delete("1.0", tk.END)
    html_text.insert(tk.END, generated_html)

def parse_file(filepath):
    """
    Reads each line of the .txt file:
      - If line starts with '*', it's a symptom => symptom_data
      - Otherwise, it's a normal group => model_data

    Example lines:
      Motor: 10,11,12
      *WillNotAgitate: 10,12
    """
    model_data = {}
    symptom_data = {}

    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if line.startswith("*"):
                # Symptom line
                line = line[1:].strip()  # remove leading '*'
                parts = line.split(":")
                if len(parts) == 2:
                    symptom_name = parts[0].strip()
                    ids = [int(x.strip()) for x in parts[1].split(",") if x.strip()]
                    symptom_data[symptom_name] = ids
            else:
                # Normal group
                parts = line.split(":")
                if len(parts) == 2:
                    group_name = parts[0].strip()
                    ids = [int(x.strip()) for x in parts[1].split(",") if x.strip()]
                    model_data[group_name] = ids

    return model_data, symptom_data

def generate_html(model_id, model_data, symptom_data):
    """
    Builds the HTML page with two menus:
      - Main parts menu (model_data)
      - Symptoms menu (symptom_data)
    Now includes extra debugging logs in the symptom click handler.
    """
    # We embed our JS code as a multiline string:
    js_code = f"""
    // Dictionaries from Python
    var parts = {json.dumps(model_data)};
    var symptoms = {json.dumps(symptom_data)};
    var api = null;
    var annotationsData = [];

    // Menu toggles
    var menuOpen = false;
    var symptomsMenuOpen = false;

    function hideAllPartsIndividually() {{
        // Hide all normal parts
        for (var p in parts) {{
            parts[p].forEach(function(id) {{
                api.hide(id);
            }});
        }}
        // Hide all symptom parts
        for (var s in symptoms) {{
            symptoms[s].forEach(function(id) {{
                api.hide(id);
            }});
        }}
    }}

    function showAllParts() {{
        // Show everything (normal parts + symptoms)
        for (var p in parts) {{
            parts[p].forEach(function(id) {{
                api.show(id);
            }});
        }}
        for (var s in symptoms) {{
            symptoms[s].forEach(function(id) {{
                api.show(id);
            }});
        }}
    }}

    // Populate the MAIN PARTS menu (toggle logic)
    function populateMainMenu() {{
        var menuContainer = document.getElementById("partMenuContainer");
        menuContainer.innerHTML = "";

        for (var part in parts) {{
            var item = document.createElement("div");
            item.className = "menu-item";
            item.textContent = part;

            // Eye icon
            var icon = document.createElement("img");
            icon.className = "icon";
            icon.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
            item.appendChild(icon);

            (function(selectedPart, iconElement, itemElement) {{
                itemElement.onclick = function() {{
                    // If currently selected => un-toggle => show that group again
                    if (itemElement.classList.contains("selected")) {{
                        itemElement.classList.remove("selected");
                        iconElement.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
                        parts[selectedPart].forEach(function(id) {{
                            api.show(id);
                        }});
                    }} else {{
                        // Hide that group's IDs
                        parts[selectedPart].forEach(function(id) {{
                            api.hide(id);
                        }});
                        itemElement.classList.add("selected");
                        iconElement.src = "C:/Users/jsmith/Blender/User interface/icons/closed-eye.png";
                    }}
                }};
            }})(part, icon, item);

            menuContainer.appendChild(item);
        }}
    }}

    // Populate the SYMPTOMS menu (inverse logic)
    // Debugging logs added to see which IDs we're showing.
    function populateSymptomsMenu() {{
        var symptomsMenuContainer = document.getElementById("symptomsMenuContainer");
        symptomsMenuContainer.innerHTML = "<div class='menu-header'>Common Symptoms</div>";

        // Debug: Print entire symptom dictionary
        console.log("Symptom dictionary:", symptoms);

        for (var symptom in symptoms) {{
            var item = document.createElement("div");
            item.className = "menu-item";
            item.textContent = symptom;

            // Eye icon
            var icon = document.createElement("img");
            icon.className = "icon";
            icon.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
            item.appendChild(icon);

            (function(selectedSymptom, iconElement, itemElement) {{
                itemElement.onclick = function() {{
                    console.log("Clicked symptom:", selectedSymptom);
                    console.log("Symptom array is:", symptoms[selectedSymptom]);

                    // Already selected => un-toggle => show all
                    if (itemElement.classList.contains("selected")) {{
                        itemElement.classList.remove("selected");
                        iconElement.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
                        showAllParts();
                    }} else {{
                        // Hide everything first
                        hideAllPartsIndividually();

                        // Show only the symptom’s parts
                        resetSymptomsMenuSelection();
                        itemElement.classList.add("selected");
                        iconElement.src = "C:/Users/jsmith/Blender/User interface/icons/closed-eye.png";

                        // Debug: see which IDs we're trying to show
                        symptoms[selectedSymptom].forEach(function(id) {{
                            console.log(" -> Attempting to show ID:", id);
                            api.show(id);
                        }});
                    }}
                }};
            }})(symptom, icon, item);

            symptomsMenuContainer.appendChild(item);
        }}
    }}

    function resetSymptomsMenuSelection() {{
        var container = document.getElementById("symptomsMenuContainer");
        var items = container.getElementsByClassName("menu-item");
        for (var i = 0; i < items.length; i++) {{
            var sItem = items[i];
            var sIcon = sItem.getElementsByTagName("img")[0];
            sItem.classList.remove("selected");
            sIcon.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
        }}
    }}

    function toggleMenu() {{
        var menu = document.getElementById("partMenuContainer");
        menu.style.display = menuOpen ? "none" : "block";
        menuOpen = !menuOpen;
    }}

    function toggleSymptomsMenu() {{
        var menu = document.getElementById("symptomsMenuContainer");
        menu.style.display = symptomsMenuOpen ? "none" : "block";
        symptomsMenuOpen = !symptomsMenuOpen;
    }}

    // If you need annotation logic, etc.
    function getMaxTextureSize() {{
        let maxTextureSize = 512;
        if (navigator.deviceMemory) {{
            const memory = navigator.deviceMemory;
            if (memory <= 2) {{
                maxTextureSize = 512;
            }} else if (memory <= 4) {{
                maxTextureSize = 1024;
            }} else if (memory <= 7) {{
                maxTextureSize = 2048;
            }} else {{
                maxTextureSize = 4096;
            }}
        }} else {{
            const userAgent = navigator.userAgent || navigator.vendor || window.opera;
            const isMobile = /android|iphone|ipad|ipod/i.test(userAgent);
            maxTextureSize = isMobile ? 512 : 1024;
        }}
        return maxTextureSize;
    }}

    function filterAnnotations(api, annotations) {{
        annotationsData = annotations;
    }}

    function navigateToAnnotation(annotationName) {{
        var index = annotationsData.findIndex(a => a.name.toLowerCase() === annotationName.toLowerCase());
        if (index !== -1) {{
            api.gotoAnnotation(index, {{}}, function(err) {{
                if (!err) {{
                    console.log('Navigated to annotation:', index + 1);
                }}
            }});
        }}
    }}

    // On window load, set up the Sketchfab iframe, etc.
    window.onload = function() {{
        var placeholder = document.getElementById("placeholder-image");
        var iframe = document.getElementById("api-frame");

        iframe.onload = function() {{
            placeholder.style.display = "none";
        }};

        var uid = '{model_id}';
        var maxTextureSize = getMaxTextureSize();
        var client = new Sketchfab(iframe);

        client.init(uid, {{
            success: function(apiInstance) {{
                api = apiInstance;
                api.start(function() {{
                    api.addEventListener('viewerready', function() {{
                        api.getAnnotationList(function(err, annotations) {{
                            if (!err) {{
                                filterAnnotations(api, annotations);
                            }}
                        }});
                    }});
                }});
            }},
            error: function(err) {{
                console.error('Sketchfab API error:', err);
            }},
            autostart: 0,
            preload: 1,
            max_texture_size: maxTextureSize,
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
        }});

        // Populate both menus
        populateMainMenu();
        populateSymptomsMenu();

        // Main menu icon
        document.getElementById("partMenuButton").addEventListener("click", function() {{
            toggleMenu();
        }});

        // Symptom menu icon
        document.getElementById("symptomsMenuButton").addEventListener("click", function() {{
            toggleSymptomsMenu();
        }});

        // Reset button
        document.getElementById("playIconButton").addEventListener("click", function() {{
            api.recenterCamera(function(err) {{
                if (!err) {{
                    showAllParts();
                    resetMenus();
                }}
            }});
        }});

        function resetMenus() {{
            // Reset the main dropdown
            var menuContainer = document.getElementById("partMenuContainer");
            var menuItems = menuContainer.getElementsByClassName("menu-item");
            for (var i = 0; i < menuItems.length; i++) {{
                var item = menuItems[i];
                var icon = item.getElementsByTagName("img")[0];
                item.classList.remove("selected");
                icon.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
            }}

            // Reset the symptom dropdown
            resetSymptomsMenuSelection();
        }}

        // Searching logic
        var searchInput = document.getElementById("searchInput");
        searchInput.addEventListener('input', function() {{
            var searchValue = this.value.toLowerCase();
            var filteredAnnotations = annotationsData.filter(annotation => 
                annotation.name.toLowerCase().includes(searchValue)
            );

            var suggestionBox = document.getElementById('suggestionBox');
            suggestionBox.innerHTML = '';

            const maxSuggestions = 5;
            filteredAnnotations.slice(0, maxSuggestions).forEach(annotation => {{
                var suggestionItem = document.createElement('div');
                suggestionItem.classList.add('suggestion-item');
                suggestionItem.textContent = annotation.name;
                suggestionItem.onclick = () => navigateToAnnotation(annotation.name);
                suggestionBox.appendChild(suggestionItem);
            }});

            suggestionBox.style.display = filteredAnnotations.length ? "block" : "none";
        }});

        document.addEventListener('click', function(event) {{
            var suggestionBox = document.getElementById("suggestionBox");
            var searchInput = document.getElementById("searchInput");
            if (!searchInput.contains(event.target) && !suggestionBox.contains(event.target)) {{
                suggestionBox.style.display = "none";
            }}
        }});

        // Third icon: user manual in popup
        document.getElementById("thirdIconButton").addEventListener("click", function() {{
            var popup = document.getElementById("popup-container");
            var iframe = document.getElementById("popup-iframe");
            iframe.src = "https://docs.google.com/gview?url=https://partselectca-dsfph5cffxaaesb6.z01.azurefd.net/assets/manuals/EBF4AEBB8D1FC994820343DF54BFFE6BD3BA063D.pdf&embedded=true";
            popup.style.display = "block";
        }});

        document.getElementById("popup-iframe").onload = function() {{
            if (this.contentDocument && this.contentDocument.body.innerHTML.trim() === "") {{
                console.error("Failed to load the PDF. Retrying...");
                this.src = this.src;
            }} else {{
                console.log("PDF loaded successfully.");
            }}
        }};

        document.getElementById("close-popup").addEventListener("click", function() {{
            var popup = document.getElementById("popup-container");
            var iframe = document.getElementById("popup-iframe");
            popup.style.display = "none";
            iframe.src = "";
        }});

        // Close menus if clicking outside them
        document.addEventListener('click', function(event) {{
            var menu = document.getElementById("partMenuContainer");
            var symptomsMenu = document.getElementById("symptomsMenuContainer");
            var partButton = document.getElementById("partMenuButton");
            var symptomsButton = document.getElementById("symptomsMenuButton");

            // main menu
            if (menu.style.display == "block" && !menu.contains(event.target) && !partButton.contains(event.target)) {{
                toggleMenu();
            }}
            // symptom menu
            if (symptomsMenu.style.display == "block" && !symptomsMenu.contains(event.target) && !symptomsButton.contains(event.target)) {{
                toggleSymptomsMenu();
            }}
        }});
    }};
    """

    html_content = f"""
<!DOCTYPE HTML>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Sketchfab Viewer API Example</title>
    <link href='https://fonts.googleapis.com/css?family=Roboto' rel='stylesheet' type='text/css'>
    <style>
        body {{
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f5f5f5;
        }}
        #viewer-container {{
            position: relative;
            width: 100%;
            max-width: 800px;
            height: 600px;
            border: none;
            margin: 20px auto;
            padding: 20px;
        }}
        #api-frame {{
            width: 100%;
            height: 100%;
        }}
        #placeholder-image {{
            width: 50%;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 1;
        }}
        #searchInput {{
            position: absolute;
            top: 25px;
            right:25%;
            width: 35%;
            padding: 3px;
            font-size: 16px;
        }}
        #suggestionBox {{
            position: absolute;
            top: 50px;
            right: 20px;
            width: 50%;
            background-color: #fff;
            border: 1px solid #ccc;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            font-size: 16px;
            z-index: 1001;
            display: none;
        }}
        .suggestion-item {{
            padding: 5px 10px;
            background-color: #fff;
            cursor: pointer;
        }}
        #partMenuButton {{
            position: absolute;
            top: 15px;
            left: 15px;
            width: 7%;
            cursor: pointer;
            z-index: 1000;
            transition: all 0.3s ease;
        }}
        #symptomsMenuButton {{
            position: absolute;
            top: 15px;
            left: 21%;
            width: 7%;
            cursor: pointer;
            z-index: 1000;
        }}
        #partMenuContainer {{
            display: none;
            position: absolute;
            top: 40px;
            left: 10px;
            background-color: #fff;
            border: 1px solid #ccc;
            border-radius: 3px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            z-index: 1001;
            width: 150px;
        }}
        #symptomsMenuContainer {{
            display: none;
            position: absolute;
            top: 40px;
            left: 21%;
            background-color: #fff;
            border: 1px solid #ccc;
            border-radius: 3px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            z-index: 1001;
            width: 150px;
        }}
        .menu-header {{
            font-weight: bold;
            padding: 6px;
            background-color: #eee;
            border-bottom: 1px solid #ccc;
            text-align: center;
        }}
        #playIconButton {{
            position: absolute;
            top: 16px;
            left: 8%;
            width: 6.7%;
            cursor: pointer;
            z-index: 1000;
        }}
        #thirdIconButton {{
            position: absolute;
            top: 14px;
            left: 14.2%;
            width: 7.4%;
            cursor: pointer;
            z-index: 1000;
        }}
        #popup-container {{
            display:none;
            position: fixed;
            top: 25%;
            left: 29%;
            width: 42%;
            height: 42%;
            background-color: white;
            border: 2px solid #000;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            z-index: 1002;
        }}
        #popup-iframe {{
            width: 100%;
            height: 100%;
            overflow: auto;
            border: none;
        }}
        .menu-item {{
            display: inline-flex;
            align-items: center;
            padding: 3px 6px;
            cursor: pointer;
            width: auto;
            margin-bottom: 2px;
        }}
        .selected {{
            background-color: #ccc;
        }}
        .icon {{
            width: 13%;
            margin-right: 5px;
        }}
        .tooltip {{
            position: absolute;
            top: 13%;
            left: 1.5%;
            color: white;
            display: block;
            background-color: #fbbc29;
            border-radius: 5px;
            padding: 10px;
            text-align: center;
            z-index: 1000;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }}
        .tooltip::before {{
            content: "";
            position: absolute;
            top: -10px;
            left: 20px;
            border-width: 0 10px 10px 10px;
            border-style: solid;
            border-color: transparent transparent #fbbc29 transparent;
        }}
        .tooltip .closebtn {{
            position: absolute;
            top: 0;
            right: 5px;
            font-size: 20px;
            color: white;
            cursor: pointer;
        }}
        @media only screen and (max-width: 480px) {{
            .icon {{
                width: 20%;
            }}
            #thirdIconButton {{ width: 17%; left: 29.5%; }}
            #playIconButton {{ width: 15%; left: 16.5%;}}
            #partMenuButton {{ width: 15%; }}
            #symptomsMenuButton {{ width: 15%; left: 44%; }}
            #searchInput {{ right:16%;}}
            #popup-container {{
                width: 88vw !important;
                height: 60vh !important;
                position: fixed !important;
                top: 20% !important;
                left: 6% !important;
                -webkit-overflow-scrolling: touch;
                overflow: auto;
            }}
            #viewer-container {{ height: 500px; }}
            .tooltip {{ top: 16%; left: 2.5%; }}
        }}
        #partMenuButton:hover, #playIconButton:hover, #thirdIconButton:hover, #symptomsMenuButton:hover {{
            transform: scale(1.1);
        }}
        #partMenuButton:active, #playIconButton:active, #thirdIconButton:active, #symptomsMenuButton:active {{
            transform: scale(0.9);
        }}
    </style>
</head>
<body>
    <div id="viewer-container">
        <!-- This placeholder image is hidden once the iframe loads -->
        <img src="C:/Users/jsmith/Blender/User interface/icons/MicrosoftTeams-image (1).png"
             id="placeholder-image" alt="Placeholder Image">

        <!-- The Sketchfab iframe -->
        <iframe src="" id="api-frame"></iframe>

        <!-- Main parts menu icon -->
        <img src="C:/Users/jsmith/Blender/User interface/icons/dropdown_icon.png"
             id="partMenuButton" alt="Menu" draggable="false" title="Hide a section">

        <div class="tooltip" style="display: block;">
            <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>
            <p>Click here to hide a section</p>
        </div>

        <!-- Reset view icon -->
        <img src="C:/Users/jsmith/Blender/User interface/icons/reset.png"
             id="playIconButton" class="icon" alt="Reset" draggable="false" title="Reset View">

        <!-- Third icon -> open user manual popup -->
        <img src="C:/Users/jsmith/Blender/User interface/icons/manual.png"
             id="thirdIconButton" class="icon" draggable="false" title="View user manual">

        <!-- Symptoms menu icon -->
        <img src="C:/Users/jsmith/Blender/User interface/icons/dropdown_icon.png"
             id="symptomsMenuButton" alt="Symptoms Menu" draggable="false" title="Hide all except symptom(s)">

        <!-- Popup container for user manual -->
        <div id="popup-container">
            <iframe src="" id="popup-iframe"></iframe>
            <button id="close-popup" style="position: absolute; top: 5px; right: 5px; background-color: #f00; color: #fff; border: none; cursor: pointer;">
                X
            </button>
        </div>

        <!-- The two dropdown containers -->
        <div id="partMenuContainer"></div>
        <div id="symptomsMenuContainer"></div>

        <!-- Search box -->
        <input type="text" id="searchInput" placeholder="Search Parts">
        <div id="suggestionBox"></div>
    </div>

    <!-- Sketchfab API script -->
    <script type="text/javascript" src="https://static.sketchfab.com/api/sketchfab-viewer-1.12.1.js"></script>

    <!-- Our dynamic JS code -->
    <script type="text/javascript">
    {js_code}
    </script>
</body>
</html>
    """
    return html_content

def open_in_browser():
    """Writes the current HTML from the text box to temp.html and opens it in the default browser."""
    with open("temp.html", "w", encoding="utf-8") as f:
        f.write(html_text.get("1.0", tk.END))
    webbrowser.open(f'file://{os.path.realpath("temp.html")}')

# ---------------------------------------------------------------------
# The Tkinter GUI
# ---------------------------------------------------------------------
app = tk.Tk()
app.title("Sketchfab Viewer API Example")

load_button = tk.Button(app, text="Load File", command=load_and_parse_file)
load_button.pack()

convert_button = tk.Button(app, text="Convert Paths to Relative", command=convert_and_update)
convert_button.pack()

html_text = tk.Text(app, height=30, width=100)
html_text.pack()

open_browser_button = tk.Button(app, text="Open in Browser", command=open_in_browser)
open_browser_button.pack()

app.mainloop()
