// ===== TOUCH CONTROLS // uniwersalna nakładka dotykowa =====
// Wstrzykuje pływające przyciski dotykowe i symuluje klawisze,
// dzięki czemu gry klawiszowe działają na telefonach/tabletach.
// Konfiguracja per gra: window.TOUCH_CONFIG = { keys: [...], touchMove: true }
(function(){
  'use strict';
  var cfg = window.TOUCH_CONFIG || { keys: ['ArrowLeft','ArrowRight','ArrowUp','ArrowDown',' ','w','a','s','d'] };
  var IS_TOUCH = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);
  if (!IS_TOUCH || window.__touchControlsLoaded) return;
  window.__touchControlsLoaded = true;

  function fire(type, key){
    try {
      var ev = new KeyboardEvent(type, { key: key, bubbles: true, cancelable: true });
      document.dispatchEvent(ev);
    } catch(e){}
  }
  function press(k){ fire('keydown', k); }
  function release(k){ fire('keyup', k); }

  // nakładka
  var pad = document.createElement('div');
  pad.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:99999;'+
    'display:flex;justify-content:space-between;padding:8px 12px calc(12px + env(safe-area-inset-bottom));'+
    'pointer-events:none;gap:10px;flex-wrap:wrap;';
  pad.id = 'touch-pad';

  var LABELS = {
    'ArrowLeft':'◀','ArrowRight':'▶','ArrowUp':'▲','ArrowDown':'▼',
    ' ':'⬤','Space':'⬤','w':'W','a':'A','s':'S','d':'D'
  };

  function mkBtn(key){
    var b = document.createElement('button');
    b.innerHTML = LABELS[key] || key;
    b.style.cssText = 'pointer-events:auto;width:64px;height:64px;border-radius:50%;'+
      'border:none;background:rgba(60,120,255,0.45);color:#fff;font-size:24px;font-weight:bold;'+
      'backdrop-filter:blur(2px);-webkit-backdrop-filter:blur(2px);box-shadow:0 2px 8px rgba(0,0,0,0.3);'+
      'user-select:none;-webkit-user-select:none;touch-action:none;';
    b.addEventListener('touchstart', function(e){ e.preventDefault(); press(key); }, {passive:false});
    b.addEventListener('touchend',   function(e){ e.preventDefault(); release(key); }, {passive:false});
    b.addEventListener('touchcancel',function(e){ e.preventDefault(); release(key); }, {passive:false});
    b.addEventListener('mousedown',  function(){ press(key); });
    b.addEventListener('mouseup',    function(){ release(key); });
    b.addEventListener('mouseleave', function(){ release(key); });
    b.style.pointerEvents = 'auto';
    return b;
  }

  // lewa i prawa grupa
  var left = document.createElement('div');
  left.style.cssText = 'display:flex;gap:8px;pointer-events:none;';
  var right = document.createElement('div');
  right.style.cssText = 'display:flex;gap:8px;pointer-events:none;';

  // rozdziel klawisze: lewo = W/A/S/D + przestrzen; prawo = strzalki
  var leftKeys = ['w','a','s','d',' '];
  var rightKeys = ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space'];
  leftKeys.forEach(function(k){ if(cfg.keys.indexOf(k)>=0) left.appendChild(mkBtn(k)); });
  rightKeys.forEach(function(k){ if(cfg.keys.indexOf(k)>=0) right.appendChild(mkBtn(k)); });

  pad.appendChild(left);
  pad.appendChild(right);
  document.body.appendChild(pad);

  // dla gier z mousemove (breakout) - symuluj ruch palcem
  if (cfg.touchMove) {
    document.addEventListener('touchmove', function(e){
      var t = e.touches[0];
      var me = new MouseEvent('mousemove', { clientX: t.clientX, clientY: t.clientY, bubbles: true });
      e.target.dispatchEvent(me);
      if (cfg.moveTarget) cfg.moveTarget();
    }, {passive:true});
  }

  // automatyczne przewijanie nie przeszkadza
  document.addEventListener('touchstart', function(e){
    if (e.target.closest && e.target.closest('#touch-pad')) e.preventDefault();
  }, {passive:false});
})();
