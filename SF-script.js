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
      var id = 1124;
      var drumid = 4319;
      var baffelsid = 4333;
      var cabid = 1110;
      var consoleid=78;
      var conbrkid=3373;
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
        api.hide(cabid);
      });
      // hide console
          document.getElementById('hide4').addEventListener('click', function () {
        api.hide(consoleid);
      });
        // hide console bracket
      document.getElementById('hide5').addEventListener('click', function () {
      api.hide(conbrkid);
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
        api.show(cabid);
      });
         // show console
        document.getElementById('show4').addEventListener('click', function () {
        api.show(consoleid);
      });
        // show console bracket
        document.getElementById('show5').addEventListener('click', function () {
        api.show(conbrkid);
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
  buttonsText += '<button id="hide4">Remove Console</button>';
  buttonsText += '<button id="show4">Show Console</button>';
  buttonsText += '<button id="hide5">Remove Console bracket</button>';
  buttonsText += '<button id="show5">Show Console bracket</button>';
  controls.innerHTML = buttonsText;
}
initGui();

//////////////////////////////////
// GUI Code end
//////////////////////////////////
