// Fuck JavaScript

/**
 * @template T
 * @param {Array<T>} arr
 * @param {number} idx
 * @returns {T}
 */
export function popFrom(arr, idx) {
    return arr.splice(idx)[0];
}

/**
 * @param {number} max
 * @param {number} min
 */
export function randInt(max, min = 0) {
    return min + Math.floor(Math.random() * max);
}

/**
 * @template T
 * @param {Array<T>} arr
 * @returns {T}
 */
export function choice(arr) {
    return arr[randInt(arr.length)];
}
