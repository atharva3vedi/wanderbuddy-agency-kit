// Assembles the WanderBuddy feature-walkthrough (9:16, 1080x1920, 30fps).
// Builds per-scene motion clips with baked captions, a VO track padded to scene
// durations, a subtle ambient music bed, then muxes the master.
const cp = require('child_process'); const fs = require('fs'); const path = require('path');
const R = __dirname;
const FF = 'C:/Users/PC/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.2-full_build/bin/ffmpeg.exe';
const S = (p)=>path.join(R,'ui','screens',p);
const C = (p)=>path.join(R,'ui','caps',p);
const B = (p)=>path.join(R,'broll',p);
const A = (p)=>path.join(R,'audio',p);
const CL = (p)=>path.join(R,'clips',p);
const run=(c)=>cp.execSync(c,{stdio:['ignore','ignore','inherit']});
const FR=30;

// scene config: dur = VO dur + tail; panels sum to dur
const scenes = [
  {name:'s00_intro', cap:'intro.png',   vo:'vo0.wav',  dur:16.4, panels:[['vid',B('hero.mp4'),5.5],['vid',B('roadtrip.mp4'),5.5],['vid',B('cafe.mp4'),5.4]]},
  {name:'s01_itin',  cap:'cap1.png',    vo:'vo1.wav',  dur:14.4, panels:[['tall',S('itinerary.png'),14.4]]},
  {name:'s02_budget',cap:'cap2.png',    vo:'vo2.wav',  dur:10.9, panels:[['img',S('budget.png'),10.9]]},
  {name:'s03_chat',  cap:'cap3.png',    vo:'vo3.wav',  dur:10.6, panels:[['tall',S('chat.png'),10.6]]},
  {name:'s04_photos',cap:'cap4.png',    vo:'vo4.wav',  dur:10.5, panels:[['img',S('photos_grid.png'),5.7],['img',S('photos_map.png'),4.8]]},
  {name:'s05_trans', cap:'cap5.png',    vo:'vo5.wav',  dur:15.7, panels:[['img',S('translate.png'),7.6],['img',S('liveconv.png'),8.1]]},
  {name:'s06_road',  cap:'cap6.png',    vo:'vo6.wav',  dur:13.4, panels:[['img',S('roadtrip.png'),13.4]]},
  {name:'s07_disc',  cap:'cap7.png',    vo:'vo7.wav',  dur:14.9, panels:[['vid',CL('community_raw.mp4'),7.1],['img',S('ai.png'),7.8]]},
  {name:'s08_safety',cap:'cap8.png',    vo:'vo8.wav',  dur:7.6,  panels:[['img',S('safety.png'),7.6]]},
  {name:'s09_price', cap:'cap9.png',    vo:'vo9.wav',  dur:21.8, panels:[['img',S('compare.png'),10.2],['img',S('pricing.png'),11.6]]},
  {name:'s10_outro', cap:null,          vo:'vo10.wav', dur:5.6,  panels:[['img',C('endcard.png'),5.6]]},
];

function motion(type, src, dur, out){
  const f = FR*dur;
  let vf;
  if(type==='vid'){
    vf = `scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,eq=brightness=-0.03:saturation=1.06,fps=${FR}`;
    run(`"${FF}" -y -an -i "${src}" -t ${dur} -vf "${vf}" -r ${FR} -pix_fmt yuv420p -c:v libx264 -preset medium -crf 19 "${out}"`);
  } else if(type==='tall'){
    // pan top->bottom over a width-1080 image taller than 1920
    vf = `scale=1080:-1,crop=1080:1920:0:'(ih-1920)*min(t/${dur}\\,1)',setsar=1,fps=${FR}`;
    run(`"${FF}" -y -loop 1 -i "${src}" -t ${dur} -vf "${vf}" -r ${FR} -pix_fmt yuv420p -c:v libx264 -preset medium -crf 19 "${out}"`);
  } else { // img: slow zoom
    vf = `scale=2160:3840,zoompan=z='min(1+0.07*on/${f}\\,1.07)':d=${Math.round(f)}:x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':fps=${FR}:s=1080x1920,setsar=1`;
    run(`"${FF}" -y -loop 1 -i "${src}" -t ${dur} -vf "${vf}" -r ${FR} -pix_fmt yuv420p -c:v libx264 -preset medium -crf 19 "${out}"`);
  }
}

// build each scene
const sceneFiles=[];
for(const sc of scenes){
  const parts=[];
  sc.panels.forEach((p,i)=>{
    const [type,src,dur]=p; const o=CL(`_${sc.name}_p${i}.mp4`);
    motion(type,src,dur,o); parts.push(o);
  });
  let base=CL(`_${sc.name}_base.mp4`);
  if(parts.length===1){ fs.copyFileSync(parts[0],base); }
  else {
    const lst=CL(`_${sc.name}.txt`);
    fs.writeFileSync(lst, parts.map(p=>`file '${p.replace(/\\/g,'/')}'`).join('\n'));
    run(`"${FF}" -y -f concat -safe 0 -i "${lst}" -c copy "${base}"`);
  }
  const out=CL(`${sc.name}.mp4`);
  if(sc.cap){
    run(`"${FF}" -y -i "${base}" -loop 1 -i "${C(sc.cap)}" -filter_complex "[1]format=rgba,fade=in:st=0.35:d=0.55:alpha=1[c];[0][c]overlay=0:0:shortest=1,format=yuv420p" -r ${FR} -c:v libx264 -preset medium -crf 19 -shortest "${out}"`);
  } else { fs.copyFileSync(base,out); }
  sceneFiles.push(out);
  console.log('scene',sc.name);
}

// concat visuals
const vlist=CL('_scenes.txt');
fs.writeFileSync(vlist, sceneFiles.map(p=>`file '${p.replace(/\\/g,'/')}'`).join('\n'));
run(`"${FF}" -y -f concat -safe 0 -i "${vlist}" -c copy "${CL('_video.mp4')}"`);
console.log('video concatenated');

// VO: pad each to scene dur, concat
const voParts=[];
scenes.forEach((sc,i)=>{
  const o=CL(`_vo_${i}.wav`);
  run(`"${FF}" -y -i "${A(sc.vo)}" -af "adelay=250|250,apad" -t ${sc.dur} -ar 44100 -ac 2 "${o}"`);
  voParts.push(o);
});
const volist=CL('_vo.txt'); fs.writeFileSync(volist, voParts.map(p=>`file '${p.replace(/\\/g,'/')}'`).join('\n'));
run(`"${FF}" -y -f concat -safe 0 -i "${volist}" -c copy "${CL('_voall.wav')}"`);
const total=scenes.reduce((a,s)=>a+s.dur,0);
console.log('VO track built; total', total.toFixed(1),'s');

// Music bed: warm 4-chord pad loop (I-vi-IV-V in A), muffled + low volume
const chords=[[220.00,277.18,329.63],[184.99,220.00,277.18],[146.83,220.00,293.66],[164.81,207.65,246.94]];
const cfiles=[];
chords.forEach((ch,i)=>{
  const o=CL(`_ch${i}.wav`);
  const ins=ch.map(f=>`-f lavfi -t 6 -i "sine=frequency=${f}:sample_rate=44100"`).join(' ');
  run(`"${FF}" -y ${ins} -filter_complex "amix=inputs=3,volume=2.2,afade=in:d=0.6,afade=out:st=5.2:d=0.8" -ar 44100 "${o}"`);
  cfiles.push(o);
});
const chlist=CL('_ch.txt');
let seq=[]; for(let k=0;k<Math.ceil(total/24)+1;k++) seq.push(...cfiles);
fs.writeFileSync(chlist, seq.map(p=>`file '${p.replace(/\\/g,'/')}'`).join('\n'));
run(`"${FF}" -y -f concat -safe 0 -i "${chlist}" -c copy "${CL('_chloop.wav')}"`);
run(`"${FF}" -y -i "${CL('_chloop.wav')}" -af "lowpass=f=850,aecho=0.8:0.88:110:0.35,volume=0.05" -t ${total} "${CL('_music.wav')}"`);
console.log('music bed built');

// Final mux: video + (VO amix music)
const FINAL=path.join(R,'final','WanderBuddy_Feature_Walkthrough.mp4');
run(`"${FF}" -y -i "${CL('_video.mp4')}" -i "${CL('_voall.wav')}" -i "${CL('_music.wav')}" ` +
    `-filter_complex "[1:a]volume=1.0[v];[2:a]volume=1.0[m];[v][m]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]" ` +
    `-map 0:v -map "[a]" -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest "${FINAL}"`);
console.log('DONE ->', FINAL);
