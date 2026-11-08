const {makeWorldGen,bakeWorld}=require('./gen.js');
function seeded(seed){ return ()=>{ seed=seed+0x6D2B79F5|0; let t=Math.imul(seed^seed>>>15,1|seed); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
const gen=makeWorldGen({FLAT_R:42,MAP_R:800,massifs:4,rng:seeded});
let t0=Date.now(); const W=bakeWorld({gen,HS:2,HALF:832,FLAT_R:42,MAP_R:800,rng:seeded,towns:10,townGap:210,LVL:4,townR:31,loops:3,loopMax:520,maxGrade:0.1,roadW:6,blendMax:34});
console.log('bake ms',Date.now()-t0,'N',W.N,'towns',W.towns.length,W.towns.map(t=>`(${t.u.toFixed(0)},${t.v.toFixed(0)}) f${t.score.toFixed(1)} h${t.avg.toFixed(0)}`).join(' '));
module.exports={W,gen};
