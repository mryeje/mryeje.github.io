import tkinter as tk
from tkinter import filedialog
import webbrowser
import os
import json

def get_uid(filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    return filename

def load_and_parse_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not filepath:
        return

    model_id = get_uid(filepath)
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
    js_code = """
    var parts = {};
    var menuOpen = false;

    function populateMenu() {
        var menuContainer = document.getElementById("partMenuContainer");
        menuContainer.innerHTML = "";

        for (var part in parts) {
            var item = document.createElement("div");
            item.className = "menu-item";
            item.textContent = part;

            var icon = document.createElement("img");
            icon.className = "icon";
            icon.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
            item.appendChild(icon);

            (function(selectedPart, iconElement, itemElement) {
                itemElement.onclick = function() {
                    if (itemElement.classList.contains("selected")) {
                        itemElement.classList.remove("selected");
                        iconElement.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
                        parts[selectedPart].forEach(showup);
                    } else {
                        api.hide();
                        switch (selectedPart) {
                            case 'Fridge door':
                                showSpecificAnnotation(api, 0, 1);
                                break;
                            case 'Freezer Door':
                                showSpecificAnnotation(api, 0, 2);
                                break;
                            case 'Refrigeration Unit':
                                showSpecificAnnotation(api, 0, 3);
                                break;
                            case 'Fridge shelves':
                                showSpecificAnnotation(api, 0, 4);
                                break;
                            case 'Freezer Shelves':
                                showSpecificAnnotation(api, 0, 5);
                                break;
                            default:
                                console.log(selectedPart);
                        }

                        parts[selectedPart].forEach(hideout);
                        itemElement.classList.add("selected");
                        iconElement.src = "C:/Users/jsmith/Blender/User interface/icons/closed-eye.png";
                    }
                };
            })(part, icon, item);

            menuContainer.appendChild(item);
        }
    }

    function toggleMenu() {
        var menu = document.getElementById("partMenuContainer");
        menu.style.display = menuOpen ? "none" : "block";
        menuOpen = !menuOpen;
    }

    function hideout(item) {
        api.hide(item);
    }

    function showup(item) {
        api.show(item);
    }

  function showSpecificAnnotation(api, annotationIndex, option) {
    var allowedIndices = [];

    switch (option) {
        case 1:
            allowedIndices = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16];
            break;
        case 2:
            allowedIndices = [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16];
            break;
        case 3:
            allowedIndices = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 15, 16];
            break;
        case 4:
            allowedIndices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16];
            break;
        case 5:
            allowedIndices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15];
            break;
        default:
            console.error('Invalid option:', option);
            return;
    }

    api.getAnnotationList(function (err, annotations) {
        if (err) {
            console.error('Error getting annotations:', err);
            return;
        }

        annotations.forEach((annotation, index) => {
            if (allowedIndices.includes(index)) {
                api.showAnnotation(index);
            } else {
                api.hideAnnotation(index);
            }
        });
    });
}


    window.onload = function() {
        var placeholder = document.getElementById("placeholder-image");
        var iframe = document.getElementById("api-frame");
        iframe.onload = function() {
            placeholder.style.display = "none";
        };
        
        populateMenu();

        var uid = '""" + model_id + """';
        var client = new Sketchfab(iframe);
        client.init(uid, {
            success: function(apiInstance) {
                api = apiInstance;
                api.start(function() {
                    api.addEventListener('viewerready', function() {
                        api.getAnnotationList(function(err, annotations) {
                            if (!err) {
                                annotationsData = annotations;
                                filterAnnotations(api, annotations);
                            }
                        });
                    });
                });
            },
            error: function(err) {
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
        
        document.getElementById("partMenuButton").addEventListener("click", function() {
            toggleMenu();
        });

        document.getElementById("playIconButton").addEventListener("click", function() {
            api.recenterCamera(function(err) {
                if (!err) {
                    Object.keys(parts).forEach(function(part) {
                        parts[part].forEach(function(item) {
                            api.show(item);
                        });
                    });
                }
            });
        });

        var searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('input', function() {
            var searchValue = this.value.toLowerCase();
            var filteredAnnotations = annotationsData.filter(annotation => annotation.name.toLowerCase().includes(searchValue));

            var suggestionBox = document.getElementById('suggestionBox');
            suggestionBox.innerHTML = '';

            const maxSuggestions = 5;
            filteredAnnotations.slice(0, maxSuggestions).forEach(annotation => {
                var suggestionItem = document.createElement('div');
                suggestionItem.classList.add('suggestion-item');
                suggestionItem.textContent = annotation.name;
                suggestionItem.onclick = () => navigateToAnnotation(annotation.name);
                suggestionBox.appendChild(suggestionItem);
            });
        });

        document.getElementById("thirdIconButton").addEventListener("click", function() {
            var popup = document.getElementById("popup-container");
            var iframe = document.getElementById("popup-iframe");
            iframe.src = "https://www.partselect.com/Models/GFE26GMKFES/";
            popup.style.display = "block";
        });
        
        document.getElementById("close-popup").addEventListener("click", function() {
            var popup = document.getElementById("popup-container");
            var iframe = document.getElementById("popup-iframe");
            popup.style.display = "none";
            iframe.src = "";
        });

        document.addEventListener('click', function(event) {
            var menu = document.getElementById("partMenuContainer");
            if (menu.style.display == "block" && !menu.contains(event.target) && !document.getElementById("partMenuButton").contains(event.target)) {
                toggleMenu();
            }
        });
    };

    function filterAnnotations(api, annotationsData) {
        window.annotationsData = annotationsData;
    }

    function navigateToAnnotation(annotationName) {
        var index = annotationsData.findIndex(annotation == annotationName);
        if (index !== -1) {
            api.gotoAnnotation(index, {}, function(err) {
                if (!err) {
                    console.log('Navigated to annotation:', index + 1);
                }
            });
        }
    }
    """

    js_code = js_code.replace('var parts = {};', f'var parts = {json.dumps(model_data)};')

    html_content = f"""
<!DOCTYPE HTML>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Sketchfab Viewer API Example</title>
    <style>
        body {{
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
            margin-top: 20px;
            padding: 2px;
            font-size: 16px;
            width: 50%;
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
        #partMenuButton:hover, #playIconButton:hover {{
           transform: scale(1.1);
        }}
        #partMenuButton:active, #playIconButton:active {{
            transform: scale(0.9);
        }}
        #playIconButton {{
            position: absolute;
            top: 15px;
            left: 70px;
            width: 6.5%;
            cursor: pointer;
            z-index: 1000;
        }}
        #partMenuIcon {{
            width: 20px;
            height: 20px;
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
        #thirdIconButton {{
            position: absolute;
            top: 10px;
            left: 120px;
            width: 8.1%;
            cursor: pointer;
            z-index: 1000;
        }}
        #thirdIconButton:active {{
            transform: scale(0.9);
        }}
         #thirdIconButton:hover {{
           transform: scale(1.1);
        }}
        #suggestionBox {{
            width: 50%;
        }}
        .menu-item {{
            display: inline-flex;
            align-items: center;
            padding: 2px 5px;
            cursor: pointer;
            width: auto;
            margin-bottom: 2px;
        }}
        .selected {{
            background-color: #ccc;
        }}
        .suggestion-item {{
            padding: 5px 10px;
            background-color: #fff;
            cursor: pointer;
        }}
        .icon {{
            width: 13%;
            margin-right: 5px;
        }}
    </style>
</head>
<body>
    <div id="viewer-container">
        <img src="C:/Users/jsmith/Blender/User interface/icons/PT_CA_Vert_Logo_595x247_no_artboard.png" id="placeholder-image" alt="Placeholder Image">
        <iframe src="" id="api-frame"></iframe>
        <img src="C:/Users/jsmith/Blender/User interface/icons/dropdown_icon.png" id="partMenuButton" alt="Menu" draggable="false" title="Hide a section">
        <img src="C:/Users/jsmith/Blender/User interface/icons/reset.png" id="playIconButton" class="icon" alt="New Icon" draggable="false" title="Reset View">
        <img src="C:/Users/jsmith/Blender/User interface/icons/web-icon.png" id="thirdIconButton" class="icon" draggable="false" title="View this Model online">
        <div id="popup-container" style="display:none; position: fixed; top: 25%; left: 29%; width: 42%; height: 42%; background-color: white; border: 2px solid #000; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); z-index: 1002;">
            <iframe src="" id="popup-iframe" style="width: 75%; height: 75%; border: none;"></iframe>
            <button id="close-popup" style="position: absolute; top: 5px; right: 5px; background-color: #f00; color: #fff; border: none; cursor: pointer;">X</button>
        </div>
        <div id="partMenuContainer"></div>
        <input type="text" id="searchInput" placeholder="Search Parts">
        <div id="suggestionBox"></div>
    </div>
    <script type="text/javascript" src="https://static.sketchfab.com/api/sketchfab-viewer-1.12.1.js"></script>
    <script type="text/javascript">{js_code}</script>
</body>
</html>
    """

    return html_content







def open_in_browser():
    with open("temp.html", "w", encoding="utf-8") as f:
        f.write(html_text.get("1.0", tk.END))

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
