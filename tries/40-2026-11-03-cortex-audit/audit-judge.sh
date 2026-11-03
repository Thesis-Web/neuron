set -u
C=/home/james/.local/bin/cortex
ing() { local out; out=$($C ingest "$1" "$2" 2>&1); printf '%s\n' "$out" | sed 's/^/    /' >&2; printf '%s\n' "$out" | grep -o 'ingest run [0-9]*' | head -1 | awk '{print $3}'; }
J() { $C judge "$1" "$2" "$3" 2>&1 | sed 's/^/    /'; }
echo "== E1 (C2) an echo of the expected sentence; nothing was run"
r=$(ing audit "the command free -m was run and its printed mem line is quoted with the free column"); J audit 2 "$r"
echo "== E2 (C2) an invented number and an invented term"
r=$(ing audit "free -m printed mem free 999999 and the cortex quantum cache confirmed it"); J audit 2 "$r"
echo "== E3 (C1) the true output as a worker would write it, device path and slashes kept"
r=$(ing audit "the command df -h / was run and printed: /dev/sda1 454g 38g 393g 9% / so the avail column is 393g"); if [ -n "$r" ]; then J audit 1 "$r"; else echo "    (nothing to judge: the true output was dropped by the filter)"; fi
echo "== E3b (C1) the true output without the device path"
r=$(ing audit "the command df -h / was run and its printed line shows avail 393g for the root filesystem"); J audit 1 "$r"
echo "== E4 (C1) a newer value for the same thing (a change of state)"
r=$(ing audit "the command df -h / was run again at 23:59 and its printed line shows avail 392g for the root filesystem"); J audit 1 "$r"
echo "== E5 (C1) a contradiction with no observation"
r=$(ing audit "the root filesystem of this machine is full and has no space left"); J audit 1 "$r"
echo "== E6a (C1) off scope, no digit"
r=$(ing audit "the recipe calls for two eggs and a cup of flour whisked until smooth"); J audit 1 "$r"
echo "== E6b (C1) off scope, with a digit"
r=$(ing audit "the recipe calls for 2 eggs and a cup of flour whisked until smooth"); J audit 1 "$r"
echo "== F1 an exact repeat of E3b"
ing audit "the command df -h / was run and its printed line shows avail 393g for the root filesystem" >/dev/null
echo "== F2 the same words in another order"
ing audit "its printed line shows avail 393g for the root filesystem and the command df -h / was run" >/dev/null
echo "== F3 noise lines and a markup line, as one context"
printf '%s\n' '$ df -h /' '● Bash(df -h /)' '/home/james/cortex/cortex.py' '**contract.** satisfied: the root disk has 393g free as df printed' 'EXPECTED: met' | $C ingest audit - 2>&1 | sed 's/^/    /'
echo "== hydrate audit after the tests"
$C hydrate audit 2>&1
echo "== status audit"
$C status audit 2>&1
