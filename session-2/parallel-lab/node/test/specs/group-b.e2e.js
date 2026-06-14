// Session 2 · Parallel lab — Device B's shard (second half of the credential rows).
// wdio.conf.js pins this spec to emulator-5556 (systemPort 8201); group-a.e2e.js runs
// on emulator-5554 at the SAME time.

import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import { loadJson } from '../data.js'
import { runLoginCases } from '../cases.js'

const DATA = join(dirname(fileURLToPath(import.meta.url)), '../../../data')
const rows = loadJson(join(DATA, 'credentials.json')).slice(2)   // second half

runLoginCases('device B', rows)
