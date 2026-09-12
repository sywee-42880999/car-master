const $=id=>document.getElementById(id);
const KNOWN_KEY='carModelKnown';
const BRAND_KEY='carModelBrand';
const views=['learnViewModel','testViewModel','modelResultView'];
let allModels=[],filtered=[],index=0,currentBrand=localStorage.getItem(BRAND_KEY)||'all';
let known=new Set(JSON.parse(localStorage.getItem(KNOWN_KEY)||'[]'));
let showingRear=false,touchStart=null,testQuestions=[],testIndex=0,testResults=[];

function save(){localStorage.setItem(KNOWN_KEY,JSON.stringify([...known]));localStorage.setItem(BRAND_KEY,currentBrand)}
function showView(id){views.forEach(v=>$(v).classList.toggle('hidden',v!==id))}
function shuffle(src){const a=[...src];for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function toast(s){$('modelToast').textContent=s;$('modelToast').classList.add('show');clearTimeout(toast.t);toast.t=setTimeout(()=>$('modelToast').classList.remove('show'),1700)}
function imagePath(brand,id,side='front'){return `./images/vehicles/${brand}/${id.toLowerCase()}_${side}.webp`}
function normalizedName(id,name){if(id==='K030')return 'EV4 Fastback';return name}
function answerAliases(name){return name.split('/').map(x=>x.trim()).filter(Boolean)}
function norm(s){return String(s||'').toLocaleUpperCase('en-US').replace(/\bTHE\b/g,'').replace(/[^A-Z0-9]/g,'')}
function isCorrect(input,name){const n=norm(input);return answerAliases(name).some(x=>norm(x)===n)}
function bodyLabel(v){return ({passenger:'PASSENGER',suv:'SUV',mpv:'MPV',pickup:'PICK-UP',commercial:'COMMERCIAL',bus:'BUS'}[v]||String(v||'').toUpperCase())}
function updateLearned(){const visibleKnown=allModels.filter(x=>known.has(x.id)).length;$('learnedCount').textContent=`${visibleKnown} / ${allModels.length}`}
function currentList(){return filtered.length?filtered:allModels}

function applyFilter(brand){currentBrand=brand;save();document.querySelectorAll('[data-brand]').forEach(b=>b.classList.toggle('active',b.dataset.brand===brand));filtered=brand==='all'?[...allModels]:allModels.filter(x=>x.brand===brand);index=0;showingRear=false;renderCard()}
function renderCard(){
  showView('learnViewModel');
  const list=currentList();
  if(!list.length)return toast('표시할 차종이 없습니다.');
  index=(index+list.length)%list.length;const m=list[index];
  $('modelPosition').textContent=`${index+1} / ${list.length}`;
  $('modelId').textContent=m.id;
  $('modelBrand').textContent=m.brand.toUpperCase();
  $('modelName').textContent=m.name;
  $('modelMeta').textContent=`${bodyLabel(m.type)} · ${m.id} · ${m.rear?'FRONT + REAR':'FRONT'}`;
  $('toggleRear').classList.toggle('hidden',!m.rear);
  if(!m.rear)showingRear=false;
  const side=showingRear?'rear':'front';
  $('angleTag').textContent=side.toUpperCase();
  $('modelImage').src=m[side];
  $('modelImage').alt=`${m.brand} ${m.name} ${side} view`;
  $('modelImage').onerror=()=>{showingRear=false;if(side==='rear'){toast('후면 이미지는 보류합니다.');renderCard()}else toast(`${m.id} 이미지 확인 필요`)};
  updateLearned();
}
function move(n){const list=currentList();if(!list.length)return;index=(index+n+list.length)%list.length;showingRear=false;renderCard()}
function markKnown(){const m=currentList()[index];known.add(m.id);save();updateLearned();move(1)}
function restore(){known.clear();save();updateLearned();toast('숨긴 차종을 모두 복원했습니다.')}
function toggleRear(){const m=currentList()[index];if(!m.rear)return;showingRear=!showingRear;renderCard()}
function randomize(){filtered=shuffle(currentList());index=0;showingRear=false;renderCard();toast('차종 순서를 섞었습니다.')}

function startTest(){
  const source=currentList();if(source.length<2)return;
  testQuestions=shuffle(source).slice(0,Math.min(20,source.length)).map((m,i)=>{
    const useRear=!!m.rear&&Math.random()<.25;
    const detail=Math.random()<.55;
    const crop=['left','center','right'][Math.floor(Math.random()*3)];
    return {m,side:useRear?'rear':'front',detail,crop};
  });
  testIndex=0;testResults=[];showView('testViewModel');renderQuestion();
}
function renderQuestion(){
  const q=testQuestions[testIndex];
  $('modelTestCount').textContent=`TEST ${String(testIndex+1).padStart(2,'0')} / ${testQuestions.length}`;
  $('cropModeLabel').textContent=q.detail?'DETAIL CROP':q.side==='rear'?'REAR VIEW':'FULL VEHICLE';
  const box=$('modelTestVisual');box.className='model-test-image';if(q.detail)box.classList.add('detail',`detail-${q.crop}`);
  $('modelTestImage').src=q.m[q.side];$('modelTestImage').alt='차종 맞히기 문제 이미지';
  $('modelAnswer').value='';$('modelAnswer').focus();
}
function submitAnswer(e){
  e.preventDefault();const q=testQuestions[testIndex],answer=$('modelAnswer').value.trim();const correct=isCorrect(answer,q.m.name);
  testResults.push({q,answer,correct});testIndex++;
  if(testIndex<testQuestions.length)renderQuestion();else finishTest();
}
function finishTest(){
  const score=testResults.filter(x=>x.correct).length,total=testResults.length,wrong=testResults.filter(x=>!x.correct);
  showView('modelResultView');
  $('modelResultBody').innerHTML=`<div class="result-score"><span>MODEL TEST RESULT</span><strong>${score} / ${total}</strong><h2>${score===total?'PASS':'다시 확인'}</h2><p>${wrong.length} Incorrect · 틀린 차종을 확인하고 다시 도전하세요.</p></div><div class="model-wrong-list">${wrong.map(x=>`<div class="model-wrong"><img src="${x.q.m.front}" alt=""><div><strong>${x.q.m.name}</strong><span>입력: ${x.answer||'—'}</span><em>${x.q.m.brand.toUpperCase()} · ${bodyLabel(x.q.m.type)}</em></div></div>`).join('')}</div><div class="model-result-actions"><button id="retryModelTest" class="primary" type="button">다시 시험보기</button><button id="backModelLearn" class="secondary" type="button">학습으로 돌아가기</button></div>`;
  $('retryModelTest').onclick=startTest;$('backModelLearn').onclick=renderCard;
}

$('prevModel').onclick=()=>move(-1);$('nextModel').onclick=()=>move(1);$('knowModel').onclick=markKnown;$('restoreModels').onclick=restore;$('toggleRear').onclick=toggleRear;$('shuffleModels').onclick=randomize;$('startTestTop').onclick=startTest;$('exitTest').onclick=renderCard;$('modelAnswerForm').onsubmit=submitAnswer;
document.querySelectorAll('[data-brand]').forEach(b=>b.onclick=()=>applyFilter(b.dataset.brand));
document.addEventListener('keydown',e=>{if(!$('learnViewModel').classList.contains('hidden')){if(e.key==='ArrowLeft')move(-1);if(e.key==='ArrowRight')move(1)}});
$('modelCard').addEventListener('touchstart',e=>{const t=e.changedTouches[0];touchStart={x:t.clientX,y:t.clientY}},{passive:true});
$('modelCard').addEventListener('touchend',e=>{if(!touchStart)return;const t=e.changedTouches[0],dx=t.clientX-touchStart.x,dy=t.clientY-touchStart.y;touchStart=null;if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy)*1.2)move(dx<0?1:-1)},{passive:true});

Promise.all([
  fetch('./data/models-latest.json?v=20260912').then(r=>r.json()),
  fetch('./data/model-image-qc.json?v=20260912').then(r=>r.json())
]).then(([registry,qc])=>{
  allModels=registry.m.filter(r=>r[1]==='hyundai'||r[1]==='kia').map(r=>{
    const [id,brand,name,type]=r,rec=qc.models?.[id]||{};
    const front=rec.front||imagePath(brand,id,'front');
    const rear=id==='H057'?null:(rec.rear_status&&rec.rear_status!=='MISS'&&rec.rear?rec.rear:null);
    return {id,brand,name:normalizedName(id,name),type,front:'./'+front.replace(/^\.\//,''),rear:rear?'./'+rear.replace(/^\.\//,''):null};
  });
  applyFilter(['all','hyundai','kia'].includes(currentBrand)?currentBrand:'all');updateLearned();
}).catch(err=>{console.error(err);toast('차종 데이터를 불러오지 못했습니다.')});

if('serviceWorker'in navigator)window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js',{scope:'./'}).catch(()=>{}));
