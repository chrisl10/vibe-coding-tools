# 15 - Review mobile task flows, not only resized screens

Grounding: C05-C11. Read [system intake](14-react-primitive-contracts.md) first. PRODUCT.md establishes web, wrapped web or native platform; a phone viewport does not prove a native application. Actual visual design/build routes through Impeccable; native targets use its native playbooks and relevant platform engineering owner.

## Start from the task and transitions

Fill [mobile flow acceptance](../templates/mobile-flow-acceptance.md). Ask which task the user must complete, what information is essential at each step, what can be deferred and what interruption is likely. Record the source of those answers. No answer means unknown, not a guessed priority. A wide comparison table may need a compact summary plus detail traversal for the same task; do not delete required comparison information merely to fit width.

Describe entry, navigation, input, review, action, result and recovery. Keep selected item, entered data and navigation context across changes of layout where the product contract requires it. A desktop side panel becoming a mobile detail route needs explicit Back/dismiss semantics and focus restoration. Do not make hover the only route to a required action. Mobile density choices should preserve readable labels, usable targets and discoverable secondary actions; derive tokens/breakpoints from the actual system and content constraints.

## Review the viewport and input environment

Test compact and expanded window states relevant to the product, portrait/landscape, browser zoom/text enlargement, long localized content and RTL when supported. Reflow review includes the 320 CSS-pixel equivalent reference and documented essential two-dimensional exceptions. Table-wide scrolling may be justified; form actions and explanatory content still need evaluation. W3C reflow.

Exercise the real virtual keyboard open/close path on target devices: is the focused field visible; can the user reach errors and the primary action; does dismissal lose data; does navigation move focus to an appropriate target? The layout viewport and visual viewport can differ. Check fixed/sticky controls, bottom overlays, scroll containers, safe-area behavior, browser chrome and viewport mode. env safe-area values alone do not prove keyboard avoidance. MDN viewport, env.

For web targets, measure actual target boxes and spacing against the chosen WCAG criterion. The AA minimum allows specified exceptions; native platform targets use their own documented units and current platform guidance. Do not equate CSS pixels with iOS points or Android dp. Check focus is not entirely obscured by author content; separately record partial obstruction as a usability concern. Target size, focus.

## Acceptance evidence

For every applicable transition record action, expected state, actual observed state, device/browser/OS/version, viewport and zoom, keyboard/assistive technology, source revision and screenshot/trace/test artifact. Screenshots support layout observations; they do not prove Back behavior, announcements, focus or retained input. Require actual task traversal with touch and keyboard where supported, manual screen-reader review, relevant automation and measured reflow. Mark unsupported device coverage unproven.

Record network failure, slow/loading response, empty results, validation error, permission denial, session expiry and cancellation when the flow has those branches. Review browser Back/forward and refresh against the documented preservation rule. Authentication, authorization and backend correctness remain their specialists' responsibilities; a UI error message is not proof of a secure server boundary.

Android adaptive patterns provide a platform-specific reference for window-space adaptation and navigation. They do not prescribe CSS breakpoints or prove a web flow. Apple source routes in this update were unavailable, so owner-specific Apple rules remain unresolved. Android.
