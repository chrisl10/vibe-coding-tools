app.get('*', (req, res) => {
  const html = renderToString(<App />);
  res.send(`<!doctype html><div id="root">${html}</div><script>window.__INITIAL_STATE__ = ${JSON.stringify(state)}</script>`);
});
