(function(){
"use strict";
var row = document.getElementById('share');
if (!row) return;

var canon = document.querySelector('link[rel="canonical"]');
function url(){ return (canon ? canon.getAttribute('href') : location.href.split('#')[0]) + (location.hash || ''); }
function text(){ return document.body.dataset.shareText || row.dataset.text || document.title; }

var links = {
  x:        function(){ return 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(text()) + '&url=' + encodeURIComponent(url()); },
  reddit:   function(){ return 'https://www.reddit.com/submit?url=' + encodeURIComponent(url()) + '&title=' + encodeURIComponent(text()); },
  whatsapp: function(){ return 'https://wa.me/?text=' + encodeURIComponent(text() + ' ' + url()); }
};
Array.prototype.forEach.call(row.querySelectorAll('a[data-net]'), function(a){
  a.addEventListener('click', function(){ a.href = links[a.dataset.net](); });
  a.href = links[a.dataset.net]();
});

var native = row.querySelector('[data-native]');
if (native){
  if (navigator.share){
    native.hidden = false;
    native.addEventListener('click', function(){
      navigator.share({ title: 'RudiMaster', text: text(), url: url() }).catch(function(){});
    });
  } else native.remove();
}
})();
