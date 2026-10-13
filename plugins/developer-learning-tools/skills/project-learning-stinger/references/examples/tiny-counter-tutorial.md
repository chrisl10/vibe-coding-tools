# Building a tiny practice counter

By the end of this tutorial, you will have a local page with a button and a count you can change.

This tutorial is for a learner practicing basic page structure, styling and one JavaScript event. Use a text editor and browser you already have. Ask the tutor for a chat-only walkthrough if those tools are unavailable. Creating an exercise file requires permission for that file; use a new practice location, not an existing app file. No package, account, network request or deployment is needed.

## Creating the page

Create a new file named `counter.html` in your agreed practice folder. Add the complete example below, or ask the tutor to reveal it after your first attempt. The matching [example file](counter.html) is the worked solution.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Practice counter</title>
  <style>
    body { font: 1.125rem system-ui, sans-serif; margin: 2rem; }
    button { font: inherit; padding: 0.75rem; }
    button:focus-visible { outline: 3px solid #003399; outline-offset: 3px; }
  </style>
</head>
<body>
  <main>
    <h1>Practice counter</h1>
    <p>Completed practice steps: <output id="count" aria-live="polite">0</output></p>
    <button id="add-step" type="button">Add one practice step</button>
  </main>
  <script>
    const countOutput = document.querySelector("#count");
    const addStepButton = document.querySelector("#add-step");
    let count = 0;
    addStepButton.addEventListener("click", () => {
      count = count + 1;
      countOutput.textContent = String(count);
    });
  </script>
</body>
</html>
```

Open the file in your browser. Expect a heading, a zero and a button. Tell the tutor what you actually see. A failed local open is an environment result, not proof you cannot learn.

## Naming the button

Predict which visible words change when you edit the words between the opening and closing button tags. Change the button label to `Count my practice step`. Reload the page and compare your prediction with the visible button name. Keep a descriptive label.

## Styling one control

Predict how adding `border: 2px solid #333333;` to the `button` rule changes the control. Add that declaration, save and reload. Use Tab to reach the button and check that focus remains visible. Do not remove the focus outline to make the page look cleaner. Record the actual result.

## Counting a click

Predict the count after two activations. Activate the button twice and compare the result with your prediction. Expected count: `2`. Reload the file. Expected count: `0`, because this exercise has no saved storage.

Use Tab to focus the button, then activate it with Enter and Space. Record the actual browser and observed changes. If you use a screen reader, record whether the count update is announced. The source uses a native button and live output; no universal accessibility result has been established.

## Changing the step

Change `count = count + 1` to `count = count + 2`. Reload, predict the count after two activations, then check it. Expected count: `4`. Explain in your own words which line controls the size of each change. Record whether you used a hint or the worked solution.

## Recording the result

Tell the tutor the prediction, actual result, support used and one thing you would change next. Use the [learning record](../templates/learning-record.md). A finished page proves only the behavior actually observed. A learner's explanation and transfer attempt supply separate learning evidence.

Feature facts: [digest L04-L09](../research/distilled-project-learning.md). This tutorial and its teaching sequence are original Wasp Nest material. Browser, keyboard, zoom and assistive technology proof are NOT_RUN in the source forge unless a separate dated evidence record reports them.
