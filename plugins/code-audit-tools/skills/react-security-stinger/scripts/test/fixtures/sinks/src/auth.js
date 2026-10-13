// run_tests.py writes a fake key line into a temporary copy at test time (keeps secret scanners quiet)
export function login(t) { localStorage.setItem('authToken', t); }
export function afterLogin() {
  const next = new URLSearchParams(location.search).get('next');
  window.location.href = next;
}
window.addEventListener('message', (e) => { document.body.innerHTML = e.data; });
