#!/bin/bash
# rebuild index.html from the original and all patches, then check that the script parses. Fails loudly (and leaves
# no half-built file) if a patch doesn't apply.
cd /home/claude/mg && cp index.orig.html /tmp/build_index.html
out=$(F=/tmp/build_index.html python3 patch.py 2>&1); st=$?
echo "$out" | tail -1
if [ $st -ne 0 ] || ! echo "$out" | tail -1 | grep -q '^patched'; then echo "BUILD FAILED"; echo "$out" | tail -5; exit 1; fi
cd ../crank-lab && node -e "
const s=require('fs').readFileSync('/tmp/build_index.html','utf8'); const i=s.indexOf('<script>\n',s.indexOf('three.min.js')); const j=s.lastIndexOf('\n</script>'); const vm=require('vm'); try{ new vm.Script(s.slice(i+9,j)); console.log('syntax ok'); }catch(e){ console.log('SYNTAX ERROR',e.message); process.exit(1); }" && cp /tmp/build_index.html /home/claude/crank-lab/index.html
