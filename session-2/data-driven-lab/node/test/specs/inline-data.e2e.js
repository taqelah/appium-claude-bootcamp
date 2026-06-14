// Session 2 · Data-driven lab — source 1 of 3: INLINE data (WebdriverIO + Mocha)
// -------------------------------------------------------------------------------
// The credential rows are an array literal right here in the test code — the simplest
// "data-driven" source. Same rows, same runner as the CSV and JSON specs.

import { runLoginCases } from '../cases.js'

const rows = [
  { case: 'valid credentials', user: 'emma@demoapp.com',   password: '10203040',  shouldPass: true },
  { case: 'wrong password',    user: 'emma@demoapp.com',   password: 'wrongpass', shouldPass: false },
  { case: 'unknown user',      user: 'nobody@demoapp.com', password: '10203040',  shouldPass: false },
  { case: 'empty fields',      user: '',                   password: '',          shouldPass: false },
]

runLoginCases('inline', rows)
