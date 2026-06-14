// Session 2 · Parallel lab — Device A's shard (first half of the credential rows).
// wdio.conf.js pins this spec to emulator-5554 (systemPort 8200); group-b.e2e.js runs
// on emulator-5556 at the SAME time. Together the two devices cover all 4 rows in
// roughly half the wall-clock of running them one after another.

import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import { loadJson } from '../data.js'
import { runLoginCases } from '../cases.js'

const DATA = join(dirname(fileURLToPath(import.meta.url)), '../../../data')
const rows = loadJson(join(DATA, 'credentials.json')).slice(0, 2)   // first half

runLoginCases('device A', rows)
