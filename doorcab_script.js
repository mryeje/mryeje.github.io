// Sketchfab Viewer API: Start/Stop the viewer
var version = '1.12.1';
var uid = '78d6466c320a419a9fc9fdf6531021a2';
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
      var id = 14;
      var drumid = 762;
      var controlpid = 1376;
	  var bracketID = 1915;
     
	  
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
			api.hide(bracketID);
			api.hide(id);
			api.hide(drumid);
		} else {
			//api.hide(controlpid);
			api.show(id);
			api.show(drumid);
			api.show(bracketID);
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


//////////////////////////////////
// GUI Code end
//////////////////////////////////