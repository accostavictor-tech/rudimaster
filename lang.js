(function(){
"use strict";
// Sugere a versao no idioma do navegador sem redirecionar.
// Redirecionamento automatico esconderia as outras versoes do Googlebot.

var LANGS = ['pt','en','es'];
var TXT = {
  pt: { msg:'Esta página também está disponível em português.', go:'Ver em português', close:'Fechar' },
  en: { msg:'This page is also available in English.',          go:'View in English',   close:'Close'  },
  es: { msg:'Esta página también está disponible en español.',  go:'Ver en español',    close:'Cerrar' }
};

function store(v){ try{ localStorage.setItem('rudi-lang', v); }catch(e){} }
function stored(){ try{ return localStorage.getItem('rudi-lang'); }catch(e){ return null; } }

var cur = document.documentElement.dataset.lang || 'pt';

// quem escolhe no menu define a preferencia e nao ve mais a faixa
Array.prototype.forEach.call(document.querySelectorAll('.langmenu a[hreflang]'), function(a){
  a.addEventListener('click', function(){ store(a.getAttribute('hreflang').slice(0,2)); });
});

if (stored()) return;

var prefs = navigator.languages || [navigator.language || 'pt'], best = null;
for (var i = 0; i < prefs.length && !best; i++){
  var code = String(prefs[i]).slice(0,2).toLowerCase();
  if (LANGS.indexOf(code) >= 0) best = code;
}
if (!best || best === cur) return;

// a URL equivalente ja esta declarada nos hreflang do head
var link = document.querySelector('link[rel="alternate"][hreflang="' + best + '"]');
if (!link) return;

var t = TXT[best];
var bar = document.createElement('div');
bar.className = 'langhint';
bar.setAttribute('lang', best);
bar.innerHTML = '<span></span><a class="lhgo"></a><button class="lhx" type="button"></button>';
bar.querySelector('span').textContent = t.msg;
var go = bar.querySelector('.lhgo');
go.textContent = t.go;
go.href = link.getAttribute('href');
go.addEventListener('click', function(){ store(best); });
var x = bar.querySelector('.lhx');
x.textContent = '\u00D7';
x.setAttribute('aria-label', t.close);
x.addEventListener('click', function(){ store(cur); bar.remove(); });

document.body.insertBefore(bar, document.body.firstChild);
})();
