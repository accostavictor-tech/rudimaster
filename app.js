(function(){
"use strict";

// Evento opcional. O Vercel so registra eventos custom em plano Pro,
// entao aqui ele simplesmente nao faz nada ate voce migrar.
function track(name, data){
  try{ if (window.va) window.va('event', { name: name, data: data }); }catch(e){}
}

function build(st, dur, acc, gr){
  acc = acc || []; gr = gr || {};
  var c = st.replace(/\s/g,'').split(''), out = [];
  for (var i=0;i<c.length;i++) out.push({ s:c[i], d:(typeof dur === 'number') ? dur : dur[i], a:acc.indexOf(i)>=0, g:gr[i]||0 });
  return out;
}
var E = 1e-6, T3 = 1/3, T6 = 1/6;
var R5 = [.25,.25,.25,.25,.5,.25,.25,.25,.25,.5];
var R7 = [.25,.25,.25,.25,.25,.25,.5,.25,.25,.25,.25,.25,.25,.5];
var R9 = [.25,.25,.25,.25,.25,.25,.25,.25,.5,.25,.25,.25,.25,.25,.25,.25,.25,.5];

var RUDIMENTS = window.RUDIMENT_PATTERNS = [
  { id:'s1', cat:'roll', notes: build('RLRLRLRL', .25) },
  { id:'s2', cat:'roll', notes: build('RRLLRRLL', .25) },
  { id:'s3', cat:'roll', notes: build('RRRLLLRRRLLL', T6) },
  { id:'r5', cat:'roll', notes: build('RRLLR LLRRL', R5, [4,9]) },
  { id:'r6', cat:'roll', notes: build('RLLRRL LRRLLR', T6, [0,5,6,11]) },
  { id:'r7', cat:'roll', notes: build('RRLLRRL LLRRLLR', R7, [6,13]) },
  { id:'r9', cat:'roll', notes: build('RRLLRRLLR LLRRLLRRL', R9, [8,17]) },
  { id:'p1', cat:'para', notes: build('RLRR LRLL', .25, [0,4]) },
  { id:'p2', cat:'para', notes: build('RLRLRR LRLRLL', T6, [0,6]) },
  { id:'p3', cat:'para', notes: build('RLRLRLRR LRLRLRLL', .25, [0,8]) },
  { id:'pd', cat:'para', notes: build('RLRRLL RLRRLL', T6, [0,6]) },
  { id:'f1', cat:'flam', notes: build('RLRL', 1, [], {0:1,1:1,2:1,3:1}) },
  { id:'f2', cat:'flam', notes: build('RRLL', .5, [0,2], {0:1,2:1}) },
  { id:'f3', cat:'flam', notes: build('RLRLRL', T3, [0,3], {0:1,3:1}) },
  { id:'f4', cat:'flam', notes: build('RLRLR LRLRL', R5, [1,6], {0:1,4:1,5:1,9:1}) },
  { id:'d1', cat:'drag', notes: build('RLRL', 1, [], {0:2,1:2,2:2,3:2}) },
  { id:'d2', cat:'drag', notes: build('RLLR', .5, [1,3], {0:2,2:2}) },
  { id:'d3', cat:'drag', notes: build('RLRL LRLR', [T6,T6,T6,.5, T6,T6,T6,.5], [3,7], {0:2,4:2}) }
];

var SIGS = [ {id:'4/4',beats:4,click:1}, {id:'3/4',beats:3,click:1}, {id:'2/4',beats:2,click:1}, {id:'5/4',beats:5,click:1}, {id:'6/8',beats:3,click:1.5} ];

function beamsFor(d){
  if (d >= 1-E) return 0;
  if (d >= .5-E) return 1;
  if (Math.abs(d-T3) < .01) return 1;
  if (d >= .25-E) return 2;
  if (Math.abs(d-T6) < .01) return 2;
  return 3;
}
function tupletOf(d){ return Math.abs(d-T3)<.01 ? 3 : (Math.abs(d-T6)<.01 ? 6 : 0); }
function figKey(d){
  if (d >= 1-E) return 'q';
  if (d >= .5-E) return 'e';
  if (Math.abs(d-T3) < .01) return 't';
  if (d >= .25-E) return 's';
  return 'x';
}
function compile(rud){
  var notes = [], at = 0, tally = {};
  for (var i=0;i<rud.notes.length;i++){
    var n = rud.notes[i];
    notes.push({ s:n.s, d:n.d, a:n.a, g:n.g, at:at, b:beamsFor(n.d), t:tupletOf(n.d) });
    tally[n.d] = (tally[n.d]||0) + 1; at += n.d;
  }
  var groups = [], cur = null;
  for (var j=0;j<notes.length;j++){
    var nt = notes[j], idx = Math.floor(nt.at + E);
    if (nt.b === 0){ cur = null; continue; }
    if (!cur || cur.beat !== idx || cur.b !== nt.b){ cur = {beat:idx,b:nt.b,t:nt.t,from:j,to:j}; groups.push(cur); }
    else cur.to = j;
  }
  for (var gi=0; gi<groups.length; gi++) if (groups[gi].t) groups[gi].t = groups[gi].to - groups[gi].from + 1;
  var top = 0, topD = .25;
  for (var k in tally) if (tally[k] > top){ top = tally[k]; topD = Number(k); }
  return { notes:notes, len:Math.round(at*1000)/1000, groups:groups, fig:figKey(topD) };
}
window.RUDI_COMPILE = compile;

var els = {};
['score','lamp','play','playIcon','bpm','bpmOut','bpmUnit','tap','rudName','rudStick','rudMeta','counter','hint',
 'pad','stripTag','theme','minus','plus','segSig','segHand','volRud','volMet','langBtn','langMenu',
 'optMet','optRud','optStick','optCount','optProg','progStep','progEvery','prev','next','openPicker','overlay',
 'rudList','search','play']
 .forEach(function(id){ els[id] = document.getElementById(id); });

var lang = document.documentElement.dataset.lang || 'pt';
var D = window.RUDI_I18N[lang];
var idx = 7, current = RUDIMENTS[idx], pattern = compile(current);
var sig = SIGS[0], bpm = 100, spb = .6, hand = 'R';

function letter(s){
  var sw = hand === 'R' ? s : (s === 'R' ? 'L' : 'R');
  return D.letters[sw];
}
function secPerBeat(v){ return (60 / v) / sig.click; }

function stickingHtml(p){
  var out = [], last = 0;
  for (var i=0;i<p.notes.length && i<20;i++){
    var n = p.notes[i];
    if (i > 0 && Math.floor(n.at+E) !== Math.floor(last+E)) out.push('<span style="opacity:.35">|</span>');
    out.push(n.a ? '<i>' + letter(n.s) + '</i>' : letter(n.s));
    last = n.at;
  }
  if (p.notes.length > 20) out.push('…');
  return out.join(' ');
}
function describe(){
  els.rudName.textContent = D.names[current.id];
  els.rudStick.innerHTML = stickingHtml(pattern);
  els.rudMeta.textContent = D.figs[pattern.fig] + ' · ' + pattern.len + ' ' + D.beats + ' · ' + pattern.notes.length + ' ' + D.strokes;
  els.stripTag.textContent = sig.id;
  els.bpmUnit.textContent = sig.click === 1.5 ? D.unit8 : D.unit4;
}

var actx = null, noise = null, master = null;
function audio(){
  if (!actx){
    actx = new (window.AudioContext || window.webkitAudioContext)();
    master = actx.createGain(); master.gain.value = 1; master.connect(actx.destination);
    var len = Math.floor(actx.sampleRate * .5);
    noise = actx.createBuffer(1, len, actx.sampleRate);
    var d = noise.getChannelData(0);
    for (var i=0;i<len;i++) d[i] = Math.random()*2-1;
  }
  if (actx.state === 'suspended') actx.resume();
  return actx;
}
function hit(time, accent, grace, side){
  var vol = (Number(els.volRud.value)/100) * (grace ? .3 : (accent ? 1 : .55));
  if (vol <= 0) return;
  var src = actx.createBufferSource(); src.buffer = noise;
  var bp = actx.createBiquadFilter(); bp.type = 'bandpass';
  bp.frequency.value = accent ? 2600 : 1700; bp.Q.value = .9;
  var g = actx.createGain(), dur = grace ? .03 : (accent ? .075 : .05);
  g.gain.setValueAtTime(.0001, time);
  g.gain.exponentialRampToValueAtTime(Math.max(.001, vol*.5), time + .002);
  g.gain.exponentialRampToValueAtTime(.0001, time + dur);
  src.connect(bp); bp.connect(g);
  if (side && actx.createStereoPanner){
    var pan = actx.createStereoPanner();
    var right = (side === 'R') === (hand === 'R');
    pan.pan.value = right ? .35 : -.35;
    g.connect(pan); pan.connect(master);
  } else g.connect(master);
  src.start(time); src.stop(time + dur + .02);
}
function click(time, first){
  var vol = (Number(els.volMet.value)/100) * (first ? .5 : .3);
  if (vol <= 0) return;
  var osc = actx.createOscillator(), g = actx.createGain();
  osc.type = 'square'; osc.frequency.setValueAtTime(first ? 1760 : 1174, time);
  g.gain.setValueAtTime(.0001, time);
  g.gain.exponentialRampToValueAtTime(vol, time + .002);
  g.gain.exponentialRampToValueAtTime(.0001, time + .035);
  osc.connect(g); g.connect(master); osc.start(time); osc.stop(time + .06);
}

var playing = false, anchorTime = 0, anchorBeat = 0;
var nextNoteBeat = 0, nextNoteIdx = 0, nextClickBeat = 0, cycles = 0;
var visual = [], timer = null, measures = 0, wake = null, lead = 0;

function beatToTime(b){ return anchorTime + (b - anchorBeat) * spb; }
function nowBeat(){ return actx ? anchorBeat + (actx.currentTime - anchorTime) / spb : 0; }
function setBpm(v, live){
  v = Math.max(30, Math.min(280, Math.round(v)));
  bpm = v; els.bpmOut.textContent = v; els.bpm.value = v;
  if (playing && live){ anchorBeat = nowBeat(); anchorTime = actx.currentTime; }
  spb = secPerBeat(v);
}
function lock(on){
  try{
    if (on && 'wakeLock' in navigator && !wake){
      navigator.wakeLock.request('screen').then(function(w){ wake = w; }, function(){});
    } else if (!on && wake){ wake.release(); wake = null; }
  }catch(e){}
}
function start(){
  audio(); spb = secPerBeat(bpm);
  measures = 0; cycles = 0; nextNoteIdx = 0; visual = [];
  lead = els.optCount.checked ? sig.beats : 0;
  anchorBeat = -lead; anchorTime = actx.currentTime + .14;
  nextNoteBeat = 0; nextClickBeat = -lead; playing = true;
  els.playIcon.innerHTML = '<rect x="6" y="5" width="4.5" height="14" rx="1"/><rect x="13.5" y="5" width="4.5" height="14" rx="1"/>';
  els.play.setAttribute('aria-label', D.stop);
  timer = setInterval(schedule, 25); schedule(); lock(true);
  document.body.classList.add('is-playing');
  track('practice_start', { mode: 'rudiment', rudiment: current.id, bpm: bpm });
}
function stop(){
  playing = false; clearInterval(timer); timer = null; visual = [];
  els.playIcon.innerHTML = '<path d="M7 4l13 8-13 8z"/>';
  els.play.setAttribute('aria-label', D.play);
  lock(false); document.body.classList.remove('is-playing'); paint(0);
}
function restart(){ if (playing){ stop(); start(); } }

function schedule(){
  if (!playing) return;
  var horizon = actx.currentTime + .14;
  while (beatToTime(nextClickBeat) < horizon){
    var b = nextClickBeat;
    if (b >= -E && Math.abs(b % sig.beats) < 1e-4){
      measures++;
      if (els.optProg.checked && measures > 1){
        var every = Math.max(1, Number(els.progEvery.value) || 8);
        if ((measures - 1) % every === 0){
          var nv = Math.min(280, bpm + (Number(els.progStep.value) || 4));
          if (nv !== bpm){
            var t = beatToTime(b);
            bpm = nv; els.bpm.value = nv; els.bpmOut.textContent = nv;
            anchorBeat = b; anchorTime = t; spb = secPerBeat(nv);
          }
        }
      }
    }
    if (els.optMet.checked){
      var pos = ((b % sig.beats) + sig.beats) % sig.beats;
      click(beatToTime(b), pos < 1e-4);
    }
    nextClickBeat = b + sig.click;
  }
  while (beatToTime(nextNoteBeat) < horizon){
    var n = pattern.notes[nextNoteIdx], nt = beatToTime(nextNoteBeat);
    if (els.optRud.checked){
      var other = n.s === 'R' ? 'L' : 'R';
      if (n.g === 1) hit(nt - Math.min(.045, spb*.12), false, true, other);
      if (n.g === 2){ hit(nt - Math.min(.09, spb*.22), false, true, other); hit(nt - Math.min(.045, spb*.11), false, true, other); }
      hit(nt, n.a, false, n.s);
    }
    visual.push({ t:nt, a:n.a });
    nextNoteIdx++;
    if (nextNoteIdx >= pattern.notes.length){ nextNoteIdx = 0; cycles++; }
    nextNoteBeat = cycles * pattern.len + pattern.notes[nextNoteIdx].at;
  }
}

var cv = els.score, cx = cv.getContext('2d'), W = 0, H = 190, MID = 104, GAP = 9;
var C = {};
function readTheme(){
  var s = getComputedStyle(document.documentElement);
  C.ink = s.getPropertyValue('--strip-ink').trim();
  C.soft = s.getPropertyValue('--strip-soft').trim();
  C.line = s.getPropertyValue('--strip-line').trim();
  C.paper = s.getPropertyValue('--strip').trim();
  C.red = s.getPropertyValue('--red').trim();
}
function resize(){
  var dpr = window.devicePixelRatio || 1;
  W = cv.clientWidth; H = cv.clientHeight; MID = Math.round(H * .55);
  cv.width = Math.round(W*dpr); cv.height = Math.round(H*dpr);
  cx.setTransform(dpr,0,0,dpr,0,0);
}
window.addEventListener('resize', function(){ resize(); if (!playing) paint(0); });

function head(x, y, small){
  cx.save(); cx.translate(x,y); cx.rotate(-.32); cx.beginPath();
  cx.ellipse(0,0, small?4:6.2, small?3:4.6, 0, 0, Math.PI*2);
  cx.fillStyle = C.ink; cx.fill(); cx.restore();
}
function drawNote(n, x, showStick){
  var top = MID - 40;
  if (n.g === 1){
    head(x-15, MID, true); cx.fillStyle = C.ink; cx.fillRect(x-11.5, MID-26, 1.2, 26);
    cx.strokeStyle = C.ink; cx.lineWidth = 1.4; cx.beginPath();
    cx.moveTo(x-17, MID-14); cx.lineTo(x-6, MID-22); cx.stroke();
  } else if (n.g === 2){
    head(x-22, MID, true); head(x-13, MID, true);
    cx.fillStyle = C.ink; cx.fillRect(x-18.5, MID-26, 1.2, 26); cx.fillRect(x-9.5, MID-26, 1.2, 26);
    cx.fillRect(x-20, MID-26, 12, 2.4); cx.fillRect(x-20, MID-21, 12, 2.4);
  }
  head(x, MID);
  cx.fillStyle = C.ink; cx.fillRect(x+5.2, top, 1.6, MID-top);
  if (n.a){
    cx.strokeStyle = C.ink; cx.lineWidth = 1.7; cx.beginPath();
    cx.moveTo(x-5, MID-44); cx.lineTo(x+5, MID-40); cx.lineTo(x-5, MID-36); cx.stroke();
  }
  if (showStick){
    cx.fillStyle = C.soft; cx.font = '600 13px "IBM Plex Mono", monospace'; cx.textAlign = 'center';
    cx.fillText(letter(n.s), x, MID+36);
  }
}
function paint(beat){
  if (!W) resize();
  cx.fillStyle = C.paper; cx.fillRect(0,0,W,H);
  var px = Math.max(W < 430 ? 74 : 92, Math.min(210, 215*spb)), playX = W*.3;
  cx.strokeStyle = C.line; cx.lineWidth = 1;
  for (var i=-2;i<=2;i++){ var y = MID + i*GAP + .5; cx.beginPath(); cx.moveTo(0,y); cx.lineTo(W,y); cx.stroke(); }
  var lb = beat - playX/px, rb = beat + (W-playX)/px;
  for (var m = Math.floor(lb/sig.beats)-1; m <= Math.ceil(rb/sig.beats)+1; m++){
    var mx = playX + (m*sig.beats - beat)*px;
    if (mx < -40 || mx > W+40) continue;
    cx.fillStyle = C.ink; cx.globalAlpha = .5; cx.fillRect(mx, MID-2*GAP, 1.5, 4*GAP); cx.globalAlpha = 1;
    if (m >= 0){
      cx.fillStyle = C.soft; cx.font = '400 11px "IBM Plex Mono", monospace'; cx.textAlign = 'left';
      cx.fillText(String(m+1), mx+5, MID-2*GAP-9);
    }
  }
  if (playing && lead > 0){
    for (var cb = -lead; cb < 0; cb++){
      var cxp = playX + (cb - beat)*px;
      if (cxp < -40 || cxp > W+40) continue;
      var now = Math.floor(beat) === cb;
      cx.fillStyle = now ? C.red : C.soft; cx.globalAlpha = now ? 1 : .55;
      cx.font = '700 ' + (now ? 34 : 26) + 'px "Big Shoulders Display", Impact, sans-serif'; cx.textAlign = 'center';
      cx.fillText(String(cb + lead + 1), cxp, MID + 10);
      cx.globalAlpha = 1;
    }
  }
  var showStick = els.optStick.checked;
  for (var k = Math.max(0, Math.floor(lb/pattern.len)-1); k <= Math.ceil(rb/pattern.len)+1; k++){
    var base = k*pattern.len;
    if (base+pattern.len < lb-1 || base > rb+1) continue;
    for (var gi=0; gi<pattern.groups.length; gi++){
      var g = pattern.groups[gi];
      var x1 = playX + (base+pattern.notes[g.from].at - beat)*px + 6;
      var x2 = playX + (base+pattern.notes[g.to].at - beat)*px + 6;
      if (x2 < -60 || x1 > W+60) continue;
      var top = MID-40;
      if (g.from === g.to) x2 = x1 + 9;
      for (var bi=0; bi<g.b; bi++){ cx.fillStyle = C.ink; cx.fillRect(x1, top+bi*6.5, x2-x1, 3.6); }
      if (g.t){
        cx.fillStyle = C.soft; cx.font = '400 11px "IBM Plex Mono", monospace'; cx.textAlign = 'center';
        cx.fillText(String(g.t), (x1+x2)/2, top - (pattern.notes[g.from].a ? 16 : 7));
      }
    }
    for (var ni=0; ni<pattern.notes.length; ni++){
      var n = pattern.notes[ni], x = playX + (base+n.at - beat)*px;
      if (x < -60 || x > W+60) continue;
      drawNote(n, x, showStick);
    }
  }
  cx.fillStyle = C.red; cx.fillRect(playX-1, MID-3.4*GAP, 2, 6.8*GAP);
  cx.beginPath(); cx.moveTo(playX-5.5, MID-3.4*GAP); cx.lineTo(playX+5.5, MID-3.4*GAP);
  cx.lineTo(playX, MID-3.4*GAP+8); cx.closePath(); cx.fill();
}

var lugs = [];
function buildLugs(){
  lugs.forEach(function(l){ l.remove(); }); lugs = [];
  var n = Math.round(sig.beats/sig.click), r = 75;
  for (var i=0;i<n;i++){
    var a = (-90 + i*360/n) * Math.PI/180;
    var d = document.createElement('span');
    d.className = 'lug' + (i === 0 ? ' first' : '');
    d.style.setProperty('--tx', (Math.cos(a)*r).toFixed(1) + 'px');
    d.style.setProperty('--ty', (Math.sin(a)*r).toFixed(1) + 'px');
    els.pad.appendChild(d); lugs.push(d);
  }
}
function frame(){
  requestAnimationFrame(frame);
  var beat = playing ? nowBeat() : 0;
  paint(beat);
  if (playing){
    var t = actx.currentTime, flash = null;
    while (visual.length && visual[0].t < t - .12) visual.shift();
    for (var i=0;i<visual.length;i++){
      if (visual[i].t <= t && visual[i].t > t - .09){ flash = visual[i]; break; }
      if (visual[i].t > t) break;
    }
    els.lamp.className = 'lamp' + (flash ? (flash.a ? ' on acc' : ' on') : '');
    var pos = ((beat % sig.beats) + sig.beats) % sig.beats, active = Math.floor(pos/sig.click);
    for (var d=0; d<lugs.length; d++) lugs[d].className = 'lug' + (d===0?' first':'') + (d===active?' on':'');
    els.counter.textContent = beat < 0 ? D.countIn : D.bar + ' ' + (Math.floor(beat/sig.beats)+1);
    els.hint.textContent = beat < 0 ? D.ready : '';
  } else {
    els.lamp.className = 'lamp';
    for (var q=0; q<lugs.length; q++) lugs[q].className = 'lug' + (q===0?' first':'');
    els.counter.textContent = '—';
    els.hint.textContent = D.start;
  }
}

function selectRud(i){
  idx = (i + RUDIMENTS.length) % RUDIMENTS.length;
  current = RUDIMENTS[idx]; pattern = compile(current);
  describe(); markList(); restart();
  if (history.replaceState) history.replaceState(null, '', '#' + current.id);
}
function buildList(q){
  q = (q || '').trim().toLowerCase();
  els.rudList.innerHTML = '';
  var found = 0;
  ['roll','para','flam','drag'].forEach(function(c){
    var items = RUDIMENTS.filter(function(r){
      if (r.cat !== c) return false;
      if (!q) return true;
      return (D.names[r.id] + ' ' + window.RUDI_I18N.en.names[r.id]).toLowerCase().indexOf(q) >= 0;
    });
    if (!items.length) return;
    var h = document.createElement('div'); h.className = 'grouphead'; h.textContent = D.cats[c];
    els.rudList.appendChild(h);
    items.forEach(function(r){
      found++;
      var p = compile(r);
      var b = document.createElement('button');
      b.className = 'item'; b.dataset.id = r.id;
      b.innerHTML = '<span class="txt"><span class="iname"></span><span class="isub"></span></span>';
      b.querySelector('.iname').textContent = D.names[r.id];
      b.querySelector('.isub').textContent = p.notes.map(function(n){ return letter(n.s); }).join(' ');
      b.addEventListener('click', function(){ selectRud(RUDIMENTS.indexOf(r)); closePicker(); });
      els.rudList.appendChild(b);
    });
  });
  if (!found){ var e = document.createElement('div'); e.className = 'empty'; e.textContent = D.empty; els.rudList.appendChild(e); }
  markList();
}
function markList(){
  Array.prototype.forEach.call(els.rudList.querySelectorAll('.item'), function(b){
    b.setAttribute('aria-current', String(b.dataset.id === current.id));
  });
}
function openPicker(){
  els.overlay.classList.add('open'); els.search.value = ''; buildList('');
  var sel = els.rudList.querySelector('[aria-current="true"]');
  if (sel) sel.scrollIntoView({ block:'center' });
}
function closePicker(){ els.overlay.classList.remove('open'); }

SIGS.forEach(function(s, i){
  var b = document.createElement('button');
  b.textContent = s.id; b.setAttribute('aria-pressed', i === 0 ? 'true' : 'false');
  b.addEventListener('click', function(){
    sig = s; buildLugs(); spb = secPerBeat(bpm); describe();
    Array.prototype.forEach.call(els.segSig.children, function(c){ c.setAttribute('aria-pressed', String(c === b)); });
    restart();
  });
  els.segSig.appendChild(b);
});
Array.prototype.forEach.call(els.segHand.children, function(b){
  b.addEventListener('click', function(){
    hand = b.dataset.v;
    Array.prototype.forEach.call(els.segHand.children, function(c){ c.setAttribute('aria-pressed', String(c === b)); });
    describe(); buildList(els.search.value);
  });
});

els.play.addEventListener('click', function(){ playing ? stop() : start(); });
els.prev.addEventListener('click', function(){ selectRud(idx - 1); });
els.next.addEventListener('click', function(){ selectRud(idx + 1); });
els.openPicker.addEventListener('click', openPicker);
els.overlay.addEventListener('click', function(e){ if (e.target === els.overlay) closePicker(); });
els.search.addEventListener('input', function(){ buildList(els.search.value); });
els.bpm.addEventListener('input', function(){ setBpm(Number(els.bpm.value), true); });

els.langBtn.addEventListener('click', function(e){ e.stopPropagation(); els.langMenu.classList.toggle('open'); });
document.addEventListener('click', function(){ els.langMenu.classList.remove('open'); });

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

els.theme.addEventListener('click', function(){
  var next = document.documentElement.dataset.theme === 'night' ? 'paper' : 'night';
  document.documentElement.dataset.theme = next;
  var meta = document.querySelector('meta[name=theme-color]');
  if (meta) meta.content = next === 'night' ? '#121110' : '#E7DFCC';
  try{ localStorage.setItem('rudi-theme', next); }catch(e){}
  readTheme();
});
document.addEventListener('keydown', function(e){
  if (e.code === 'Escape'){ closePicker(); return; }
  var tag = e.target.tagName;
  if (tag === 'INPUT' || tag === 'SELECT' || tag === 'TEXTAREA') return;
  if (e.code === 'Space'){ e.preventDefault(); playing ? stop() : start(); }
  if (e.code === 'ArrowUp'){ e.preventDefault(); nudge(e.shiftKey ? 5 : 1); }
  if (e.code === 'ArrowDown'){ e.preventDefault(); nudge(e.shiftKey ? -5 : -1); }
});
document.addEventListener('visibilitychange', function(){ if (!document.hidden && playing) lock(true); });

var hash = (location.hash || '').replace('#','');
for (var h=0; h<RUDIMENTS.length; h++) if (RUDIMENTS[h].id === hash) idx = h;
current = RUDIMENTS[idx]; pattern = compile(current);

els.play.setAttribute('aria-label', D.play);
els.theme.setAttribute('aria-label', D.theme);
readTheme(); buildLugs(); resize(); setBpm(100, false); describe(); buildList(''); frame();
})();
