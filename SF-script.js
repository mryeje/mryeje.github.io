// Sketchfab Viewer API: Start/Stop the viewer
var version = '1.12.1';
var uid = '05f628525abb4ce3b5266725154e8bde';
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
      var id = 905;
      var drumid = 22;
      var baffelsid = 39;
      var cab = 21;
      // hide lid
      document.getElementById('hide').addEventListener('click', function () {
        api.hide(id);
      });
      // hide drum
      document.getElementById('hide2').addEventListener('click', function () {
        api.hide(drumid);
      });
      // hide baffles
      document.getElementById('hide2').addEventListener('click', function () {
        api.hide(baffelsid); 
      });
      // hide cabinet
          document.getElementById('hide3').addEventListener('click', function () {
        api.hide(baffelsid);
      });
      // show lid
      document.getElementById('show').addEventListener('click', function () {
        api.show(id);
      });
      // show drum
      document.getElementById('show2').addEventListener('click', function () {
        api.show(drumid);
      });
      //show baffles
         document.getElementById('show2').addEventListener('click', function () {
        api.show(baffelsid);
      });
      // show cabinet
        document.getElementById('show3').addEventListener('click', function () {
        api.show(baffelsid);
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
  buttonsText += '<button id="show">Show Lid</button>';
  buttonsText += '<button id="hide">Remove Lid</button>';
  buttonsText += '<button id="show2">Show Drum</button>';
  buttonsText += '<button id="hide2">Remove Drum</button>';
  buttonsText += '<button id="hide3">Remove Cabinet</button>';
  buttonsText += '<button id="show3">Show Cabinet</button>';
  controls.innerHTML = buttonsText;
}
initGui();

//////////////////////////////////
// GUI Code end
//////////////////////////////////
