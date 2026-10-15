# Motion and interaction

Use this guide when applying `/impeccable animate`, reviewing transitions or adding motion to a surface. Read PRODUCT.md, DESIGN.md and the surface brief first. Keep the existing named commands, bounded inspection and detector gate. This guide adds interaction evidence to that process. Grounding: digest, source hashes.

1. Inventory each CSS/JS transition, scrolling/parallax effect, animated SVG/GIF/video/canvas, skeleton and automatic update. Record trigger, duration/repetition, parallel content, purpose and essentialness rationale in [the worksheet](../templates/motion-interaction-evidence.md). Mark decorative motion as optional. Do not infer a user's preference from no-preference.
2. Design a usable static/default state. Opt into nonessential movement only in the applicable preference branch. Provide the same information, state and controls when motion is disabled; retain loading/status text, errors and completion feedback. Inventory third-party and JS media separately rather than assuming CSS disables them.
3. For JS-driven motion, read the preference initially, subscribe to MediaQueryList change while the surface is mounted and remove subscriptions on teardown. Define behavior if preference changes mid-animation. Do not depend solely on an animation/transition completion callback for semantic state or focus; the motion-disabled path must finish the same task without it.
4. Verify keyboard and focus independently: Tab/Shift+Tab order, activation, Escape where the primitive specifies it, visible focus during changes and a valid destination after close/remove/rerender. Use the established primitive's actual behavior. A focus trap inside an open modal with a working dismissal path is different from a page the user cannot leave. Follow the dialog source; aria-modal alone implements none of this.
5. Assess automatic motion and updates against SC2.2.2, interaction animation against SC2.3.3 AAA, and flashes separately against SC2.3.1. A hover/focus-only pause that monopolizes focus is not an adequate pause mechanism. An “essential” exception must be recorded per activity, not assigned to all loaders or all brand animations.
6. In one batched inspection, use the supported real desktop/mobile/browser environments with default and reduced preference. Observe initial load, a live preference change, keyboard entry/exit, slow/failed loading and interrupted close. Record exact browser/version, target revision, preference mechanism, expected and actual state, focus and screenshots/trace. Emulation proves that browser under that emulation, not device-wide or assistive-technology behavior. When tools are unavailable, mark NOT_RUN and retain the manual work, not PASS.
7. Fix the observed failures in one batch and confirm at most once. Run the existing detector gate for implementation work; detector success is not WCAG conformance or keyboard proof. Hand off Security then independent Quality with the worksheet and remaining manual/assistive-technology checks. Product-specific tokens stay with their designated owner.

Illustrative CSS strategy, not a shipped component:

```css
/* Information is visible and usable in the base state. */
.notice { transform: none; opacity: 1; }
@media (prefers-reduced-motion: no-preference) {
  .notice[data-entering] { animation: notice-enter 160ms ease-out; }
}
@keyframes notice-enter {
  from { transform: translateY(4px); }
  to { transform: none; }
}
```

The duration and displacement are illustrative design values. This fragment supplies no keyboard implementation, automatic-update controls or flash analysis. Never globally hide content, remove focus outlines or shorten every animation to a near-zero duration and declare accessibility complete. Ensure semantic completion remains correct even when no motion event fires.
