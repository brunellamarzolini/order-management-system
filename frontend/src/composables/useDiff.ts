import { isRef, unref } from 'vue'
import _ from 'lodash'

// Generic deep equality check for objects/arrays/primitives
/* export function isEqual<T>(a: T, b: T): boolean {
  if (a === b) return true
  if (typeof a !== typeof b) return false
  if (typeof a !== 'object' || a === null || b === null) return false
  if (Array.isArray(a) && Array.isArray(b)) {
    if (a.length !== b.length) return false
    for (let i = 0; i < a.length; i++) {
      if (!isEqual(a[i], b[i])) return false
    }
    return true
  }
  if (Array.isArray(a) !== Array.isArray(b)) return false
  const aKeys = Object.keys(a as object)
  const bKeys = Object.keys(b as object)
  if (aKeys.length !== bKeys.length) return false
  for (const key of aKeys) {
    if (!bKeys.includes(key)) return false
    if (!isEqual((a as Record<string, unknown>)[key], (b as Record<string, unknown>)[key]))
      return false
  }
  return true
} */

export function hasDiff<T extends object>(
  current: T | null | undefined,
  original: T | null | undefined,
): boolean {
  const cur = isRef(current) ? unref(current) : current
  const orig = isRef(original) ? unref(original) : original
  if (!cur || !orig) return false
  return !_.isEqual(cur, orig)
}

export function useDiff() {
  return {
    hasDiff,
  }
}
