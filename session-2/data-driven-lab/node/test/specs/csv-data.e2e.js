// Session 2 · Data-driven lab — source 2 of 3: CSV file (WebdriverIO + Mocha)
// ----------------------------------------------------------------------------
// Same cases as the inline spec, but the rows are read from ../../data/credentials.csv.

import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import { loadCsv } from '../data.js'
import { runLoginCases } from '../cases.js'

const DATA = join(dirname(fileURLToPath(import.meta.url)), '../../../data')

runLoginCases('CSV', loadCsv(join(DATA, 'credentials.csv')))
