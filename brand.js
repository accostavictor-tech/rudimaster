/* Versao com marca parceira: poe o link para o site da marca no rodape.
   A marca em si e aplicada no <head> (HEAD_SCRIPT no build.py), que deixa
   os dados dela em window.RUDI_BRAND. Sem ?brand= na URL, nada acontece. */
(function(){
  var b = window.RUDI_BRAND, foot = document.querySelector('.sitefoot');
  if(!b || !foot) return;
  var lang = document.documentElement.dataset.lang;
  var label = {pt:'Conheça as baterias %s', es:'Conoce las baterías %s'}[lang] || 'Explore %s drums';
  var a = document.createElement('a');
  a.className = 'brandlink'; a.href = b.url; a.target = '_blank'; a.rel = 'noopener';
  a.textContent = label.replace('%s', b.name) + ' →';
  var s = document.createElement('span');
  s.appendChild(a);
  foot.insertBefore(s, foot.firstChild);
})();
