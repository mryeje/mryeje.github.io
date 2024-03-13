// Sketchfab Viewer API: Start/Stop the viewer
var version = '1.12.1';
var uid = '4e23eadc76844c0ebf6582699c9c25b2';
var iframe = document.getElementById('api-frame');
var client = new window.Sketchfab(version, iframe);
var error = function error() {
    console.error('Sketchfab API error');
};
var success = function success(api) {
  api.start(function () {
    api.addEventListener('viewerready', function () {
      api.getSceneGraph(function (err, result) {
        if (err) {
          console.log('Error getting nodes');
          return;
        }
        // get the id from that log
        console.log(result);
      });
	  
	document.getElementById('resetcam').addEventListener('click', function () {
        api.focusOnVisibleGeometries(function (err) {
          if (err) return;
        });
      });  
	  
		var id = 4;
      var drumid = 972;
      var controlpid = 291;
	  var bracketID = 794;
	  
	 
	  
     
	  
	  var checkbox1 = document.querySelector("input[name=checkbox1]");
	  var checkbox2 = document.querySelector("input[name=checkbox2]");
	  var checkbox3 = document.querySelector("input[name=checkbox3]");
	  //var checkbox4 = document.querySelector("input[name=checkbox4]");
	 // var checkbox5 = document.querySelector("input[name=checkbox5]");
	  
		checkbox1.addEventListener('change', function() {
		if (this.checked) {
			api.show(id);
			//api.show(door_exp);
			//api.hide(door_intact);
			api.hide(drumid);
			//api.hide(blower_exp);
			//api.hide(bulkhead);
			api.hide(controlpid);
			api.hide(bracketID);
			api.hide(drumid);
			//api.hide(console_exp);
			checkbox2.checked = false;
			checkbox3.checked = false;
		} else {
			api.hide(id);
			api.show(drumid);
			api.show(controlpid);
			//api.hide(door_exp);
			//api.show(door_intact);
			
		}
		});
		checkbox2.addEventListener('change', function() {
		if (this.checked) {
			api.show(drumid);
			//api.hide(bulkhead);
			//api.show(door_exp);
			//api.hide(door_intact);
			api.hide(controlpid);
			api.hide(id);
			//api.show(blower_exp);
			//api.hide(door_exp);
			//api.hide(console_exp);
			checkbox1.checked = false;
			checkbox3.checked = false;
			
		} else {
			
			api.show(id);
			api.show(controlpid);
			//api.show(door_intact);
			//api.hide(blower_exp);
			
		}
		});
			checkbox3.addEventListener('change', function() {
		if (this.checked) {
			//api.show(console_exp);
			api.show(controlpid);
			api.show(bracketID);
			//api.hide(blower_exp);
			api.hide(id);
			//api.hide(bulkhead);
			api.hide(drumid);
			//api.hide(door_exp);
			//api.hide(door_intact);
			checkbox1.checked = false;
			checkbox2.checked = false;
		} else {
			//api.hide(controlpid);
			api.show(id);
			api.show(controlpid);
			api.show(drumid);
			//api.hide(bracketID);
			//api.hide(console_exp);
			//api.show(door_intact);
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
  max_texture_size:512,
  transparent:1,
  ui_watermark:0,
  ui_infos:0,
  ui_controls:1,
  ui_annotations:1,
  ui_settings:0,
  ui_ar_qrcode:0,
  ui_ar_help:0,
  ui_help:0,
  ui_ar:0,
  ui_vr:0,
  ui_fullscreen:0,
  ui_inspector:0
});


//////////////////////////////////
// GUI Code
//////////////////////////////////
function initGui() {
  var controls = document.getElementById('controls');
  var buttonsText = '';
  //buttonsText +='<span id="orbit"><img src="orbit.png"><img src="pinch.png"><img src="2fdrag.png"></span>';
 buttonsText +=' <table style="width:100%">';
 buttonsText +=' <tr>';
 buttonsText +='  <th>Cabinet & Door Assembly</th>';
 buttonsText +=' <th>Drum & Motor Assembly</th>';
 buttonsText +=' <th>Control panel</th>';
 buttonsText +=' </tr>';
  buttonsText +=' <tr>';
  buttonsText +='  <td><label class="switch">';
  buttonsText +='<input id="hidex" name="checkbox1" type="checkbox">';
  buttonsText +=' <span class="slider round"></span>';
  buttonsText +='</label></td>';
  buttonsText +=' <td><label class="switch">';
  buttonsText +='<input id="hide2" name="checkbox2" type="checkbox">';
  buttonsText +=' <span class="slider round"></span>';
  buttonsText +='</label></td>';
  buttonsText +=' <td><label class="switch">';
  buttonsText +='<input id="hide3" name="checkbox3" type="checkbox">';
  buttonsText +=' <span class="slider round"></span>';
  buttonsText +='</label></td>';
  buttonsText +=' </tr>';
  buttonsText +='</table>';
  
  
  controls.innerHTML = buttonsText;
}
function showOrbit() {
  var x = document.getElementById("orbit");
  var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  
  if (isMobile) {
    x.style.visibility = 'visible';
  } else {
    x.style.visibility = 'hidden';
  }
}

showOrbit(); // Call the function to initially set the visibility
initGui();

//////////////////////////////////
// GUI Code end
//////////////////////////////////
