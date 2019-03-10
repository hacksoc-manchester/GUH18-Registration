var gCtx = null;
var gCanvas = null;

var vidhtml = '<video id="hardware-qr-scanner" width:"100%" autoplay></video>';

function initCanvas(w, h) {
    gCanvas = document.getElementById("qr-canvas");
    gCanvas.style.width = w + "px";
    gCanvas.style.height = h + "px";
    gCanvas.width = w;
    gCanvas.height = h;
    gCtx = gCanvas.getContext("2d");
    gCtx.clearRect(0, 0, w, h);
}

function read(a) {
    location.href = a
}

function isCanvasSupported() {
    var elem = document.createElement('canvas');
    return !!(elem.getContext && elem.getContext('2d'));
}

function load() {
    if (isCanvasSupported() && window.File && window.FileReader) {
        initCanvas(800, 600);
        startQRScanner(read);
    }
    else {
        document.getElementById("error").style.display = "inline";
        document.getElementById("error").innerHTML = '<p id="mp1">QR code scanner for HTML5 capable browsers</p><br>' +
            '<br><p id="mp2">sorry your browser is not supported</p><br><br>' +
            '<p id="mp1">try <a href="http://www.mozilla.com/firefox"><img src="firefox.png"/></a> or <a href="http://chrome.google.com"><img src="chrome_logo.gif"/></a> or <a href="http://www.opera.com"><img src="Opera-logo.png"/></a></p>';
    }
}

function couldNotStartCamera() {
    $.notify({
      message: 'Could not start webcam!'
    }, {
        type: 'danger'
    });
  }

function startQRScanner(callback) {
    closeScanner();
    scanner = new Instascan.Scanner({ video: document.getElementById('hardware-qr-scanner'), mirror: false });
    scanner.addListener('scan', function (content) {
      callback(content);
    });
    Instascan.Camera.getCameras().then(function (cameras) {
      if (cameras.length > 0) {
        maxCameras = cameras.length;
        camera = cameras[camera_option];
        scanner.start(camera);
      } else {
        couldNotStartCamera();
      }
    }).catch(function (e) {
      couldNotStartCamera();
      console.error(e);
    });
  }

