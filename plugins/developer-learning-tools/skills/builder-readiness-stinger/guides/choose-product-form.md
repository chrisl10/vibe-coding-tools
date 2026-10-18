# Choose what kind of product to build

Use [the worksheet](../references/templates/product-form-worksheet.md), digest and [cases](../references/examples/product-form-cases.md). Start with the job people need to finish. Framework choices come later.

1. Read supplied context. Ask only missing facts that change the choice: who uses it, what they finish, where they use it, what must work without internet, device/files/background needs, an existing app it must live inside, data/services it must reach, distribution, learner experience and actual owner/permission constraints.
2. Define terms near use. A website delivers linked pages. A web app lets people complete interactive work in a browser; the two can overlap. A desktop/mobile app is a device-delivered interface with platform needs to qualify. An integration moves data or actions between systems. A plugin works inside a named host. A command-line tool accepts typed commands. These forms can combine, but do not recommend a bundle without a real requirement.
3. Use the table below as prompts, not an automatic selector. Recommend ONE provisional main form when facts support it, with a one-sentence reason and one decisive condition to qualify. If that condition is unknown and changes the form, ask that question before choosing. Continue independent explanations.
4. Propose one representative behavior and its success/failure evidence. Identify actual selected Web Stack, Desktop/native, Mobile/platform or Integration owner as appropriate through trusted Core. Missing selection stays a gap; do not invent a Mobile role. Builder Readiness does not select languages/frameworks or prove platform capabilities.
5. Record learning needs, distribution/account prerequisites and operating/data ownership as questions or selected-owner handoffs. Do not claim every website needs a database or every device app needs a store. Store/signing/host requirements depend on the actual target and release channel. No accounts, settings, installations or publication are implied.
6. Return one recommendation, qualification condition, first-slice proposal and next owner. Ask one teach-back question: "What job makes this form useful, and what must we check before committing to it?" Mark understanding pending until a supplied response supports an observation.

| Job or constraint to investigate | Possible form to investigate | Decisive question and owner handoff |
|---|---|---|
| Read public information from a link | Website | Is reading/navigation the job, or is private state/action required? Selected web owner. |
| Shared interactive work across browser devices | Web app | What access/data/connection behavior must hold? Selected Web Stack and data/auth owners. |
| Local files, background work or device behavior | Desktop/mobile app | Which exact OS/device behavior and distribution channel? Selected native/platform owner; PWA is not presumed incapable or sufficient. |
| Transfer events or records between existing services | Integration | Which event/API, direction, permission and failure behavior are actually available? Selected integration owner. |
| Add behavior inside an existing application | Host plugin | Which host, extension API, permissions and distribution rules? Selected host owner. Chrome docs are only one example. |
| Repeat a bounded task without a visual interface | Command-line tool | Who can run it, with what input/output/error and access? Selected language/tool owner. |

A tool can be delivered through any of these forms. If the user's word "tool" is ambiguous, clarify its interface and job rather than treating it as a platform. Current captures support definitions and prerequisite prompts; the recommendation still depends on supplied user facts.
