// Sketchfab Viewer API: Start/Stop the viewer
var version = '1.12.1';
var uid = 'fff65f81c0e84592829813b939eedc05';
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
      var id = 4;
      var drumid = 1502;
      var controlpid = 307;
     
	  
	  var checkbox1 = document.querySelector("input[name=checkbox1]");
	  var checkbox2 = document.querySelector("input[name=checkbox2]");
	  var checkbox3 = document.querySelector("input[name=checkbox3]");
	  //var checkbox4 = document.querySelector("input[name=checkbox4]");
	 // var checkbox5 = document.querySelector("input[name=checkbox5]");
	  
 checkbox1.addEventListener('change', function() {
		if (this.checked) {
			api.show(id);
			api.hide(drumid);
			api.hide(controlpid);
		} else {
			//api.hide(id);
			api.show(drumid);
			api.show(controlpid);
		}
		});
		checkbox2.addEventListener('change', function() {
		if (this.checked) {
			api.show(drumid);
			api.hide(controlpid);
			api.hide(id);
		} else {
			//api.hide(drumid);
			api.show(id);
			api.show(controlpid);
		}
		});
			checkbox3.addEventListener('change', function() {
		if (this.checked) {
			api.show(controlpid);
			api.hide(id);
			api.hide(drumid);
		} else {
			//api.hide(controlpid);
			api.show(id);
			api.show(drumid);
		}
		});
		
				  
    });
  });
};
client.init(uid, {
  success: success,
  error: error,
  autostart: 1,
  preload: 1
});
//////////////////////////////////
// GUI Code
//////////////////////////////////
function initGui() {
  var controls = document.getElementById('controls');
  var buttonsText = '';
 buttonsText +=' <table style="width:100%">';
 buttonsText +=' <tr>';
 buttonsText +='  <th>Cabinet and Door Assembly</th>';
 buttonsText +=' <th>Drum and motor assembly</th>';
 buttonsText +=' <th>Control panel assembly</th>';
 buttonsText +=' </tr>';
  buttonsText +=' <tr>';
  buttonsText +='  <td><label class="switch">';
  buttonsText +='<input id="hidex" name="checkbox1" type="checkbox" checked>';
  buttonsText +=' <span class="slider round"></span>';
  buttonsText +='</label></td>';
  buttonsText +=' <td><label class="switch">';
  buttonsText +='<input id="hide2" name="checkbox2" type="checkbox" checked>';
  buttonsText +=' <span class="slider round"></span>';
  buttonsText +='</label></td>';
  buttonsText +=' <td><label class="switch">';
  buttonsText +='<input id="hide3" name="checkbox3" type="checkbox" checked>';
  buttonsText +=' <span class="slider round"></span>';
  buttonsText +='</label></td>';
  buttonsText +=' </tr>';
  buttonsText +='</table>';
  
  
  controls.innerHTML = buttonsText;
}
initGui();

//////////////////////////////////
// GUI Code end
//////////////////////////////////
