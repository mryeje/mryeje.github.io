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
      document.getElementById('hide').addEventListener('click', function () {
        api.hide(id);
      });
      document.getElementById('show').addEventListener('click', function () {
        api.show(id);
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
  controls.innerHTML = buttonsText;
}
initGui();

//////////////////////////////////
// GUI Code end
//////////////////////////////////
