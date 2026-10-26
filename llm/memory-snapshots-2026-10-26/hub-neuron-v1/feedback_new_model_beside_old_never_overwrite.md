---
name: feedback_new_model_beside_old_never_overwrite
description: Owner 2026-10-22 - each new version of a Neuron model page is a NEW artifact and a NEW Downloads file beside the old one, so the owner can diff them; never republish over the previous version
metadata:
  type: feedback
---

Owner, verbatim (2026-10-22): "do not just over write the model I have also. create a new one , such that I can compare and diff the two on my own."

**Why:** the owner reviews each model against the last; overwriting destroys the comparison, and twice tonight a publish over an earlier URL would have replaced another version.

**How to apply:** fork the source into a new scratchpad folder before changing anything; publish to a new artifact (new file path); save to Downloads under a new versioned name; leave the older artifact, file and Downloads copies byte-identical (check a hash before and after). Link the previous version from the new page's header. Related: [[reference_neuron_pages_20261021]], [[feedback_smoke_test_pages_before_publish]].
