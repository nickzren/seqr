import React from 'react'
import toJson from 'enzyme-to-json'
import { shallow, configure } from 'enzyme'
import Adapter from 'enzyme-adapter-react-16'
import { AwesomeBarComponent, AwesomeBarFormInput } from './AwesomeBar'

configure({ adapter: new Adapter() })

test('shallow-render without crashing', () => {
  const wrapper = shallow(<AwesomeBarComponent />)

  expect(toJson(wrapper)).toMatchSnapshot()
})

test('shallow-render AwesomeBarFormInput  without crashing', () => {
  shallow(<AwesomeBarFormInput />)
})
