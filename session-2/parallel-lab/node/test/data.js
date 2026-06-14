// Data loader for the parallel lab — read the credential rows from JSON.
// Returns: [{ case, user, password, shouldPass: boolean }, ...]

import { readFileSync } from 'node:fs'

export function loadJson(file) {
  return JSON.parse(readFileSync(file, 'utf-8'))
}
