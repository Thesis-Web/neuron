# NEURON --- Build Chain from Empty Substrate to Acceptance

**Status:** Derived proposed sequence; not yet owner-ratified.\
**Basis:** Neuron Reference Draft 1 (2026-10-23), Neuron Thesis, and the
recovered Neuron builder handoff (2026-10-20).\
**Purpose:** Specify the dependency-ordered chain from the first
permitted physical substrate to a verified, self-developing Neuron,
without silently inventing unresolved mechanisms.

## How to read this plan

This is a build order, not a replacement architecture. The broad chain
in the owner's example is sound: establish the physical boundary, make
neuronal execution work, then add working state, construction, memory,
routing, input/output, sources, reasoning, correction, and
self-development. The key correction is that the builder must not
hand-build every finished module as a conventional application. Only the
permitted bootstrap is hand-laid; Neuron must construct further neuronal
structure through its own runs.

Status labels: - **DESIGN** --- requirement supported by the reference
material. - **EXPERIMENT** --- bounded candidate mechanism requiring a
test written first. - **OPEN** --- the correct mechanism is not
established. - **GATE** --- evidence required before continuing. 
**HYPOTHESIS** --- A guess that we thing will work for open, that
has not been fully built or tested. 

Authority: 1. Explicit owner corrections and ratified requirements
govern intent. 2. The Reference Draft is the primary design reference,
subject to those corrections. 3. The Thesis explains the architecture
but does not override the Reference Draft. 4. Existing builds are
evidence about those builds, not architectural law. 5. Builder ideas are
hypotheses until approved. 6. Preserve failed experiments, receipts, and
superseded states; do not silently rewrite history. 7. Write tests
before implementation and never weaken them merely to pass. 8. If a
necessary design detail is unknown, mark it OPEN and resolve it through
source recovery or a test-first experiment. Do not fill it with a
familiar software pattern.

**Governing invariant:** The seed may lack knowledge, but it must not
lack the means to acquire, test, revise, remember, compose, and use
further capability.

------------------------------------------------------------------------

# Build chain --- one-line overview

1.  Ratify source authority, scope, unknowns, prohibited substitutions,
    builder traps, correct scope grounding procedure,and acceptance tests.
2.  Create the SQLite database and the smallest permitted
    environment/bottom handler.
3.  Hand-lay only the minimum neuron/gate, run-sheet, DNA-row, and
    hop-trigger bootstrap needed to start real neuronal runs.
4.  Prove that actual neuron tables and DNA triggers---not a host
    walker---cause deterministic hops.
5.  Make the run sheet preserve arrival, remainder, bindings, progress,
    child-run associations, findings, and completion state.
6.  Make a neuronal run create another neuron and DNA row through the
    same permitted SQL boundary.
7.  Make neuronal runs that construct the needed read/write/move/copy and
    composition processes.
8.  Add durable run receipts, timeline, state, memory, and correction
    history tied to actual runs.
9.  Build mother as a router/traverser only, with correlated mailbox
    request/reply paths and freeze it after.
10. Connect source brains through their own corpus/inbox/outbox/local
    processing and mother's transport boundary.
11. Build user input → encoder → internal gate identity, and internal
    result → decoder → user output.
12. Unfreeze mother and Build mother/source replies → a separate, 
    traceable secondary input path. freeze mother
13. Make gates trigger subsidiary runs that ask relevant questions and
    return findings to the parent run sheet.
14. Form results from the run sheet, evidence, context, memory, state,
    time, and intended outcome---not from the last gate or canned text.
15. Build comparison, explicit uncertainty, correction, and later
    changed behavior inside the neurons by runs of neurons and triggers 
    or **Hypothesis** runners .
16. Build long-run reuse, shortcut/formula substitution, and selective
    back-population after the long process is proven.
17. Specify and build the sixth brain and its input path only when its
    behavior is concrete enough to test.
18. Close the developmental loop: told → remember → compare → decide →
    learn → execute → observe → evaluate →
    correct → remember → transfer → construct further capability → output
    state and change.
19. Restart from persistent state and repeat without the prior model
    transcript or a manually written handoff.
20. Package the exact tested artifact and claim only the capabilities
    demonstrated by evidence.

------------------------------------------------------------------------

# Phase 0 --- Orient and freeze the task

1.  **Collect controlling sources.** Preserve the Reference Draft,
    relevant owner source passages/corrections, Thesis, and only the
    implementation artifacts needed for this task.
2.  **Classify claims.** Separate owner requirements, measured behavior,
    hypotheses, and open questions. An assistant summary or a passing
    old build is not automatically authority.
3.  **Write the prohibited-substitution list.** No external cognitive
    engine, host-language next-hop walker, hard-coded meaning, canned
    reply, externally supplied semantic matcher, or fixed command list
    standing in for learning.
4.  **Inventory unresolved dependencies.** At minimum: run-sheet fields,
    DNA context fields, roots, definition compilation, graph-axis pull
    functions, result formation, question selection, guessing,
    sixth-brain design, and encoder write-back.
5.  **Write the first acceptance test before coding.** Specify expected
    behavior, a negative control, observable database evidence, and
    failure conditions.

**Gate 0:** Scope, authority, prohibited substitutions, unknowns, and
the first test are recorded.

# Phase 1 --- Physical substrate and bottom boundary

6.  **Create the SQLite database and minimal environment handler.** The
    handler may accept SQL emitted by Neuron, submit it to SQLite, and
    return actual rows/results/errors.
7.  **Restrict handler authority.** It must not infer meaning, choose a
    neuronal continuation, perform learning, select questions, or
    generate an answer.
8.  **Measure relevant SQLite constraints.** Test trigger
    creation/firing, cross-database limits, nesting limits, transaction
    behavior, trigger timing after creation, and error reporting in
    throwaway databases.
9.  **Define failure isolation.** A failed candidate must not corrupt
    accepted state; preserve the exact error and evidence.
10. **Prove transport only.** Run one explicitly supplied SQL operation
    through the boundary and return its actual result/error.

**Gate 1:** The bottom boundary works but performs no hidden cognitive
work.

# Phase 2 --- Minimal neuronal bootstrap

11. **Hand-lay the neuron/gate mechanism.** A neuron is represented as
    its own table/gate, consistent with the Reference Draft. Do not
    collapse distinct meanings merely because they share an external
    spelling.
12. **Hand-lay the minimal run/data-sheet structure.** Add only fields
    with an evidenced role; do not copy conventional interpreter schemas
    by habit.
13. **Hand-lay the minimum DNA-row/hop-trigger mechanism.** A row must
    cause behavior based on actual arrival and relevant
    remainder/continuation context.
14. **Preserve ordered input, arrival, and remainder.** Do not assume a
    spelling alone captures arrival, and do not add a duplicate `next`
    field without evidence.
15. **Prove one hop.** Inspect the actual row, trigger, and state
    transition.
16. **Prove a multi-hop run.** Confirm every hop follows neuronal
    structure and retains the required remainder/bindings.
17. **Test a missing hop.** The system must expose missing
    knowledge/path honestly, not invoke a host fallback.
18. **Test newly created triggers.** Continue at the correct subsequent
    execution point; do not assume a trigger created mid-statement fires
    retroactively.
19. **Decouple logical depth from host stack depth.** Continuation must
    preserve the same run and progress without nesting a full run in
    host calls, restarting completed work, or merely moving a stack
    failure to another execution context.

**Gate 2:** Real neuronal rows/triggers cause a reproducible run,
including honest missing-path behavior.

# Phase 3 --- Run sheet, worksheet, and receipts

20. **Define the run-sheet contract from evidence.** Candidate contents
    include arrival/path, remainder, bindings, context/perspective,
    parent/child associations, questions, findings, pending/completed
    work, and result evidence. Mark unverified fields OPEN.
21. **Separate working state from durable memory.** The worksheet
    supports the current run; memory/timeline/source records preserve
    durable experience.
22. **Preserve parent/child run identity.** A subsidiary finding must be
    traceable to the parent task and conditions that caused it.
23. **Preserve continuation.** Branching, waiting for a source, or
    resuming must retain the correct unresolved work and bindings.
24. **Write a receipt for each run.** Include the relevant path/rows,
    state changes, findings, completion/failure, and result. A summary
    must not replace the trace.

**Gate 3:** A run can be inspected and resumed from actual working
state, not reconstructed from prose.

# Phase 4 --- Neuron constructs more of Neuron

25. **Build the neuronal run that creates a neuron/table.** The host
    must not become the normal builder for every later neuron.
26. **Build the neuronal run that creates a DNA row and its required
    trigger behavior.**
27. **Build reusable construction components.** The Reference Draft
    describes constructions as compositions (for example, `CREATE` and
    `TABLE` plus required syntax/components), not as an opaque external
    template with a substituted name.
28. **Build read/write/move/copy as neuronal processes.** The label or
    external utility call is not proof that Neuron owns the operation.
29. **Build composition.** Use existing neuronal processes to construct
    a more complex process, then use the newly constructed process.
30. **Test invalid construction.** Preserve the actual substrate error
    and receipt; do not claim a nonexistent structure.
31. **Test beyond a fixed outcome list.** The seed must have a real
    route to acquire or construct a needed process not predeclared as a
    command. If the mechanism is unknown, record the blocker rather than
    substituting a narrow learner.

**Gate 4:** Neuron creates further usable neuronal structure through its
own runs.

# Phase 5 --- Timeline, memory, state, and correction history

32. **Build timeline behavior.** Place run receipts in durable
    time/order with relevant state. The timeline points to evidence; it
    does not replace it.
33. **Build memory through neuronal behavior.** Preserve the run and
    conditions, not only the final answer.
34. **Associate memory with the relevant DNA behavior.** The exact
    physical arrangement (shared memory table versus per-row storage)
    must follow accepted design/evidence, not convention.
35. **Preserve prior belief and correction.** A corrected understanding
    is appended; the prior state and reason for change remain
    addressable.
36. **Preserve relevant state/context.** Include only fields with a
    demonstrated role.
37. **Restart and recover.** Stop and restart; recover runs, receipts,
    memory, timeline, state, and correction history without the previous
    model conversation.

**Gate 5:** Experience survives restart, and prior beliefs and their
corrections remain traceable.

# Phase 6 --- Mother, mailboxes, and source-brain boundary

38. **Fix mother's narrow role.** Mother transports requests/replies
    between the main brain, source brains, other brains, and the
    permitted SQL prompt. Mother does not reason, choose meanings, or
    form answers.
39. **Build the brain's outgoing mailbox.** A neuronal process places a
    request with enough identity/context to correlate the reply to its
    run.
40. **Define the mailbox contract.** Specify destination, originating
    run/parent, payload, status, and reply association only where each
    has a distinct purpose; unresolved fields stay OPEN.
41. **Build each source brain's corpus, inbox, outbox, and local
    processing.** A source performs its own work when an ask arrives;
    mother transports the ask and reply.
42. **Prove one request/reply.** The correct source receives the request
    and the result returns to the originating run without semantic
    decisions by mother.
43. **Build mailbox wake/notification.** Select listener, notification,
    or bounded checking only after testing actual substrate/runtime
    constraints. The exact wake mechanism is OPEN until evidenced.
44. **Test duplicates, delay, refusal, empty reply, error, and orphaned
    reply.** Preserve the result of each case.
45. **Enforce the cross-brain boundary.** Only mother crosses between
    brains; do not assume one database's trigger can write directly into
    another database.

**Gate 6:** Correlated requests and replies work; the router remains a
router.

# Phase 7 --- Encoder, decoder, and input/output paths

46. **Build the encoder.** Map external symbols/spellings/keys to
    internal gate identities. The encoder does not guess meanings or do
    neuronal work.
47. **Keep English words out of the main brain's internal
    representation.** External labels belong at the boundary; preserve
    raw source text in its own source record.
48. **Build the user-input mailbox → encoder path.** Preserve original
    input, source, time, and relevant perspective.
49. **Build mother/source reply → secondary input → encoder/brain.**
    Keep it distinct and traceable; source wording is not automatically
    accepted meaning.
50. **Preserve input perspective.** Distinguish user input, source
    reply, internal input, or another brain's input where relevant;
    exact fields remain subject to evidence.
51. **Build the decoder.** Convert internal gate results and supported
    output metadata to external representation without inventing answers
    or supplying templates.
52. **Build brain → mother (if needed) → decoder → user output.** The
    neuronal process determines the result; the boundary only
    transports/renders it.
53. **Test unknown input and unlabeled meaning.** Never pretend an
    unknown word/label or undiscovered meaning was learned.

**Gate 7:** Input/output boundaries work without performing semantic
work on behalf of the brain.

# Phase 8 --- Source learning and definitions

54. **Select a small, justified source set.** Each source is
    independently addressable and has known provenance/limitations; do
    not bulk-import indiscriminately.
55. **Give each source its own corpus/mailbox behavior.**
56. **Preserve raw source evidence and identity.** Summaries or
    normalized records never replace originals.
57. **Build definition acquisition as a neuronal process.** Neuron
    requests and receives definitions; the builder must not type the
    meaning into a gate and call it learning.
58. **Separate definition from executable meaning.** A definition
    describes behavior; it does not prove that behavior has been
    understood or implemented.
59. **Preserve disagreement.** Do not blindly keep only shared words or
    silently select one source. Correct multi-source definition
    compilation remains OPEN until tested.
60. **Test refusal, no result, and contradiction.** Preserve actual
    status and source reason; do not convert a refusal into fabricated
    content.

**Gate 8:** The brain can retrieve source evidence, preserve provenance,
and distinguish evidence from executable meaning.

# Phase 9 --- Internal questions and parallel runs

61. **Make gate/DNA behavior trigger subsidiary runs** that investigate
    relevant memory, timeline, state, source, or other questions through
    neuronal structure.
62. **Associate each child run with its parent and purpose.**
63. **Collect child findings in the parent's worksheet** with
    provenance, status, and unresolved remainder.
64. **Allow relevant subsidiary work while the parent continues**
    without hard-coding a fixed number or universal list of question
    types as the permanent cognitive policy.
65. **Distinguish endpoint, missing knowledge, unanswered question,
    eligible choice, and speculative extension.** They are not
    automatically the same state.
66. **Test a question that changes the result.** Removing its finding
    must change the outcome in the controlled test; otherwise the
    question may be decorative.

**Gate 9:** Subsidiary runs contribute actual findings to parent
reasoning, visible in receipts.

# Phase 10 --- Result formation, evaluation, and correction

67. **Treat result formation as an explicit open mechanism until
    resolved.** The Reference Draft leaves open how expected output
    arises from context, topic, state, knowledge, and conversational
    purpose. Do not add a host answer generator.
68. **Form the result from the run worksheet and its findings,** not
    from the last gate visited or the original input repeated back.
69. **Represent intended/desired outcome through an evidenced
    mechanism.** A generic "goal" field alone does not solve result
    formation.
70. **Build a neuronal comparison process** for actual versus intended
    outcome: improvement, regression, unresolved, or contradiction.
71. **Preserve the basis of the comparison** in the receipt:
    expectation, evidence, result, and reason.
72. **Test correct, plausible-but-wrong, missing, and contradictory
    outcomes.**
73. **Make learning alter executable structure.** Storing a lesson
    string or answer is not sufficient.
74. **Keep candidates tentative until tested.** A source or model
    assertion does not become truth merely by being stated.
75. **Test new processes against held processes, including failures.**
    The precise understanding algorithm is OPEN unless recovered or
    experimentally established.
76. **Demonstrate correction.** Preserve a controlled failure; add a
    correction with provenance; show later behavior changes for the
    right reason.
77. **Test transfer on a different case** that shares the relevant
    process but not surface wording. The answer/process must not be
    directly supplied by the lesson or hard-coded fixture.

**Gate 10:** Results arise from neuronal work and evidence; correction
changes later behavior; at least one transfer case passes.

# Phase 11 --- Long runs, shortcuts, formulas, back-population

78. **Prove the long process first** and preserve its receipt.
79. **Create shortcuts only from evidenced, understood work.** A
    shortcut must retain access to its basis; a repeated supplied
    algorithm or memorized answer is not discovery.
80. **Build formula substitution as neuronal structure.** Preserve
    variable bindings, context, necessary triggers/checks, state
    dependencies, and uncertainty.
81. **Compare long and shortcut runs.** Any omitted necessary check,
    stale result, or changed semantics fails even if faster.
82. **Build selective back-population.** Apply a learned process only
    where the relationship actually fits; record evidence for each
    application.
83. **Keep guessing distinct from known execution.** Shape similarity
    and historical frequency can support a candidate, not verify it.

**Gate 11:** Reuse preserves the meaningful behavior and basis of the
long process; propagation is selective and uncertainty remains explicit.

# Phase 12 --- Sixth brain and internal initiation

84. **Recover/specify the sixth brain's actual behavior.** Its intended
    role includes inner observation, questioning, comparison,
    initiation, and seeking efficiency, but the exact mechanism remains
    OPEN where not specified.
85. **Build the third input path only when the sixth brain produces real
    output.** A mailbox to an empty/inert database is not a sixth sense.
86. **Route sixth-brain input through the permitted boundary** with
    identity, context, and provenance; the encoder/mother must not
    interpret it.
87. **Demonstrate internally initiated work** that asks a relevant
    question or starts a comparison without an external model supplying
    that specific next cognitive step.

**Gate 12:** The sixth brain is demonstrated as a functioning source of
internal work, not just a named database or mailbox.

# Phase 13 --- Close the developmental loop

88. **Trace the dependency closure:** inspect a run → ask a useful
    question → obtain evidence → construct a candidate process → execute
    it → compare result with intention → correct it → preserve history →
    use the correction later.
89. **Audit every host/SQL/source/encoder/decoder path** for hidden
    cognitive work. Physical execution/transport is distinct from
    neuronal decision/composition; a large opaque SQL procedure does not
    become neuronal merely because it is stored in SQLite.
90. **Give Neuron a task whose solution process is not preinstalled.**
    It must gather evidence, construct/test a candidate, and retain the
    result.
91. **Terminate and restart the runtime.** Continue from persistent
    state without the previous model transcript or a manually written
    handoff.
92. **Test corrected transfer after restart.** The brain must use the
    preserved correction on a new case and show the receipt supporting
    its choice.
93. **Demonstrate an unsupplied relationship/process.** Predeclare
    controls that exclude direct memorization and external answer
    supply; preserve alternatives, failed candidates, evidence, and
    subsequent application.
94. **Demonstrate self-construction of further capability** through the
    same neuronal mechanism. If an external model must write the missing
    cognitive mechanism, the bootstrap is not closed.

**Gate 13:** Neuron continues, learns, tests, revises, and builds
further capability through its own neuronal structure after the builder
conversation is absent.

# Phase 14 --- Package and declare completion honestly

95. **Run the complete acceptance suite:** positive tests, negative
    controls, regression tests, restart/recovery, source boundary, and
    architecture-ownership checks.
96. **Verify persistent, non-destructive history:** receipts remain
    addressable; corrections append; failed candidates do not corrupt
    accepted state.
97. **Inspect the exact host and SQL boundary:** no hidden walker,
    semantic engine, answer template, fixed command ceiling, or external
    learning substitute.
98. **Package the exact tested artifact** with reproducible setup,
    source, test definitions/results, schema/trigger evidence, known
    limitations, and hashes.
99. **Publish a capability/evidence matrix** with status VERIFIED /
    PARTIAL / OPEN / FAILED, test, artifact/receipt, limitations, and
    next dependency.
100. **Declare completion only against the acceptance contract.**
     Starting, accepting input, creating tables, traversing a graph, or
     returning an answer are milestones---not proof of a finished
     self-developing brain.

**Final gate:** The exact packaged build passes the agreed
connected-development and transfer tests, and every claim is backed by
evidence.

------------------------------------------------------------------------

## How this corrects the example chain

-   Do **not** hand-lay every final table first. Hand-lay only the
    permitted bootstrap; later structures must be laid by neuronal runs.
-   The run sheet is working state for a task, not just another table.
-   Memory/timeline/state must record actual neuronal runs and preserve
    correction history.
-   Mother routes; it does not reason or decide.
-   A mailbox is transport, not the capability it carries. A sixth-brain
    mailbox does not create a sixth brain.
-   The encoder/decoder are symbol boundaries, not meaning or answer
    generators.
-   Source definitions are evidence describing meanings; they are not
    executable meanings by themselves.
-   The order must close the loop: **construct → execute → observe →
    evaluate → correct → remember → transfer → construct further
    capability**.
-   A correct output is insufficient; tests must show the claimed
    behavior is produced by the intended neuronal mechanism.
-   The sixth brain and other unresolved mechanisms must stay explicitly
    OPEN until sourced or tested.

## First bounded build slice

Before building the rest, prove this small chain end to end:

1.  The permitted SQLite boundary executes neuronal SQL and returns real
    results/errors.
2.  One hand-laid neuron/gate can be entered.
3.  An actual DNA row/trigger causes the next hop.
4.  A short multi-gate run preserves arrival and remainder.
5.  The receipt exposes path and state changes.
6.  A missing continuation is reported honestly.
7.  A neuronal run creates one further neuron/row through the same
    boundary.
8.  A later run uses the newly created structure.
9.  Restart preserves the structure and receipt.
10. A negative control proves that removing the relevant row/trigger
    breaks the behavior.

The proof is not "it can create a table." The proof is: **the brain's
own run creates usable neuronal structure and then uses it.**

## Open questions that must not be silently answered

-   Minimal correct physical schema for run sheet, DNA, memory,
    timeline, state, and receipts.
-   Which context/modifier/perspective fields belong on DNA rows versus
    the run sheet.
-   Measured root operations and which higher operations can be composed
    from them.
-   Correct multi-source definition compilation.
-   Relationship pull functions and graph-axis placement.
-   How expected output is formed from context/state/knowledge/purpose.
-   How worksheet findings produce a reasoned reply tree.
-   How useful internal questions are selected without hard-coded
    cognitive policy.
-   How a new process is tested against held processes and recognized as
    transferable.
-   How guesses are represented, tested, accepted/rejected, and revised.
-   The exact sixth-brain architecture and boundary.
-   Encoder write-back when new meaning/label relationships are learned.
-   Continuation across substrate limits without host-stack dependence.
-   A valid mailbox notification/wake mechanism for the actual runtime.

For each: recover the source anchor, define a small test, record
expected results and failure criteria before execution, preserve the
artifact/receipt, and mark the outcome honestly.

------------------------------------------------------------------------

## Final invariant

**The seed may be ignorant; it may not be incapable of learning.**

The project is not complete when modules exist. It is complete when the
connected mechanisms let Neuron acquire and use new meanings/processes,
preserve evidence and history, correct its own behavior, and construct
further capability through neuronal runs---without a builder or external
model secretly doing the cognition on its behalf.
