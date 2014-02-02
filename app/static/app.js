$(function() {
    if ("WebSocket" in window) {
                cam = new WebSocket("ws://" + document.domain + ":5000/camera");
                cam.onmessage = function (msg) {
                    $("#cam").attr('src', 'data:image/jpg;base64,' + msg.data);
                };
                cam.onerror = function(e) {
                    console.log(e);
                }
            } else {
                alert("WebSocket not supported");
            }
    });
