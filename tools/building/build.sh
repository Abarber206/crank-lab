#!/bin/bash
# rebuild index.html from the original and all patches, then check that the script parses
cd /home/claude/mg && cp index.orig.html ../crank-lab/index.html && python3 patch.py 2>&1 | tail -1 && cd ../crank-lab && node -e "
const s=require('fs').readFileSync('index.html','utf8'); const i=s.indexOf('<script>\n',s.indexOf('three.min.js')); const j=s.lastIndexOf('\n</script>'); const vm=require('vm'); try{ new vm.Script(s.slice(i+9,j)); console.log('syntax ok'); }catch(e){ console.log('SYNTAX ERROR',e.message); process.exit(1); }"
