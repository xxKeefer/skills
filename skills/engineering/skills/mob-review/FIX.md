# Fix your own code

Step 5 runs this on your own code only, before it writes the report.

The report is for QA, not for decisions, so the panel makes each
fix that a finding names and never asks the user to choose. Skip this part on someone else's code.

1. Sort each finding. A finding is **open** when the persona marked it `future`, or when its fix
   needs a product or design answer that the code and the spec do not give. Every other finding
   is **fixable**, nits included.
2. When a suggestion names two fixes, take the one the persona recommends. With no
   recommendation, take the smaller fix that removes the defect. Do not ask.
3. If the working tree has changes and Step 1 did not review the working tree, fix nothing. A fix
   commit would take in those changes. Mark each finding open, with that reason.
4. Apply each fixable finding as [`apply-review`](../apply-review/SKILL.md) Step 3 says, in the
   Step 4 order. Where that step asks the user, use item 2 of this list.
5. Run the gates as `apply-review` Step 4 says. When a fix fails a gate, or its test cannot go red
   and then green, revert that fix. Mark the finding open, with the reason.
6. Make one commit in the repo's commit convention. The body lists each fix and its finding. For
   a working-tree run, leave the fixes in the working tree. Never push.

The fix commit is the new **reviewed head**. The panel read the head from Step 1, and this step
made the fixes under the gates, so the push step finds no drift from the fix commit.
