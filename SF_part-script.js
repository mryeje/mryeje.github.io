// Sketchfab Viewer API: Start/Stop the viewer
var version = '1.12.1';
var uid = '33f92a5fa55343e1a83ad30b5dc34fee';
var iframe = document.getElementById('api-frame');
var client = new window.Sketchfab(version, iframe);
var id = 60;
var lenid = 29;
var widthid = 46;
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
     
	  api.hide(id);
	  api.hide(lenid);
	  api.hide(widthid);
	  
	  var checkbox1 = document.querySelector("input[name=checkbox1]");
	  var checkbox2 = document.querySelector("input[name=checkbox2]");
	  var checkbox3 = document.querySelector("input[name=checkbox3]");

	  
	  checkbox1.addEventListener('change', function() {
		if (this.checked) {
			api.show(id);
		} else {
			api.hide(id);
		}
		});
		checkbox2.addEventListener('change', function() {
		if (this.checked) {
			api.show(lenid);
		
		} else {
			api.hide(lenid);
			
		}
		});
		checkbox3.addEventListener('change', function() {
		if (this.checked) {
			api.show(widthid);
		} else {
			api.hide(widthid);
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
 buttonsText +='  <th>Height</th>';
 buttonsText +=' <th>Length</th>';
 buttonsText +=' <th>Width</th>';
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
initGui();

//////////////////////////////////
// GUI Code end
//////////////////////////////////


