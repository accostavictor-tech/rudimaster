(function(){
"use strict";

// Evento opcional. O Vercel so registra eventos custom em plano Pro,
// entao aqui ele simplesmente nao faz nada ate voce migrar.
function track(name, data){
  try{ if (window.va) window.va('event', { name: name, data: data }); }catch(e){}
}

var lang = document.documentElement.dataset.lang || 'pt';
var D = window.RUDI_I18N[lang];

var els = {};
['play','playIcon','bpm','bpmOut','tap','counter','elapsed','hint','pad','theme','minus','plus',
 'segSub','beatsMinus','beatsPlus','beatsOut','volMet','optProg','progStep','progEvery','langBtn','langMenu']
 .forEach(function(id){ els[id] = document.getElementById(id); });

var bpm = 100, spb = 0.6, beats = 4, sub = 1;
var accents = [2,1,1,1];   // 2 acento, 1 normal, 0 mudo

var actx = null, master = null;
function audio(){
  if (!actx){
    actx = new (window.AudioContext || window.webkitAudioContext)();
    master = actx.createGain(); master.gain.value = 1; master.connect(actx.destination);
  }
  if (actx.state === 'suspended') actx.resume();
  return actx;
}
function click(time, kind){
  var base = Number(els.volMet.value)/100;
  var vol = base * (kind === 2 ? .5 : kind === 1 ? .3 : .13);
  if (vol <= 0) return;
  var osc = actx.createOscillator(), g = actx.createGain();
  osc.type = 'square';
  osc.frequency.setValueAtTime(kind === 2 ? 1760 : kind === 1 ? 1174 : 880, time);
  g.gain.setValueAtTime(.0001, time);
  g.gain.exponentialRampToValueAtTime(vol, time + .002);
  g.gain.exponentialRampToValueAtTime(.0001, time + (kind === 3 ? .022 : .035));
  osc.connect(g); g.connect(master);
  osc.start(time); osc.stop(time + .06);
}

var playing = false, anchorTime = 0, anchorTick = 0, nextTick = 0;
var timer = null, wake = null, startedAt = 0, visual = [];

function tickTime(t){ return anchorTime + (t - anchorTick) * (spb / sub); }
function nowTick(){ return actx ? anchorTick + (actx.currentTime - anchorTime) / (spb / sub) : 0; }

function setBpm(v, live){
  v = Math.max(30, Math.min(300, Math.round(v)));
  bpm = v; els.bpmOut.textContent = v; els.bpm.value = v;
  if (playing && live){ anchorTick = nowTick(); anchorTime = actx.currentTime; }
  spb = 60 / v;
}
function lock(on){
  try{
    if (on && 'wakeLock' in navigator && !wake) navigator.wakeLock.request('screen').then(function(w){ wake = w; }, function(){});
    else if (!on && wake){ wake.release(); wake = null; }
  }catch(e){}
}

function start(){
  audio(); spb = 60 / bpm;
  anchorTick = 0; anchorTime = actx.currentTime + .12; nextTick = 0;
  startedAt = anchorTime; visual = []; playing = true;
  els.playIcon.innerHTML = '<rect x="6" y="5" width="4.5" height="14" rx="1"/><rect x="13.5" y="5" width="4.5" height="14" rx="1"/>';
  els.play.setAttribute('aria-label', D.stop);
  timer = setInterval(schedule, 25); schedule(); lock(true);
  document.body.classList.add('is-playing');
  track('practice_start', { mode: 'metronome', beats: beats, subdivision: sub, bpm: bpm });
}
function stop(){
  playing = false; clearInterval(timer); timer = null; visual = [];
  els.playIcon.innerHTML = '<path d="M7 4l13 8-13 8z"/>';
  els.play.setAttribute('aria-label', D.play);
  lock(false); document.body.classList.remove('is-playing');
}
function restart(){ if (playing){ stop(); start(); } }

function schedule(){
  if (!playing) return;
  var horizon = actx.currentTime + .14, per = beats * sub;
  while (tickTime(nextTick) < horizon){
    var t = nextTick, inBar = ((t % per) + per) % per;
    var beatIdx = Math.floor(inBar / sub), isBeat = (inBar % sub) === 0;
    var kind = isBeat ? accents[beatIdx] : 3;
    var when = tickTime(t);

    if (inBar === 0 && t > 0 && els.optProg.checked){
      var bar = Math.round(t / per);
      var every = Math.max(1, Number(els.progEvery.value) || 8);
      if (bar % every === 0){
        var nv = Math.min(300, bpm + (Number(els.progStep.value) || 4));
        if (nv !== bpm){
          bpm = nv; els.bpm.value = nv; els.bpmOut.textContent = nv;
          anchorTick = t; anchorTime = when; spb = 60 / nv;
        }
      }
    }
    if (kind !== 0) click(when, kind);
    if (isBeat) visual.push({ t: when, i: beatIdx, k: kind });
    nextTick = t + 1;
  }
}

var lugs = [];
function buildLugs(){
  lugs.forEach(function(l){ l.remove(); }); lugs = [];
  var r = 75;
  for (var i=0;i<beats;i++){
    var a = (-90 + i*360/beats) * Math.PI/180;
    var b = document.createElement('button');
    b.className = 'lug tap';
    b.dataset.i = i;
    b.setAttribute('aria-label', String(i+1));
    b.style.setProperty('--tx', (Math.cos(a)*r).toFixed(1) + 'px');
    b.style.setProperty('--ty', (Math.sin(a)*r).toFixed(1) + 'px');
    b.addEventListener('click', function(e){
      e.stopPropagation();
      var k = Number(this.dataset.i);
      accents[k] = (accents[k] + 2) % 3;   // 1 -> 0 -> 2 -> 1
      paintLugs();
    });
    els.pad.appendChild(b); lugs.push(b);
  }
  paintLugs();
}
function paintLugs(active){
  for (var i=0;i<lugs.length;i++){
    var s = accents[i];
    lugs[i].className = 'lug tap' + (s === 2 ? ' acc' : s === 0 ? ' mute' : '') + (i === active ? ' on' : '');
  }
}
function setBeats(n){
  n = Math.max(1, Math.min(12, n));
  var old = accents.slice();
  accents = [];
  for (var i=0;i<n;i++) accents.push(i < old.length ? old[i] : 1);
  if (accents[0] === 1) accents[0] = 2;
  beats = n; els.beatsOut.textContent = n;
  buildLugs(); restart();
}

function pad2(n){ return (n < 10 ? '0' : '') + n; }
function frame(){
  requestAnimationFrame(frame);
  if (!playing){
    els.counter.textContent = '—'; els.elapsed.textContent = '00:00';
    els.hint.textContent = D.start; els.pad.classList.remove('pulse');
    paintLugs(); return;
  }
  var t = actx.currentTime, cur = null;
  while (visual.length && visual[0].t < t - .2) visual.shift();
  for (var i=0;i<visual.length;i++){
    if (visual[i].t <= t){ cur = visual[i]; } else break;
  }
  var flash = cur && (t - cur.t) < .085;
  els.pad.classList.toggle('pulse', !!flash);
  paintLugs(cur ? cur.i : -1);
  var bar = Math.floor(nowTick() / (beats * sub)) + 1;
  els.counter.textContent = D.bar + ' ' + Math.max(1, bar);
  var s = Math.max(0, Math.floor(t - startedAt));
  els.elapsed.textContent = pad2(Math.floor(s/60)) + ':' + pad2(s%60);
  els.hint.textContent = '';
}

Array.prototype.forEach.call(els.segSub.children, function(b){
  b.addEventListener('click', function(){
    sub = Number(b.dataset.v);
    Array.prototype.forEach.call(els.segSub.children, function(c){ c.setAttribute('aria-pressed', String(c === b)); });
    restart();
  });
});
els.beatsMinus.addEventListener('click', function(){ setBeats(beats - 1); });
els.beatsPlus.addEventListener('click', function(){ setBeats(beats + 1); });
els.play.addEventListener('click', function(){ playing ? stop() : start(); });
els.bpm.addEventListener('input', function(){ setBpm(Number(els.bpm.value), true); });

function nudge(d){ setBpm(bpm + d, true); }
function holdable(el, d){
  var to = null, iv = null;
  el.addEventListener('pointerdown', function(e){
    e.preventDefault(); nudge(d);
    to = setTimeout(function(){ iv = setInterval(function(){ nudge(d); }, 90); }, 420);
  });
  ['pointerup','pointerleave','pointercancel'].forEach(function(ev){
    el.addEventListener(ev, function(){ clearTimeout(to); clearInterval(iv); });
  });
}
holdable(els.minus, -5); holdable(els.plus, 5);

els.tap.addEventListener('click', (function(){
  var taps = [];
  return function(){
    var now = performance.now();
    if (taps.length && now - taps[taps.length-1] > 2200) taps = [];
    taps.push(now); if (taps.length > 5) taps.shift();
    if (taps.length >= 2){
      var sum = 0; for (var i=1;i<taps.length;i++) sum += taps[i]-taps[i-1];
      setBpm(60000 / (sum/(taps.length-1)), true);
    }
  };
})());

els.langBtn.addEventListener('click', function(e){ e.stopPropagation(); els.langMenu.classList.toggle('open'); });
document.addEventListener('click', function(){ els.langMenu.classList.remove('open'); });
els.theme.addEventListener('click', function(){
  var n = document.documentElement.dataset.theme === 'night' ? 'paper' : 'night';
  document.documentElement.dataset.theme = n;
  var m = document.querySelector('meta[name=theme-color]');
  if (m) m.content = n === 'night' ? '#121110' : '#E7DFCC';
  try{ localStorage.setItem('rudi-theme', n); }catch(e){}
});
document.addEventListener('keydown', function(e){
  var tag = e.target.tagName;
  if (tag === 'INPUT' || tag === 'SELECT' || tag === 'TEXTAREA') return;
  if (e.code === 'Space'){ e.preventDefault(); playing ? stop() : start(); }
  if (e.code === 'ArrowUp'){ e.preventDefault(); nudge(e.shiftKey ? 5 : 1); }
  if (e.code === 'ArrowDown'){ e.preventDefault(); nudge(e.shiftKey ? -5 : -1); }
});
document.addEventListener('visibilitychange', function(){ if (!document.hidden && playing) lock(true); });

els.play.setAttribute('aria-label', D.play);
setBeats(4); setBpm(100, false); frame();
})();
