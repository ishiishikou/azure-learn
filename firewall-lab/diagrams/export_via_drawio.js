const fs=require('fs');
const path=require('path');
let chromium;
try { ({chromium}=require('playwright-core')); }
catch (e) { ({chromium}=require('/workspace/azure-playwright-controller/node_modules/playwright-core')); }
const input=path.join(__dirname,'azure-firewall-basic.drawio');
const png=path.join(__dirname,'azure-firewall-basic.png');
(async()=>{
const xml=fs.readFileSync(input,'utf8');
const browser=await chromium.connectOverCDP(process.env.PLAYWRIGHT_CDP_URL || 'http://127.0.0.1:3333');
const ctx=await browser.newContext({viewport:{width:1800,height:1100}});
const page=await ctx.newPage();
await page.goto('about:blank');
await page.evaluate((xmlText)=>{
  window.__out={events:[],png:null,svg:null,error:null};
  let frame;
  window.addEventListener('message',event=>{
    let msg=event.data;
    if(typeof msg==='string'){try{msg=JSON.parse(msg);}catch(e){return}}
    if(!msg||!msg.event)return;
    window.__out.events.push({name:msg.event,format:msg.format||'',error:msg.error||'',message:(msg.message||'').slice?.(0,100)??''});
    if(msg.event==='init'){
      frame.contentWindow.postMessage(JSON.stringify({
       action:'load',xml:xmlText,autosave:0,exportProtocol:true,title:'Azure Firewall Basic'
      }),'*');
    }else if(msg.event==='load'){
      frame.contentWindow.postMessage(JSON.stringify({
       action:'export',format:'png',scale:1.5,background:'#FFFFFF',
       border:16,size:'page',includeData:true,withSvg:true
      }),'*');
    }else if(msg.event==='export'){
      if(msg.format==='png'||String(msg.data||'').startsWith('data:image/png')){
       window.__out.png=msg.data;window.__out.svg=msg.svg||null;
      }else{window.__out.error=JSON.stringify(msg).slice(0,500)}
    }else if(msg.event==='error'){
      window.__out.error=JSON.stringify(msg).slice(0,500);
    }
  });
  frame=document.createElement('iframe');
  frame.id='editor';
  frame.style='width:1780px;height:1050px;border:0';
  frame.src='https://embed.diagrams.net/?embed=1&proto=json&ui=kennedy';
  document.body.appendChild(frame);
},xml);
console.log('EMBED_STARTED');
await page.waitForFunction(()=>window.__out.png!==null||window.__out.error!==null,{timeout:95000,polling:300});
const details=await page.evaluate(()=>({events:window.__out.events,hasPng:!!window.__out.png,size:window.__out.png?.length,hasSvg:!!window.__out.svg,error:window.__out.error}));
console.log('EXPORT_RESULT',JSON.stringify(details));
if(details.hasPng){
  const base64=await page.evaluate(()=>window.__out.png.split(',')[1]);
  fs.writeFileSync(png,Buffer.from(base64,'base64'));
  if(details.hasSvg){
    const svg=await page.evaluate(()=>window.__out.svg);
    fs.writeFileSync(png.replace('.png','.svg'),svg,'utf8');
  }
  console.log('PNG_EXPORTED',png,'bytes',fs.statSync(png).size);
}
await page.close();await ctx.close();await browser.close();
})().catch(e=>{console.log('ERROR',e.stack?.slice(0,1400));process.exitCode=1});