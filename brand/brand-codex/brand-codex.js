(function () {
  // Light / dark is handled by the shared theme.js (loaded in <head>, [data-theme-toggle]).
  // This file runs the Sound section: two clip players and the six piano keys.
  'use strict';

  function fmt(s) {
    s = Math.max(0, Math.round(isFinite(s) ? s : 0));
    return Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2);
  }

  var players = [].slice.call(document.querySelectorAll('[data-player]'));
  players.forEach(function (p) {
    var audio = p.querySelector('audio');
    var btn = p.querySelector('button');
    var bar = p.querySelector('.bar');
    var fill = bar.querySelector('i');
    var time = p.querySelector('.time');
    var name = p.getAttribute('data-name');

    function show() {
      fill.style.width = (audio.duration ? audio.currentTime / audio.duration * 100 : 0) + '%';
      time.textContent = fmt(audio.currentTime) + ' / ' + fmt(audio.duration);
    }
    btn.addEventListener('click', function () {
      if (!audio.paused) { audio.pause(); return; }
      // one clip at a time
      players.forEach(function (o) { var a = o.querySelector('audio'); if (a !== audio) a.pause(); });
      audio.play();
    });
    audio.addEventListener('play', function () { p.classList.add('on'); btn.setAttribute('aria-label', 'Pause ' + name); });
    audio.addEventListener('pause', function () { p.classList.remove('on'); btn.setAttribute('aria-label', 'Play ' + name); });
    audio.addEventListener('ended', function () { audio.currentTime = 0; show(); });
    audio.addEventListener('loadedmetadata', show);
    audio.addEventListener('timeupdate', show);
    bar.addEventListener('click', function (e) {
      if (!audio.duration) return;
      var r = bar.getBoundingClientRect();
      audio.currentTime = Math.min(1, Math.max(0, (e.clientX - r.left) / r.width)) * audio.duration;
    });
  });

  // Each tap is a fresh Audio, so quick taps ring over each other like a real piano.
  [].forEach.call(document.querySelectorAll('[data-note]'), function (k) {
    k.addEventListener('click', function () {
      var a = new Audio('codex/key-' + k.getAttribute('data-note') + '.mp3');
      a.play();
      k.classList.add('hit');
      setTimeout(function () { k.classList.remove('hit'); }, 160);
    });
  });
})();
