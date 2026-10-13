import { marked } from 'marked';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';

export function Comment({ body, site }) {
  return <div dangerouslySetInnerHTML={{ __html: marked.parse(body) }} />;
}
export function Profile({ user }) {
  return <a href={user.website}>site</a>;
}
export function Safe() {
  return <div dangerouslySetInnerHTML={{ __html: "<b>static</b>" }} />;
}
export function Post({ md }) {
  return <ReactMarkdown rehypePlugins={[rehypeRaw]}>{md}</ReactMarkdown>;
}
export function useWidget(ref, html) {
  ref.current.innerHTML = html;
}
