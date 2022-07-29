var localstream, vancas, video, cxt, is_camera_aviable;
is_camera_aviable = false;

function turnOnCamera() {
  canvas = document.getElementById("canvas");
  cxt = canvas.getContext("2d");
  video = document.getElementById("video");

  if (!navigator.getUserMedia)
    navigator.getUserMedia =
      navigator.webkitGetUserMedia ||
      navigator.mozGetUserMedia ||
      navigator.msGetUserMedia;

  if (!window.URL) window.URL = window.webkitURL;

  if (navigator.getUserMedia) {
    navigator.getUserMedia(
      { video: true, audio: false },
      function (stream) {
        try {
          localstream = stream;
          video.srcObject = stream;
          video.play();
        } catch (error) {
          video.srcObject = null;
        }
      },
      function (err) {
        alert("Please enable permission to the camera and refresh the page");
      }
    );
  } else {
    alert("Media not available");
  }
}

function checkCamera() {
  if(video.srcObject == null){
    is_camera_aviable = false;
  }else if (!video.srcObject.active){
    is_camera_aviable = false;
  }else{
    is_camera_aviable = true;
  }
  return is_camera_aviable;
}

$(document).ready(function () {
  turnOnCamera();
});
