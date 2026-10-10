// Execute the actual classic script in an isolated in-memory DOM. No browser,
// network or model is used. This specifically tests immediate reduced-motion
// rendering and cancellation when the user changes rounds rapidly.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

function run(reduced) {
  let cancelled = 0;
  let document;
  class Element {
    constructor(tag) {
      this.tagName = tag; this.children = []; this.attributes = {}; this.events = {};
      this.textContent = ''; this.open = false; this.disabled = false; this.parentElement = null;
      this.style = {setProperty() {}};
      const classes = new Set();
      this.classList = {add: x => classes.add(x), remove: x => classes.delete(x), contains: x => classes.has(x)};
    }
    append(...nodes) {for (const node of nodes) {node.parentElement = this; this.children.push(node);}}
    replaceChildren(...nodes) {this.children = []; this.append(...nodes);}
    setAttribute(key,value) {this.attributes[key] = value;}
    getAttribute(key) {return this.attributes[key];}
    addEventListener(name,callback) {this.events[name] = callback;}
    getAnimations() {return [{cancel() {cancelled++;}}];}
    focus() {document.activeElement = this;}
    closest(selector) {return selector === '#round-grid' && this.parentElement?.id === 'round-grid' ? this.parentElement : null;}
    get firstChild() {return this.children[0];}
    get offsetWidth() {return 400;}
  }
  const ids = ['scene','round-title','round-context','position','previous','next','previous-group','next-group','round-grid','trend','choices','trend-stage','roster','play','speed','scrub','raw-link','final-summary','batch-details'];
  const elements = Object.fromEntries(ids.map(id => {const e=new Element('div');e.id=id;return [id,e];}));
  document = {getElementById:id=>elements[id],createElement:tag=>new Element(tag),createElementNS:(_,tag)=>new Element(tag),activeElement:null,addEventListener(){}};
  const records = Array.from({length:25},(_,i)=>({round:i+1,original:['cooperate','defect'],actions:['cooperate','defect'],payoffs:[0,5],cumulative:[0,(i+1)*5],proposer:null}));
  const data = {config:{scenario:'prisoner-dilemma',players:['cooperate','defect'],id:'unit'},records,
    match:{status:'complete',cumulative:[0,125],cost_usd_returned:0,cost_missing_attempts:0,reason:null,number:1,seed:'18446744073709551615',returned_snapshots:[]},
    raw_segments:[{start:1,end:20,path:'unit-m001-s1.html'},{start:21,end:25,path:'unit-m001-s2.html'}],slug:'unit-m001',batch_id:'unit-only',model:'test-double',generated:'unit-only',names:{cooperate:'rule cooperator',defect:'rule defector'},actions:{cooperate:'cooperate',defect:'defect'}};
  let clock=0,sequence=0;const timers=new Map();elements.speed.value='1800';
  function tick(ms){const until=clock+ms;while(true){const due=[...timers].filter(([,t])=>t.at<=until).sort((a,b)=>a[1].at-b[1].at)[0];if(!due)break;clock=due[1].at;timers.delete(due[0]);due[1].fn()}clock=until}
  const context = {DATA:data,document,location:{hash:''},history:{replaceState(){}},window:{addEventListener(){}},matchMedia:()=>({matches:reduced}),setTimeout(fn,ms){timers.set(++sequence,{fn,at:clock+ms});return sequence},clearTimeout(id){timers.delete(id)}};
  const asset=path.join(__dirname,'../src/game_theory/assets');
  vm.runInNewContext(fs.readFileSync(path.join(asset,'identity.js'),'utf8')+fs.readFileSync(path.join(asset,'match.js'),'utf8'),context);
  assert.equal(elements['round-title'].textContent,'第 1 轮');
  elements.next.onclick(); elements.next.onclick(); elements.next.onclick(); elements.previous.onclick();
  assert.equal(elements['round-title'].textContent,'第 3 轮');
  assert.equal(elements.scene.classList.contains('reveal'),!reduced);
  // The actual values are already in the DOM; CSS must not delay them in the
  // reduced-motion branch. An old reveal is cancelled on every selection.
  const players = elements.scene.children[1];
  assert.equal(players.children[1].children[2].textContent,'defect');
  assert.equal(players.children[1].children[4].children[1].children[1].textContent,'15');
  assert.equal(cancelled,5);
  assert.equal(elements['round-grid'].children.length,20);
  elements['next-group'].onclick();
  assert.equal(elements['round-grid'].children.length,5);
  elements['round-grid'].children[0].onclick();
  assert.equal(elements['round-title'].textContent,'第 21 轮');
  assert.equal(elements['raw-link'].href,'../raw/unit-m001-s2.html#r21');
  tick(800);assert.equal(elements['trend-stage'].textContent,'截至第 21 轮');
  const result={reduced,round:elements['round-title'].textContent,cancelled};
  elements.play.onclick();tick(1800);assert.equal(elements['round-title'].textContent,'第 22 轮');
  if(!reduced)assert.equal(elements['trend-stage'].textContent,'截至第 21 轮');
  tick(800);assert.equal(elements['trend-stage'].textContent,'截至第 22 轮');
  elements.play.onclick();tick(5000);assert.equal(elements['round-title'].textContent,'第 22 轮');
  elements.scrub.value='24';elements.scrub.events.input();elements.play.onclick();tick(2600);
  assert.equal(elements['round-title'].textContent,'第 25 轮');assert.equal(elements.play.attributes['aria-pressed'],'false');assert.equal(timers.size,0);
  elements.play.onclick();assert.equal(elements['round-title'].textContent,'第 1 轮');
  // Replaying the already revealed first round must keep the trend mounted;
  // clearing it used to collapse the right panel before the settle timer.
  assert.equal(elements['trend-stage'].textContent,'截至第 1 轮');
  assert.ok(elements.trend.children.length>0 && elements.choices.children.length>0);
  elements.next.onclick();tick(5000);assert.equal(elements['round-title'].textContent,'第 2 轮');assert.equal(timers.size,0);
  assert.equal(elements.roster.children.length,2);return result;
}

console.log(JSON.stringify([run(false),run(true)]));
