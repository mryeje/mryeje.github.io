import tkinter as tk
from tkinter import filedialog
import webbrowser
import os
import json

##############################################################################
# 1) Convert paths (placeholder)
##############################################################################
def convert_to_relative_paths(html_content):
    return html_content

def convert_and_update():
    content = html_text_normal.get("1.0", tk.END)
    converted = convert_to_relative_paths(content)
    html_text_normal.delete("1.0", tk.END)
    html_text_normal.insert(tk.END, converted)

##############################################################################
# 2) Helpers
##############################################################################
def get_uid(filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    return filename

def parse_file(filepath):
    model_data = {}
    symptom_data = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("*"):
                line = line[1:].strip()  # symptom line
                parts = line.split(":")
                if len(parts) == 2:
                    sname = parts[0].strip()
                    ids = [int(x.strip()) for x in parts[1].split(",") if x.strip()]
                    symptom_data[sname] = ids
            else:
                parts = line.split(":")
                if len(parts) == 2:
                    gname = parts[0].strip()
                    ids = [int(x.strip()) for x in parts[1].split(",") if x.strip()]
                    model_data[gname] = ids
    return model_data, symptom_data

##############################################################################
# 3) Generate Normal HTML (temp.html)
##############################################################################
def generate_html_normal(model_id, model_data, symptom_data):
    # In this version the "symptoms" menu icon is turned into a hyperlink.
    js_code = f"""
    var parts = {json.dumps(model_data)};
    var symptoms = {json.dumps(symptom_data)};
    var api = null;
    var annotationsData = [];

    var menuOpen = false;
    // Note: We no longer need to build a symptoms menu on this page.

    function hideAllPartsIndividually() {{
        for (var p in parts) {{
            parts[p].forEach(function(id) {{
                api.hide(id);
            }});
        }}
        for (var s in symptoms) {{
            symptoms[s].forEach(function(id) {{
                api.hide(id);
            }});
        }}
    }}

    function showAllParts() {{
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

    // Populate main parts menu
    function populateMainMenu() {{
        var menuContainer = document.getElementById("partMenuContainer");
        menuContainer.innerHTML = "";
        for (var part in parts) {{
            var item = document.createElement("div");
            item.className = "menu-item";
            item.textContent = part;

            var icon = document.createElement("img");
            icon.className = "icon";
            icon.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
            item.appendChild(icon);

            (function(selectedPart, iconElement, itemElement) {{
                itemElement.onclick = function() {{
                    if (itemElement.classList.contains("selected")) {{
                        itemElement.classList.remove("selected");
                        iconElement.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
                        parts[selectedPart].forEach(function(id) {{
                            api.show(id);
                        }});
                    }} else {{
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

    // Instead of a symptoms menu, the Symptoms icon will be a hyperlink.
    // No need to build a menu here.
    window.onload = function() {{
        var placeholder = document.getElementById("placeholder-image");
        var iframe = document.getElementById("api-frame");
        iframe.onload = function() {{
            placeholder.style.display = "none";
        }};

        var uid = "{model_id}";
        var client = new Sketchfab(iframe);
        var maxTexture = (function() {{
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
                const ua = navigator.userAgent || navigator.vendor || window.opera;
                const isMobile = /android|iphone|ipad|ipod/i.test(ua);
                maxTextureSize = isMobile ? 512 : 1024;
            }}
            return maxTextureSize;
        }})();

        client.init(uid, {{
            success: function(apiInstance) {{
                api = apiInstance;
                api.start(function() {{
                    api.addEventListener('viewerready', function() {{
                        api.getAnnotationList(function(err, annotations) {{
                            if (!err) {{
                                annotationsData = annotations;
                            }}
                        }});
                    }});
                }});
            }},
            error: function(err) {{
                console.error("Sketchfab API error:", err);
            }},
            autostart: 0,
            preload: 1,
            max_texture_size: maxTexture,
            transparent: 1,
            ui_watermark: 0,
            ui_infos: 0,
            ui_controls: 1,
            ui_annotations: 1,
            ui_settings: 0
        }});

        populateMainMenu();

        // Normal page: Change the Symptoms icon to be a button that navigates to the symptom page in the same window.
        document.getElementById("symptomsMenuButton").addEventListener("click", function() {{
            window.location.href = "temp_symptom.html";
        }});

        // Part menu icon toggling
        document.getElementById("partMenuButton").addEventListener("click", function() {{
            var menu = document.getElementById("partMenuContainer");
            menu.style.display = menuOpen ? "none" : "block";
            menuOpen = !menuOpen;
        }});

        // Reset icon
        document.getElementById("playIconButton").addEventListener("click", function() {{
            api.recenterCamera(function(err) {{
                if (!err) {{
                    showAllParts();
                    var pmc = document.getElementById("partMenuContainer");
                    var items = pmc.getElementsByClassName("menu-item");
                    for (var i = 0; i < items.length; i++) {{
                        var item = items[i];
                        var icon = item.getElementsByTagName("img")[0];
                        item.classList.remove("selected");
                        icon.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
                    }}
                }}
            }});
        }});

        // Manual icon => open user manual popup
        document.getElementById("thirdIconButton").addEventListener("click", function() {{
            var pop = document.getElementById("popup-container");
            var ifr = document.getElementById("popup-iframe");
            ifr.src = "https://docs.google.com/gview?url=https://partselectca-dsfph5cffxaaesb6.z01.azurefd.net/assets/manuals/EBF4AEBB8D1FC994820343DF54BFFE6BD3BA063D.pdf&embedded=true";
            pop.style.display = "block";
        }});
        document.getElementById("popup-iframe").onload = function() {{
            if (this.contentDocument && this.contentDocument.body.innerHTML.trim() === "") {{
                console.error("Failed to load the PDF. Retrying...");
                this.src = this.src;
            }}
        }};
        document.getElementById("close-popup").addEventListener("click", function() {{
            var pop = document.getElementById("popup-container");
            var ifr = document.getElementById("popup-iframe");
            pop.style.display = "none";
            ifr.src = "";
        }});

        // Searching built-in annotations
        var searchInput = document.getElementById("searchInput");
        var suggestionBox = document.getElementById("suggestionBox");
        searchInput.addEventListener('input', function() {{
            var val = this.value.toLowerCase();
            var filtered = annotationsData.filter(annotation => 
                annotation.name.toLowerCase().includes(val)
            );
            suggestionBox.innerHTML = '';
            const maxS = 5;
            filtered.slice(0, maxS).forEach(annotation => {{
                var suggestionItem = document.createElement('div');
                suggestionItem.classList.add('suggestion-item');
                suggestionItem.textContent = annotation.name;
                suggestionItem.onclick = () => navigateToAnnotation(annotation.name);
                suggestionBox.appendChild(suggestionItem);
            }});
            suggestionBox.style.display = filtered.length ? "block" : "none";
        }});
        document.addEventListener('click', function(e) {{
            if (!searchInput.contains(e.target) && !suggestionBox.contains(e.target)) {{
                suggestionBox.style.display = "none";
            }}
        }});
    }};
    """
    normal_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Normal Page</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
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
            right: 25%;
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
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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
            display: none;
            position: fixed;
            top: 25%;
            left: 29%;
            width: 42%;
            height: 42%;
            background-color: white;
            border: 2px solid #000;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
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
    </style>
</head>
<body>
    <div id="viewer-container">
        <img src="C:/Users/jsmith/Blender/User interface/icons/MicrosoftTeams-image (1).png"
             id="placeholder-image" alt="Placeholder">
        <iframe src="" id="api-frame"></iframe>
        <img src="C:/Users/jsmith/Blender/User interface/icons/dropdown_icon.png"
             id="partMenuButton" alt="Menu" draggable="false" title="Hide a section">
        <img src="C:/Users/jsmith/Blender/User interface/icons/reset.png"
             id="playIconButton" class="icon" alt="Reset" draggable="false" title="Reset View">
        <img src="C:/Users/jsmith/Blender/User interface/icons/manual.png"
             id="thirdIconButton" class="icon" draggable="false" title="View user manual">
        <img src="C:/Users/jsmith/Blender/User interface/icons/dropdown_icon.png"
             id="symptomsMenuButton" alt="Symptoms Menu" draggable="false" title="Go to Symptoms Page">
        <div id="popup-container">
            <iframe src="" id="popup-iframe"></iframe>
            <button id="close-popup" style="position:absolute; top:5px; right:5px; background:#f00; color:#fff; border:none; cursor:pointer;">X</button>
        </div>
        <div id="partMenuContainer"></div>
        <div id="symptomsMenuContainer"></div>
        <input type="text" id="searchInput" placeholder="Search Parts">
        <div id="suggestionBox"></div>
    </div>
    <script src="https://static.sketchfab.com/api/sketchfab-viewer-1.12.1.js"></script>
    <script>
    {js_code}
    </script>
</body>
</html>
    """
    return normal_html

##############################################################################
# 4) Generate the Symptom HTML (temp_symptom.html)
##############################################################################
def generate_html_symptom(model_id, model_data, symptom_data):
    js_code = f"""
    var parts = {json.dumps(model_data)};
    var symptoms = {json.dumps(symptom_data)};
    var api = null;
    var annotationsData = [];

    var menuOpen = false;
    var symptomsMenuOpen = false;

    function hideAllPartsIndividually() {{
        for (var p in parts) {{
            parts[p].forEach(id => api.hide(id));
        }}
        for (var s in symptoms) {{
            symptoms[s].forEach(id => api.hide(id));
        }}
    }}

    function showAllParts() {{
        for (var p in parts) {{
            parts[p].forEach(id => api.show(id));
        }}
        for (var s in symptoms) {{
            symptoms[s].forEach(id => api.show(id));
        }}
    }}

    function populateMainMenu() {{
        var container = document.getElementById("partMenuContainer");
        container.innerHTML = "";
        for (var part in parts) {{
            var item = document.createElement("div");
            item.className = "menu-item";
            item.textContent = part;

            var icon = document.createElement("img");
            icon.className = "icon";
            icon.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
            item.appendChild(icon);

            (function(partName, iconElem, itemElem) {{
                itemElem.onclick = function() {{
                    if (itemElem.classList.contains("selected")) {{
                        itemElem.classList.remove("selected");
                        iconElem.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
                        parts[partName].forEach(id => api.show(id));
                    }} else {{
                        itemElem.classList.add("selected");
                        iconElem.src = "C:/Users/jsmith/Blender/User interface/icons/closed-eye.png";
                        parts[partName].forEach(id => api.hide(id));
                    }}
                }};
            }})(part, icon, item);

            container.appendChild(item);
        }}
    }}

    function populateSymptomsMenu() {{
        var container = document.getElementById("symptomsMenuContainer");
        container.innerHTML = "<div class='menu-header'>Common Symptoms</div>";
        for (var sym in symptoms) {{
            var item = document.createElement("div");
            item.className = "menu-item";
            item.textContent = sym;

            var icon = document.createElement("img");
            icon.className = "icon";
            icon.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
            item.appendChild(icon);

            (function(symName, iconElem, itemElem) {{
                itemElem.onclick = function() {{
                    if (itemElem.classList.contains("selected")) {{
                        itemElem.classList.remove("selected");
                        iconElem.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
                        showAllParts();
                    }} else {{
                        hideAllPartsIndividually();
                        resetSymptomsMenuSelection();
                        itemElem.classList.add("selected");
                        iconElem.src = "C:/Users/jsmith/Blender/User interface/icons/closed-eye.png";
                        symptoms[symName].forEach(id => api.show(id));
                    }}
                }};
            }})(sym, icon, item);

            container.appendChild(item);
        }}
    }}

    function resetSymptomsMenuSelection() {{
        var c = document.getElementById("symptomsMenuContainer");
        var items = c.getElementsByClassName("menu-item");
        for (var i = 0; i < items.length; i++) {{
            var sItem = items[i];
            var sIcon = sItem.getElementsByTagName("img")[0];
            sItem.classList.remove("selected");
            sIcon.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
        }}
    }}

    function toggleMenu() {{
        var m = document.getElementById("partMenuContainer");
        m.style.display = menuOpen ? "none" : "block";
        menuOpen = !menuOpen;
    }}

    function toggleSymptomsMenu() {{
        var m = document.getElementById("symptomsMenuContainer");
        m.style.display = symptomsMenuOpen ? "none" : "block";
        symptomsMenuOpen = !symptomsMenuOpen;
    }}

    function getMaxTextureSize() {{
        let maxTextureSize = 512;
        if (navigator.deviceMemory) {{
            const mem = navigator.deviceMemory;
            if (mem <= 2) {{
                maxTextureSize = 512;
            }} else if (mem <= 4) {{
                maxTextureSize = 1024;
            }} else if (mem <= 7) {{
                maxTextureSize = 2048;
            }} else {{
                maxTextureSize = 4096;
            }}
        }} else {{
            const ua = navigator.userAgent || navigator.vendor || window.opera;
            const isMobile = /android|iphone|ipad|ipod/i.test(ua);
            maxTextureSize = isMobile ? 512 : 1024;
        }}
        return maxTextureSize;
    }}

    var annotationsData = [];
    function filterAnnotations(api, ann) {{
        annotationsData = ann;
    }}
    function navigateToAnnotation(aName) {{
        var idx = annotationsData.findIndex(a => a.name.toLowerCase() === aName.toLowerCase());
        if (idx !== -1) {{
            api.gotoAnnotation(idx, {{}}, function(e){{}});
        }}
    }}

    window.onload = function() {{
        var placeholder = document.getElementById("placeholder-image");
        var iframe = document.getElementById("api-frame");

        iframe.onload = function() {{
            placeholder.style.display = "none";
        }};

        var uid = "{model_id}";
        var client = new Sketchfab(iframe);
        var maxTex = getMaxTextureSize();

        client.init(uid, {{
            success: function(apiInstance) {{
                api = apiInstance;
                api.start(function() {{
                    api.addEventListener('viewerready', function() {{
                        api.getAnnotationList(function(err, ann) {{
                            if (!err) {{
                                filterAnnotations(api, ann);
                            }}
                        }});
                    }});
                }});
            }},
            error: function(err) {{
                console.error("Sketchfab API error (symptom):", err);
            }},
            autostart: 0,
            preload: 1,
            max_texture_size: maxTex,
            transparent: 1,
            ui_watermark: 0,
            ui_infos: 0,
            ui_controls: 1,
            ui_annotations: 1,
            ui_settings: 0
        }});

        populateMainMenu();
        populateSymptomsMenu();

        document.getElementById("partMenuButton").addEventListener("click", function() {{
            toggleMenu();
        }});
        document.getElementById("symptomsMenuButton").addEventListener("click", function() {{
            toggleSymptomsMenu();
        }});
        document.getElementById("playIconButton").addEventListener("click", function() {{
            api.recenterCamera(function(err) {{
                if (!err) {{
                    showAllParts();
                    resetMenus();
                }}
            }});
        }});

        function resetMenus() {{
            var pmc = document.getElementById("partMenuContainer");
            var items = pmc.getElementsByClassName("menu-item");
            for (var i = 0; i < items.length; i++) {{
                var it = items[i];
                var ic = it.getElementsByTagName("img")[0];
                it.classList.remove("selected");
                ic.src = "C:/Users/jsmith/Blender/User interface/icons/open_eye.png";
            }}
            resetSymptomsMenuSelection();
        }}

        document.getElementById("thirdIconButton").addEventListener("click", function() {{
            var pop = document.getElementById("popup-container");
            var ifr = document.getElementById("popup-iframe");
            ifr.src = "https://docs.google.com/gview?url=https://partselectca-dsfph5cffxaaesb6.z01.azurefd.net/assets/manuals/EBF4AEBB8D1FC994820343DF54BFFE6BD3BA063D.pdf&embedded=true";
            pop.style.display = "block";
        }});
        document.getElementById("popup-iframe").onload = function() {{
            if (this.contentDocument && this.contentDocument.body.innerHTML.trim() === "") {{
                console.error("Failed to load PDF. Retrying...");
                this.src = this.src;
            }}
        }};
        document.getElementById("close-popup").addEventListener("click", function() {{
            var pop = document.getElementById("popup-container");
            var ifr = document.getElementById("popup-iframe");
            pop.style.display = "none";
            ifr.src = "";
        }});

        var searchInput = document.getElementById("searchInput");
        var suggestionBox = document.getElementById("suggestionBox");
        searchInput.addEventListener('input', function() {{
            var val = this.value.toLowerCase();
            var filtered = annotationsData.filter(a => a.name.toLowerCase().includes(val));
            suggestionBox.innerHTML = '';
            const maxS = 5;
            filtered.slice(0, maxS).forEach(a => {{
                var div = document.createElement('div');
                div.classList.add('suggestion-item');
                div.textContent = a.name;
                div.onclick = () => navigateToAnnotation(a.name);
                suggestionBox.appendChild(div);
            }});
            suggestionBox.style.display = filtered.length ? "block" : "none";
        }});
        document.addEventListener('click', function(e) {{
            if (!searchInput.contains(e.target) && !suggestionBox.contains(e.target)) {{
                suggestionBox.style.display = "none";
            }}
        }});
    }};
    """
    symptom_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Symptom Page</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
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
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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
            display: none;
            position: fixed;
            top: 25%;
            left: 29%;
            width: 42%;
            height: 42%;
            background-color: white;
            border: 2px solid #000;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
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
    </style>
</head>
<body>
    <div id="viewer-container">
        <img src="C:/Users/jsmith/Blender/User interface/icons/MicrosoftTeams-image (1).png"
             id="placeholder-image" alt="Placeholder Image">
        <iframe src="" id="api-frame"></iframe>
        <img src="C:/Users/jsmith/Blender/User interface/icons/dropdown_icon.png"
             id="partMenuButton" alt="Menu" draggable="false" title="Hide a section">
        <img src="C:/Users/jsmith/Blender/User interface/icons/reset.png"
             id="playIconButton" class="icon" alt="Reset" draggable="false" title="Reset View">
        <img src="C:/Users/jsmith/Blender/User interface/icons/manual.png"
             id="thirdIconButton" class="icon" draggable="false" title="View user manual">
        <img src="C:/Users/jsmith/Blender/User interface/icons/dropdown_icon.png"
             id="symptomsMenuButton" alt="Symptoms Menu" draggable="false" title="Hide all except symptom(s)">
        <div id="popup-container">
            <iframe src="" id="popup-iframe"></iframe>
            <button id="close-popup" style="position:absolute; top:5px; right:5px; background:#f00; color:#fff; border:none; cursor:pointer;">X</button>
        </div>
        <div id="partMenuContainer"></div>
        <div id="symptomsMenuContainer"></div>
        <input type="text" id="searchInput" placeholder="Search Parts">
        <div id="suggestionBox"></div>
    </div>
    <script src="https://static.sketchfab.com/api/sketchfab-viewer-1.12.1.js"></script>
    <script>
    {js_code}
    </script>
</body>
</html>
    """
    return symptom_html

##############################################################################
# 6) Tkinter UI
##############################################################################
app = tk.Tk()
app.title("Dual Normal/Symptom Pages")

# Globals for normal page
model_data_normal = {}
symptom_data_normal = {}
model_id_normal = ""

# Globals for symptom page
model_data_sym = {}
symptom_data_sym = {}
model_id_sym = ""

def load_normal_file():
    fp = filedialog.askopenfilename(filetypes=[("Text files","*.txt"), ("All files","*.*")])
    if not fp:
        return
    global model_data_normal, symptom_data_normal, model_id_normal
    model_id_normal = get_uid(fp)
    md, sd = parse_file(fp)
    model_data_normal = md
    symptom_data_normal = sd
    normal_html = generate_html_normal(model_id_normal, model_data_normal, symptom_data_normal)
    html_text_normal.delete("1.0", tk.END)
    html_text_normal.insert(tk.END, normal_html)

def load_symptom_file():
    fp = filedialog.askopenfilename(filetypes=[("Text files","*.txt"), ("All files","*.*")])
    if not fp:
        return
    global model_data_sym, symptom_data_sym, model_id_sym
    model_id_sym = get_uid(fp)
    md, sd = parse_file(fp)
    model_data_sym = md
    symptom_data_sym = sd
    sym_html = generate_html_symptom(model_id_sym, model_data_sym, symptom_data_sym)
    html_text_sym.delete("1.0", tk.END)
    html_text_sym.insert(tk.END, sym_html)

def open_normal_in_browser():
    content = html_text_normal.get("1.0", tk.END)
    with open("temp.html", "w", encoding="utf-8") as f:
        f.write(content)
    webbrowser.open(f'file://{os.path.realpath("temp.html")}')

def open_symptom_in_browser():
    content = html_text_sym.get("1.0", tk.END)
    with open("temp_symptom.html", "w", encoding="utf-8") as f:
        f.write(content)
    # Open in same window by setting location.href
    webbrowser.open(f'file://{os.path.realpath("temp_symptom.html")}', new=0)

# Layout
btn_frame = tk.Frame(app)
btn_frame.pack(pady=5)

btn_load_norm = tk.Button(btn_frame, text="Load Normal .txt", command=load_normal_file)
btn_load_norm.grid(row=0, column=0, padx=5)

btn_load_sym = tk.Button(btn_frame, text="Load Symptom .txt", command=load_symptom_file)
btn_load_sym.grid(row=0, column=1, padx=5)

btn_convert = tk.Button(btn_frame, text="Convert Paths", command=convert_and_update)
btn_convert.grid(row=0, column=2, padx=5)

btn_open_norm = tk.Button(btn_frame, text="Open Normal", command=open_normal_in_browser)
btn_open_norm.grid(row=0, column=3, padx=5)

btn_open_sym = tk.Button(btn_frame, text="Open Symptom", command=open_symptom_in_browser)
btn_open_sym.grid(row=0, column=4, padx=5)

tk.Label(app, text="Normal Page HTML Preview:").pack()
html_text_normal = tk.Text(app, width=100, height=15)
html_text_normal.pack()

tk.Label(app, text="Symptom Page HTML Preview:").pack()
html_text_sym = tk.Text(app, width=100, height=15)
html_text_sym.pack()

app.mainloop()
