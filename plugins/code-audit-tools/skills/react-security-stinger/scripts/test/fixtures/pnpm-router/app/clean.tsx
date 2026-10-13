import DOMPurify from 'dompurify';
export const clean = (h: string) => DOMPurify.sanitize(h, { ADD_ATTR: ['target'] });
