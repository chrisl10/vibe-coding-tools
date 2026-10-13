import test from 'node:test'
import assert from 'node:assert/strict'
import { decodeRecord, titleError } from '../references/templates/model.ts'

test('network data has required types and bounded fields; only declared keys leave decoder', () => {
  assert.deepEqual(decodeRecord({ id: 'a', title: '<script>x</script>', secret: 'discard' }),
    { id: 'a', title: '<script>x</script>' })
  for (const input of [null, [], {}, { id: 1, title: 'valid' }, { id: '', title: 'valid' },
    { id: 'x'.repeat(129), title: 'valid' }, { id: 'a', title: false },
    { id: 'a', title: 'x'.repeat(121) }]) assert.throws(() => decodeRecord(input), /Invalid response/)
  assert.equal(decodeRecord({ id: 'x'.repeat(128), title: 'x'.repeat(120) }).title.length, 120)
})

test('form validation rejects blank and oversized drafts while accepting trimmed boundary', () => {
  assert.equal(titleError('   '), 'Enter a title.')
  assert.equal(titleError('x'.repeat(121)), 'Use 120 characters or fewer.')
  assert.equal(titleError(`  ${'x'.repeat(120)}  `), null)
})
