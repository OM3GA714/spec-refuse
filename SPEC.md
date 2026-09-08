You are building a standalone open-source Python library, autonomously, start to
finish. Do not ask me questions. Do not stop for confirmation. Do not propose
alternatives before building. Build it, test it, and report.

TARGET: a new public GitHub repository under the account I control. Create the
full repository contents. MIT licence. Standard library only except the
dependencies the specification names.

RULES FOR THIS BUILD
- The specification below is prescriptive. Where it names a filename, a
  signature, an exit code, a JSON key or a test id, that is the value to build.
- Write each failing test before the code that satisfies it.
- Never weaken a test to make it pass. If a test is wrong, leave it failing and
  record why in DECISIONS.md.
- Any check that cannot decide must REFUSE (exit 2). It must never pass.
  Exit 0 = checked and correct. Exit 1 = checked and wrong. Exit 2 = could not
  check. Silence must never read as agreement.
- Build nothing the specification does not name. Extra scope is a defect.
- It must run on Windows: encoding="utf-8" on every open(), stdout reconfigured
  at module top.
- Where the specification leaves something open, choose the option that FAILS
  CLOSED, implement it, and record the choice in DECISIONS.md.

WHEN YOU ARE DONE, REPORT IN THIS ORDER
1. Every acceptance case id, with pass / fail / not-implemented and a reason for
   any that is not passing.
2. The conformance or verification result in full, including the explicit
   counts the specification requires.
3. The benchmark table with scaling ratios and the derived complexity estimate.
4. EVERY AMBIGUITY YOU FOUND IN THE SPECIFICATION. This list is the most
   valuable thing you will produce. A build that reports none is assumed not to
   have looked.

The specification follows.

---
