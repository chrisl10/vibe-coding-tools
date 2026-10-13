// Adapt to the installed Vue Test Utils/Vitest toolchain. NOT_RUN in the forge.
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import RecordForm from './RecordForm.vue'
describe('RecordForm public behavior', () => {
  it('associates the label and blocks whitespace submission', async () => {
    const wrapper = mount(RecordForm, { props: { formId: 'edit', pending: false } })
    expect(wrapper.get('label').attributes('for')).toBe(wrapper.get('input').attributes('id'))
    await wrapper.get('input').setValue('   ')
    await wrapper.get('form').trigger('submit')
    expect(wrapper.emitted('save')).toBeUndefined()
    expect(wrapper.get('[role="alert"]').text()).toBe('Enter a title.')
    wrapper.unmount()
  })
  it('emits a trimmed intent and blocks repeats while pending', async () => {
    const wrapper = mount(RecordForm, { props: { formId: 'edit', pending: false } })
    await wrapper.get('input').setValue(' Example ')
    await wrapper.get('form').trigger('submit')
    expect(wrapper.emitted('save')).toEqual([['Example']])
    await wrapper.setProps({ pending: true })
    await wrapper.get('form').trigger('submit')
    expect(wrapper.emitted('save')).toHaveLength(1)
    expect(wrapper.get('button').attributes('disabled')).toBeDefined()
    wrapper.unmount()
  })
  it('renders server-provided HTML as literal text', () => {
    const message = '<img src=x onerror=alert(1)>'
    const wrapper = mount(RecordForm, { props: { formId: 'edit', pending: false, serverError: message } })
    expect(wrapper.get('[role="alert"]').text()).toBe(message)
    expect(wrapper.find('img').exists()).toBe(false)
    wrapper.unmount()
  })
})
