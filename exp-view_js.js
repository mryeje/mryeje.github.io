// Sketchfab Viewer API: Start/Stop the viewer
var version = '1.12.1';
var uid = '21720d61652f4ca4b45c1e9e6f614203';
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
	  
	  
	  
      var cabinet_id = 4;
      var full_drum = 1674;
      var controlpid = 993;
	  var bracketID = 1496;
	  var door_intact=822;
	  var door_exp=603;
	  var blower_exp=2096;
	  var bulkhead = 2303;
	  var console_exp=100;
	  
	  api.hide(blower_exp);
	  api.hide(door_exp);
	  api.hide(console_exp);
	  
     
	  
	  var checkbox1 = document.querySelector("input[name=checkbox1]");
	  var checkbox2 = document.querySelector("input[name=checkbox2]");
	  var checkbox3 = document.querySelector("input[name=checkbox3]");
	  //var checkbox4 = document.querySelector("input[name=checkbox4]");
	 // var checkbox5 = document.querySelector("input[name=checkbox5]");
	  
		checkbox1.addEventListener('change', function() {
		if (this.checked) {
			api.show(cabinet_id);
			api.show(door_exp);
			api.hide(door_intact);
			api.hide(full_drum);
			api.hide(blower_exp);
			api.hide(bulkhead);
			api.hide(controlpid);
			api.hide(bracketID);
			api.hide(full_drum);
			api.hide(console_exp);
		} else {
			//api.hide(cabinet_id);
			api.show(full_drum);
			api.show(controlpid);
			api.hide(door_exp);
			api.show(door_intact);
			
		}
		});
		checkbox2.addEventListener('change', function() {
		if (this.checked) {
			api.show(full_drum);
			api.hide(bulkhead);
			api.show(door_exp);
			api.hide(door_intact);
			api.hide(controlpid);
			api.hide(cabinet_id);
			api.show(blower_exp);
			api.hide(door_exp);
			api.hide(console_exp);
			
		} else {
			
			api.show(cabinet_id);
			api.show(controlpid);
			api.show(door_intact);
			api.hide(blower_exp);
			
		}
		});
			checkbox3.addEventListener('change', function() {
		if (this.checked) {
			api.show(console_exp);
			api.hide(controlpid);
			api.hide(bracketID);
			api.hide(blower_exp);
			api.hide(cabinet_id);
			api.hide(bulkhead);
			api.hide(full_drum);
			api.hide(door_exp);
			api.hide(door_intact);
		} else {
			//api.hide(controlpid);
			api.show(cabinet_id);
			api.show(controlpid);
			api.show(full_drum);
			api.show(bracketID);
			api.hide(console_exp);
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

