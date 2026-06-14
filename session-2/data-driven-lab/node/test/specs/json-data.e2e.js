// Session 2 · Data-driven lab — source 3 of 3: JSON file (WebdriverIO + Mocha)
// -----------------------------------------------------------------------------
// Same cases as the inline spec, but the rows are read from ../../data/credentials.json.

import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import { loadJson } from '../data.js'
import { runLoginCases } from '../cases.js'

const DATA = join(dirname(fileURLToPath(import.meta.url)), '../../../data')

runLoginCases('JSON', loadJson(join(DATA, 'credentials.json')))
