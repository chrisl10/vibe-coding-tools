# Constructed motion cases

These are source review scenarios, not executed UI tests. Every browser/device result is NOT_RUN. Use the worksheet and an actual target to establish behavior.

| Case | Failure to catch | Expected review decision |
|---|---|---|
| A toast is translated in; reduced mode sets animation:none, but dismissal is registered only in animationend. | Static users cannot finish the task. | Reject; make semantic dismissal independent and observe both paths. |
| A card starts opacity:0 and removes its reveal animation in reduced mode. | Content remains invisible. | Reject; base state must contain usable information. |
| A modal looks closed but focus remains trapped during its exit transition. | Visual close and keyboard state disagree. | Reject; use the primitive's semantic lifecycle and observe interruption, Escape and focus return. |
| A carousel runs automatically alongside text for eight seconds and pauses only while focused. | User must surrender focus to pause it. | Reject this pause design; assess an independent pause/stop/hide control and its actual behavior. |
| A prices feed updates every three seconds with no control because each transition is under five seconds. | Automatic updating misuses the duration exemption. | Reject the exemption reasoning; classify SC2.2.2 updating separately. |
| A loading spinner is replaced by a static “Loading” status with identical success/error state changes. | Static path accidentally loses feedback. | Candidate approach; observe actual feedback, accessible naming/status and errors before PASS. |
| CSS honors reduced preference but canvas confetti and smooth JS scrolling continue. | Preference coverage misses non-CSS owners. | Inventory those owners; observe initial and live-change preference handling. |
| A keyboard user can operate everything but has no visible focus after animation. | Keyboard operation is mistaken for focus visibility. | Review SC2.4.7 independently and fix the observed focus indicator. |
| A flashing banner has a pause button and a reduced-mode rule. | Pause/preference is mistaken for flash safety. | Assess SC2.3.1 separately; unmeasured thresholds remain unknown. |
| A diagram's essential moving relationship cannot be paused. | Essentialness is asserted without an alternate information path. | Require the specific information-loss rationale and assess alternatives before any exception conclusion. |

These cases apply the [motion guide](../guides/12-motion-and-interaction.md), grounded in the nine-source digest. They establish coverage intent, not a browser, screen-reader, native or legal conformance result.
