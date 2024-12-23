import md5 from 'crypto-js/md5';
import { StatusCodes } from 'http-status-codes';

const IMAGE_URI_TEMPLATE = "cats/{}.jpg";
const EXCLUDED_CODES = ["419", "420"];
const UPPERCASE_WORDS = ["URI", "HTTP", "OK"];
const HTTP_CODES = Object.keys(StatusCodes).filter(key => key.length == 3);
EXCLUDED_CODES.forEach(code => HTTP_CODES.splice(HTTP_CODES.indexOf(code), 1));

export function randomHttpCode() {
    return Number(HTTP_CODES[Math.floor(Math.random() * HTTP_CODES.length)]);
}

/**
 * @param {number} httpCode
 * @param {boolean} useMd5
 */
export function imageForHttpCode(httpCode, useMd5 = true) {
    const httpCodeString = httpCode.toString();
    return IMAGE_URI_TEMPLATE.replace("{}", useMd5 ? md5(httpCodeString).toString() : httpCodeString);
}

/**
 * @param {string} word
 */
function mapPhraseWord(word) {
    return UPPERCASE_WORDS.includes(word) ? word : word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
}


/**
 * @param {number} httpCode
 */
export function phraseForHttpCode(httpCode) {
    return StatusCodes[httpCode].split("_").map(mapPhraseWord).join(" ");
}