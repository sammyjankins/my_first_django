"use strict";
function swapclass(class_name) {
    var btnn = document.getElementById(class_name);
    btnn.childNodes[1].childNodes[1].classList.toggle('play');
    btnn.childNodes[1].childNodes[1].classList.toggle('pause');
}