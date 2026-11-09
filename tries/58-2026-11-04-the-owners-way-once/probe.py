# tries/58 probe: how does a called run find the hit that called it? A run whose one span writes, onto the line's sheet (cell 23),
# its own from_ord and the line's receipts (id:pos:gate); bound to the word probe at (heard, :). Then "probe : x" typed and read back.
import sys; sys.path.insert(0, '.')
from nkdoor import Door
d = Door(sys.argv[1])
span = ("BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , 23 , 1 , "
        "'from_ord=' || ( SELECT from_ord FROM run WHERE id = me ) || ' from_run=' || ( SELECT from_run FROM run WHERE id = me ) || ' above=' || above || ' me=' || me || ' receipts=' || "
        "( SELECT group_concat ( id || ':' || pos || ':' || gate , ' ' ) FROM run_receipt WHERE run = above ) || ' hits=' || "
        "coalesce ( ( SELECT group_concat ( ord || ':' || pos || ':' || gate || ':' || before || ':' || next , ' ' ) FROM hit WHERE run = above ) , 'none' ) ; BUILD")
r1 = d.typed(span); run1 = r1.get('run')
print('the probe run', run1, 'replies:', d.replies(run1)[:3])
g = d.gate('probe') or (d.typed('probe', quiet=True) and d.gate('probe'))
print('probe gate', g)
r2 = d.typed('BUILD INSERT INTO dna ( gate , shard , before , trigger , call , spawn , times ) VALUES ( %d , NULL , 1 , 68 , %d , NULL , 0 ) ; BUILD' % (g, run1))
print('bind replies:', d.replies(r2.get('run'))[:2])
r3 = d.typed('probe : x')
sh = d.sheet(r3.get('run')); print('cell 23 of the line:', sh.get(23))
r4 = d.typed('a probe : y')
sh = d.sheet(r4.get('run')); print('cell 23 of the second line (probe at pos 3):', sh.get(23))
