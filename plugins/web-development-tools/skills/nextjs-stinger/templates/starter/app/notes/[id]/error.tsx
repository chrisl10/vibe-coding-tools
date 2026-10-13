'use client';
// The current archive exposes retry. Verify error props against the installed Next version.
export default function ErrorBoundary({ retry }: { retry: () => void }) {
  return <div role="alert"><p>The note could not be loaded.</p><button onClick={retry}>Try again</button></div>;
}
