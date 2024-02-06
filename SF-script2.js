// Sketchfab Viewer API: Start/Stop the viewer
var version = '1.12.1';
var uid = '0993ac8fb3e548b49460cd40186f0bbc';
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
      var id = 1143;
      var drumid = 4335;
      var baffelsid = 4349;
      var cabid = 1129;
      var consoleid=84;
      var conbrkid=3391;
	  
	  var checkbox1 = document.querySelector("input[name=checkbox1]");
	  var checkbox2 = document.querySelector("input[name=checkbox2]");
	  var checkbox3 = document.querySelector("input[name=checkbox3]");
	  var checkbox4 = document.querySelector("input[name=checkbox4]");
	  var checkbox5 = document.querySelector("input[name=checkbox5]");
	  
	  checkbox1.addEventListener('change', function() {
		if (this.checked) {
			api.show(id);
		} else {
			api.hide(id);
		}
		});
		checkbox2.addEventListener('change', function() {
		if (this.checked) {
			api.show(drumid);
			api.show(baffelsid);
		} else {
			api.hide(drumid);
			api.hide(baffelsid);
		}
		});
		checkbox3.addEventListener('change', function() {
		if (this.checked) {
			api.show(cabid);
		} else {
			api.hide(cabid);
		}
		});
		checkbox4.addEventListener('change', function() {
		if (this.checked) {
			api.show(consoleid);
		} else {
			api.hide(consoleid);
		}
		});
		checkbox5.addEventListener('change', function() {
		if (this.checked) {
			api.show(conbrkid);
		} else {
			api.hide(conbrkid);
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
 buttonsText +='  <th>Lid</th>';
 buttonsText +=' <th>Drum</th>';
 buttonsText +=' <th>Cabinet</th>';
 buttonsText +=' <th>Console</th>';
 buttonsText +=' <th>Console bracket</th>';
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
  buttonsText +=' <td><label class="switch">';
  buttonsText +='<input id="hide3" name="checkbox4" type="checkbox" checked>';
  buttonsText +=' <span class="slider round"></span>';
  buttonsText +='</label></td>';
  buttonsText +=' <td><label class="switch">';
  buttonsText +='<input id="hide3" name="checkbox5" type="checkbox" checked>';
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
