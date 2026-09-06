
let parts=[], vehicles=[], idx=0;
let score=Number(localStorage.getItem('cm_score')||0);
let learned=JSON.parse(localStorage.getItem('cm_learned')||'[]');
const $=s=>document.querySelector(s);

async function load(){
  [parts,vehicles]=await Promise.all([
    fetch('./data/parts.json').then(r=>r.json()),
    fetch('./data/vehicles.json').then(r=>r.json())
  ]);
  idx=Math.min(Number(localStorage.getItem('cm_idx')||0), Math.max(parts.length-1,0));
  render();
}

function currentPart(){ return parts[idx]; }

function rememberProgress(){
  localStorage.setItem('cm_idx', idx);
  localStorage.setItem('cm_learned', JSON.stringify(learned));
  localStorage.setItem('cm_score', score);
}

function render(){
  const p=currentPart(), v=vehicles[0];
  $('#term').textContent=p.en.toUpperCase();
  $('#ko').textContent=p.ko;
  $('#where').textContent=p.where;
  $('#look').textContent=p.look;
  $('#sourceType').textContent=p.source_type==='HYUNDAI_OFFICIAL'?'HYUNDAI OFFICIAL':'INDUSTRY TERM';
  $('#count').textContent=`${idx+1} / ${parts.length}`;
  const pct=Math.round(((idx+1)/parts.length)*100);
  $('#bar').style.width=`${pct}%`;
  $('#mbar').style.width=`${pct}%`;
  $('#mcount').textContent=`${idx+1} / ${parts.length}`;
  $('#score').textContent=score;

  $('#partList').innerHTML=parts.map((x,i)=>(
    `<div class="item ${i===idx?'active':''}">${i+1}. ${x.ko} / ${x.en}${learned.includes(x.id)?' ✓':''}</div>`
  )).join('');

  const img=$('#hero');
  img.src=v.image;
  img.onerror=()=>{
    img.onerror=null;
    img.src=v.fallback;
    $('#imageNotice').style.display='block';
  };
  rememberProgress();
}

function goNext(){
  const p=currentPart();
  if(!learned.includes(p.id)) learned.push(p.id);
  idx=(idx+1)%parts.length;
  $('#quiz').style.display='none';
  render();
}

function goPrev(){
  idx=(idx-1+parts.length)%parts.length;
  $('#quiz').style.display='none';
  render();
}

$('#next').addEventListener('click',goNext);
$('#prev').addEventListener('click',goPrev);
$('#quizBtn').addEventListener('click',()=>{
  $('#quiz').style.display=$('#quiz').style.display==='block'?'none':'block';
  makeQuiz();
});

function makeQuiz(){
  const correct=currentPart();
  const distractors=parts.filter(x=>x.id!==correct.id).sort(()=>Math.random()-.5).slice(0,3);
  const pool=[correct,...distractors].sort(()=>Math.random()-.5);
  $('#q').textContent=`“${correct.ko}”의 영문 명칭은?`;
  $('#answers').innerHTML=pool.map(x=>`<button data-id="${x.id}">${x.en}</button>`).join('');
  $('#result').textContent='정답을 선택하세요.';
  [...$('#answers').children].forEach(b=>{
    b.addEventListener('click',()=>{
      if(b.dataset.id===correct.id){
        score+=100;
        $('#result').textContent='정답 +100';
      }else{
        $('#result').textContent=`다시 확인: ${correct.ko} = ${correct.en}`;
      }
      rememberProgress();
      render();
    });
  });
}

// Mobile swipe on the image stage
const stage=$('#stage');
let startX=0,startY=0,tracking=false;
stage.addEventListener('pointerdown',e=>{
  tracking=true; startX=e.clientX; startY=e.clientY;
});
stage.addEventListener('pointerup',e=>{
  if(!tracking) return;
  tracking=false;
  const dx=e.clientX-startX, dy=e.clientY-startY;
  if(Math.abs(dx)>55 && Math.abs(dx)>Math.abs(dy)*1.25){
    dx<0 ? goNext() : goPrev();
  }
});
stage.addEventListener('pointercancel',()=>tracking=false);

if('serviceWorker' in navigator){
  navigator.serviceWorker.register('./sw.js').catch(()=>{});
}
load();
