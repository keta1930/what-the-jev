// Strategy shapes are independent of player colors and never encode an action.
const StrategyUI=(()=>{
 const shapes={jev:'M12 2 15 9 22 12 15 15 12 22 9 15 2 12 9 9Z',cooperate:'M12 3V21M3 12H21',defect:'M12 2 21 8V17L12 22 3 17V8ZM12 7V14M12 17V18',random:'M4 3H20V21H4ZM8 7H8.1M16 7H16.1M12 12H12.1M8 17H8.1M16 17H16.1',cycle:'M19 8A8 8 0 1 0 20 15M19 3V9H13',tit_for_tat:'M3 7H21L17 3M21 17H3L7 21',generous:'M12 21C-3 11 3-2 12 7C21-2 27 11 12 21Z',win_stay_lose_shift:'M3 5H8L16 19H21M3 19H8L16 5H21M18 2 21 5 18 8M18 16 21 19 18 22'};
 const short={jev:'Jev',cooperate:'始终合作',defect:'始终强硬',random:'随机',cycle:'循环',tit_for_tat:'针锋相对',generous:'宽容互惠',win_stay_lose_shift:'赢留输换'};
 function icon(key){const ns='http://www.w3.org/2000/svg',s=document.createElementNS(ns,'svg'),p=document.createElementNS(ns,'path');s.setAttribute('viewBox','0 0 24 24');s.setAttribute('class','strategy-icon');s.setAttribute('aria-hidden','true');p.setAttribute('d',shapes[key]);p.setAttribute('fill',key==='jev'?'currentColor':'none');p.setAttribute('stroke','currentColor');p.setAttribute('stroke-width','1.8');p.setAttribute('stroke-linecap','round');p.setAttribute('stroke-linejoin','round');s.append(p);return s}
 function badge(key,player){const b=document.createElement('span');b.className='strategy-badge strategy-'+key;b.setAttribute('title',DATA.names[key]+(key==='jev'?' · 真实模型':' · 规则策略'));b.append(icon(key));const t=document.createElement('span');t.textContent=(player===undefined?'':'P'+(player+1)+' · ')+short[key];b.append(t);return b}
 return {shapes,short,icon,badge};
})();
