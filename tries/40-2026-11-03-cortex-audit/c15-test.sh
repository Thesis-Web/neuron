set -u
C=/home/james/.local/bin/cortex
J() { $C judge "$1" "$2" "$3" 2>&1 | sed 's/^/    /'; }
echo "== 1 the project gate key for every line (build time, once)"; time $C learn --key 2>&1
echo "== 2 status line"; $C status 2>&1 | head -1
echo "== 3 the audit lines re-judged by the shape (no weights yet: what the shape leaves goes to haiku)"
echo "-- E1 echo (C2)";        J audit 2 266392
echo "-- E2 invention (C2)";   J audit 2 266407
echo "-- E3b true 393g (C1)";  J audit 1 266417
echo "-- E4 392g (C1)";        J audit 1 266432
echo "-- E5 contradiction";    J audit 1 266442
echo "-- E6a recipe";          J audit 1 266452
echo "-- E6b recipe 2 eggs";   J audit 1 266469
echo "-- F3 bold line";        J audit 1 266479
echo "-- F3 bare expected met"; J audit 1 266484
echo "== 4 roll back the false close of C2 (its parts are rejected now)"; $C state audit 2 open 2>&1
$C hydrate audit --at 2 2>/dev/null | grep -c "^ACCEPTED" | sed 's/^/    C2 ACCEPTED lines: /'
$C hydrate audit --at 1 2>/dev/null | grep "^ACCEPTED" | sed 's/^/    /'
echo "== 5 marks (the labeled set: the audit by construction, the probe by its live outputs, neuron's closed gates and one drift)"
for m in "audit 266392 dupe" "audit 266407 invention" "audit 266417 completes" "audit 266432 supersedes" "audit 266442 hallucination" "audit 266452 drift" "audit 266469 drift" "probe 266494 completes" "probe 266489 completes" "probe 264894 completes" "probe 264889 completes" "probe 264822 completes" "neuron 266193 drift"; do $C mark $m 2>&1 | sed 's/^/    /'; done
for r in $($C q "select n from cx where kind='verdict' and name='neuron' and json_extract(value,'\$.kind')='completes' and n>0" | python3 -c 'import json,sys; print(" ".join(str(r[0]) for r in json.load(sys.stdin)["rows"]))'); do $C mark neuron $r completes 2>&1 | sed 's/^/    /'; done
echo "== 6 learn"; time $C learn 2>&1
echo "== 7 the unsettled lines again, now with the weights"
echo "-- E2 invention";  J audit 2 266407
echo "-- E5 contradiction"; J audit 1 266442
echo "-- F3 bold line";  J audit 1 266479
echo "== 8 a fresh true line for C2 end to end, then its exact repeat"
r=$($C ingest audit "the command free -m was run and its printed mem line shows free 300 for mem" 2>&1 | tee /dev/stderr | grep -o 'ingest run [0-9]*' | awk '{print $3}')
J audit 2 "$r"
$C ingest audit "the command free -m was run and its printed mem line shows free 300 for mem" 2>&1 | sed 's/^/    /'
echo "== 9 status and load"; $C status audit 2>&1 | head -12; uptime; free -m | sed -n 2p
