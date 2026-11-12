# patch160: a new sound system.
#  - Sounds in the world come from where they happen: each is placed around you in 3D (HRTF on a computer, simple
#    stereo on phones), following the camera as you turn.
#  - Distance: gunshots and explosions carry about 320 m (dull and soft far off, with an echo back off the hills);
#    other sounds about 110 m. A hill between you and a sound, or a wall (you inside a house and it outside, or the
#    other way round), muffles it.
#  - Rooms: inside a house the echo is short and boxy; outside it's the long outdoor one.
#  - Looping sounds placed in the world (used by the battle bus and the storm), and new sounds: the bus horn, jumping
#    out, the storm closing in (thunder).
rep("""let AC=null, noiseBuf=null, sfxGain=1, sfxLP=20000, sfxVerb=0, master=null, verb=null, cur=null;""",
"""let AC=null, noiseBuf=null, sfxGain=1, sfxLP=20000, sfxVerb=0, master=null, verb=null, cur=null, sfxPos=null, sfxEcho=0; const AUDIO={comp:null,inside:false,og:null,rg:null,echo:null};""")
rep("""function zsfx(k,pos){ const d=pos.distanceTo(P.pos); if(d>45) return; const f=1-d/45; sfxGain=0.5*f*f; sfxLP=Math.max(700,16000*f*f); sfx(k); sfxGain=1; sfxLP=20000; }
function sfxAt(k,pos){ const d=pos.distanceTo(P.pos); if(d>110) return; sfxGain=Math.max(0.1,1-d/110); sfxLP=Math.max(1200,20000*Math.pow(1-d/110,2.2)); sfx(k); sfxGain=1; sfxLP=20000; }""",
"""function zsfx(k,pos){ const d=pos.distanceTo(P.pos); if(d>45) return; const f=1-d/45; sfxGain=0.5*f*f; sfxLP=Math.max(700,16000*f*f); if(sfxOccluded(pos,d)){ sfxGain*=0.6; sfxLP=Math.min(sfxLP,1000); } sfxPos=pos; sfx(k); sfxPos=null; sfxGain=1; sfxLP=20000; }
const SFX_FAR=/^(shot|pump|boom|rocket|gl)/;
// a hill in the way, or a wall between inside a house and outside
function sfxOccluded(pos,d){ if(d<4||typeof camera==='undefined') return false; const L=camera.position;
  for(let i=1;i<8;i++){ const t=i/8, x=L.x+(pos.x-L.x)*t, z=L.z+(pos.z-L.z)*t, y=L.y+(pos.y+1-L.y)*t; if(terrainH(x,z)>y+0.3) return true; }
  return typeof brHouseAt==='function'&&AUDIO.inside!==!!brHouseAt(pos.x,pos.z); }
function sfxAt(k,pos){ const L=typeof camera!=='undefined'?camera.position:P.pos, d=pos.distanceTo(L), far=SFX_FAR.test(k), R=far?320:110; if(d>R) return;
  const f=1-d/R; sfxGain=Math.max(0.05,far?Math.pow(f,1.5):f); sfxLP=Math.max(800,20000*Math.pow(f,far?1.7:2.2));
  if(sfxOccluded(pos,d)){ sfxGain*=0.55; sfxLP=Math.min(sfxLP,1100); }
  sfxPos=pos; sfxEcho=far&&d>40?Math.min(0.55,0.15+d/550):0; if(sfxEcho&&AUDIO.echo) AUDIO.echo.delayTime.setTargetAtTime(Math.min(0.7,0.14+d/650),AC.currentTime,0.02);
  sfx(k); sfxPos=null; sfxEcho=0; sfxGain=1; sfxLP=20000; }
function panAt(p,pos){ if(p.positionX){ const t=AC.currentTime; p.positionX.setValueAtTime(pos.x,t); p.positionY.setValueAtTime(pos.y,t); p.positionZ.setValueAtTime(pos.z,t); } else p.setPosition(pos.x,pos.y,pos.z); }
function mkPanner(){ const p=AC.createPanner(); p.panningModel=isTouch?'equalpower':'HRTF'; p.distanceModel='linear'; p.refDistance=1; p.maxDistance=1e5; p.rolloffFactor=0; return p; } // direction only: the distance falloff is ours
// the listener: the camera, each frame; inside a house or not
function audioListen(){ if(!AC) return; const L=AC.listener, c=camera.position, t=AC.currentTime; camera.getWorldDirection(_alF);
  if(L.positionX){ L.positionX.setValueAtTime(c.x,t); L.positionY.setValueAtTime(c.y,t); L.positionZ.setValueAtTime(c.z,t); L.forwardX.setValueAtTime(_alF.x,t); L.forwardY.setValueAtTime(_alF.y,t); L.forwardZ.setValueAtTime(_alF.z,t); L.upX.setValueAtTime(0,t); L.upY.setValueAtTime(1,t); L.upZ.setValueAtTime(0,t); }
  else { L.setPosition(c.x,c.y,c.z); L.setOrientation(_alF.x,_alF.y,_alF.z,0,1,0); }
  const ins=typeof brHouseAt==='function'&&!!brHouseAt(c.x,c.z)&&c.y<terrainH(c.x,c.z)+12; if(ins!==AUDIO.inside&&AUDIO.og){ AUDIO.inside=ins; AUDIO.og.gain.setTargetAtTime(ins?0.25:1,t,0.3); AUDIO.rg.gain.setTargetAtTime(ins?1.2:0,t,0.3); } }
const _alF=new THREE.Vector3();
// a sound that keeps playing at a place: make(out) wires its sources into out; set(volume, position)
function loopSound(make){ if(!AC) return null; const g=AC.createGain(); g.gain.value=0; const p=mkPanner(); g.connect(p).connect(master); const stops=make(g)||[];
  return {g,p,set(v,pos){ g.gain.setTargetAtTime(v,AC.currentTime,0.15); if(pos) panAt(p,pos); },stop(){ try{ stops.forEach(s=>s.stop()); }catch(e){} g.disconnect(); }}; }
function audioUpgrade(comp){ AUDIO.comp=comp; const out=verb, len=Math.floor(AC.sampleRate*0.42), ir=AC.createBuffer(2,len,AC.sampleRate); // a room: dense early reflections, quick decay
  for(let c=0;c<2;c++){ const ch=ir.getChannelData(c); for(let i=0;i<len;i++) ch[i]=(Math.random()*2-1)*Math.pow(1-i/len,2.2)*(i<AC.sampleRate*0.004?0:1)*(1+0.8*Math.sin(i*0.004+c)); }
  const room=AC.createConvolver(); room.buffer=ir; const rg=AC.createGain(); rg.gain.value=0; room.connect(rg).connect(comp);
  const vin=AC.createGain(), og=AC.createGain(); vin.connect(og).connect(out); vin.connect(room); AUDIO.og=og; AUDIO.rg=rg; verb=vin;
  const e=AC.createDelay(1.0), fb=AC.createGain(), lp=AC.createBiquadFilter(), eg=AC.createGain(); e.delayTime.value=0.3; fb.gain.value=0.3; lp.type='lowpass'; lp.frequency.value=1500; eg.gain.value=0.55; // an echo off the hills, for far gunfire
  e.connect(lp).connect(fb).connect(e); lp.connect(eg).connect(comp); AUDIO.echo=e; }""")
rep("""verb.buffer=ir; const vg=AC.createGain(); vg.gain.value=0.5; verb.connect(vg); vg.connect(comp);""","""verb.buffer=ir; const vg=AC.createGain(); vg.gain.value=0.5; verb.connect(vg); vg.connect(comp); audioUpgrade(comp);""")
rep("""function bus(){ const g=AC.createGain(); g.gain.value=sfxGain; let n=g;
  if(sfxLP<19000){ const f=AC.createBiquadFilter(); f.type='lowpass'; f.frequency.value=sfxLP; g.connect(f); n=f; }
  n.connect(master); if(sfxVerb>0){ const sg=AC.createGain(); sg.gain.value=sfxVerb; n.connect(sg); sg.connect(verb); } return g; }""",
"""function bus(){ const g=AC.createGain(); g.gain.value=sfxGain; let n=g;
  if(sfxLP<19000){ const f=AC.createBiquadFilter(); f.type='lowpass'; f.frequency.value=sfxLP; g.connect(f); n=f; }
  if(sfxPos){ const p=mkPanner(); panAt(p,sfxPos); n.connect(p).connect(master); } else n.connect(master);
  const v=sfxVerb*(AUDIO.inside?1.3:1); if(v>0){ const sg=AC.createGain(); sg.gain.value=v; n.connect(sg); sg.connect(verb); }
  if(sfxEcho>0&&AUDIO.echo){ const eg=AC.createGain(); eg.gain.value=sfxEcho; n.connect(eg); eg.connect(AUDIO.echo); } return g; }""")
rep("""  const r=()=>0.94+Math.random()*0.12;
  switch(k){""","""  const r=()=>0.94+Math.random()*0.12;
  switch(k){
    case 'honk': [[330,0],[415,0],[330,0.42],[415,0.42]].forEach(([f,d])=>{ tone('square',f,f*0.99,0.34,0.07,d); tone('sawtooth',f*1.005,f,0.34,0.035,d); }); break; // the bus horn: two notes, twice
    case 'bus_jump': noise(900,0.5,0.22,0.6,0,'bandpass',300); noise(3000,0.25,0.06,0.8,0,'highpass'); tone('sine',220,110,0.18,0.06); break;
    case 'storm_close': noise(90,2.6,0.6,0.7,0,'lowpass',45); noise(260,1.2,0.25,0.6,0.05,'lowpass',90); for(let q=0;q<6;q++) noise(1800+Math.random()*2500,0.05,0.06,2,0.05+q*0.07+Math.random()*0.05); break; // thunder""")
rep("""  frPoll(dt); fitView(); updateCamera();""","""  frPoll(dt); fitView(); updateCamera(); audioListen();""")
