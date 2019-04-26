function swapNav() {
    var navBtn = document.getElementById('nav-button');
    navBtn.classList.toggle('nav-closed');
    navBtn.classList.toggle('nav-opened');
}

var getPercentage = function (presentTime, totalLength) {
    let calcPercentage = (presentTime / totalLength) * 100;
    return parseFloat(calcPercentage.toString());
};


function myTime(time) {
    var sec_min = '';
    var min = ~~(time / 60);
    var sec = ~~(time % 60);
    sec_min += '' + min + ':' + (sec < 10 ? '0' : '');
    sec_min += '' + sec;
    return sec_min;
}


function playSong(song_id) {
    var aud = $('#audio-' + song_id)[0];
    var length = aud.duration;
    var skbrOuter = $('.outer-' + song_id)[0];
    let updateTiming = function (s_id, flag = false) {
        var audio = $('#audio-' + s_id)[0];
        var time_info = $('#start-' + s_id)[0];
        var skbrInner = $('#progress-' + s_id)[0];

        if (flag) {
            time_info.innerHTML = '0:00';
            $(skbrInner).css('width', '0%');
            audio.currentTime = 0;
        } else {
            let seekBarPercentage = getPercentage(audio.currentTime.toFixed(2), audio.duration.toFixed(2));
            time_info.innerHTML = myTime(audio.duration - audio.currentTime);
            $(skbrInner).css('width', seekBarPercentage + '%');
        }
    };

    var interval;
    if (aud.paused) {
        var playing;
        if ((playing = $('.pause')[0])) {
            playing = playing.parentElement.id;
            if (playing != song_id) {
                $('#audio-' + playing)[0].pause();
                $('#audio-' + playing)[0].currentTime = 0;
                updateTiming(playing, true);
                toggleButtonClass(playing);
            }
        } else {
            var auds = $('audio');
            for (var i = 0; i < auds.length; i++) {
                if (auds[i].currentTime != 0 && auds[i].id != aud.id) {
                    updateTiming(auds[i].id.split('-')[1], true);
                }
            }
        }

        aud.play();
    } else {
        aud.pause();
    }
    toggleButtonClass(song_id);


    interval = setInterval(function () {

        if (!aud.paused) {
            updateTiming(song_id);
        }
        if (aud.ended) {
            clearInterval(interval);
            toggleButtonClass(song_id)
        }

    }, 550);

    skbrOuter.onclick = function(e){
        if (!aud.ended && length!==undefined){
            var seekPosition = e.pageX - $(skbrOuter).offset().left;
            if (
                seekPosition >= 0 &&
                seekPosition < $(skbrOuter).width()
            ){
                aud.currentTime =
                    parseFloat((seekPosition * aud.duration) / $(skbrOuter).width());
                updateTiming(song_id);
            }
        }
    };

}

function toggleButtonClass(song_id) {
    var btn = document.getElementById(song_id).childNodes[1].classList;
    btn.toggle('play');
    btn.toggle('pause');

}