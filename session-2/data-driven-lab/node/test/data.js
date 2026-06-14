// Data loaders for the data-driven lab — read the same credential rows from JSON or CSV.
// Each returns: [{ case, user, password, shouldPass: boolean }, ...]

import { readFileSync } from 'node:fs'

export function loadJson(file) {
  return JSON.parse(readFileSync(file, 'utf-8'))
}

// Minimal zero-dependency CSV parser — fine because our values contain no commas/quotes.
// (Real projects: use a library like `csv-parse`.)
export function loadCsv(file) {
  const [header, ...lines] = readFileSync(file, 'utf-8').trim().split(/\r?\n/)
  const keys = header.split(',').map((k) => k.trim())
  return lines.map((line) => {
    const values = line.split(',')
    const row = Object.fromEntries(keys.map((k, i) => [k, (values[i] ?? '').trim()]))
    return {
      case: row.case,
      user: row.user,
      password: row.password,
      shouldPass: row.shouldPass === 'true',   // CSV is all strings → coerce
    }
  })
}
