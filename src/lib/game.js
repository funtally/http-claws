import md5 from 'crypto-js/md5';
import { StatusCodes } from 'http-status-codes';

const IMAGE_URI_TEMPLATE = "cats/{}.jpg"
const EXCLUDED_CODES = ["419", "420"];
const HTTP_CODES = Object.keys(StatusCodes).filter(key => key.length == 3);
EXCLUDED_CODES.forEach(code => HTTP_CODES.splice(HTTP_CODES.indexOf(code), 1));

export function randomHTTPCode() {
    const idx = Math.floor(Math.random() * HTTP_CODES.length);
    return HTTP_CODES[idx];
}

export function randomImage() {
    const hash = md5(randomHTTPCode()).toString();
    return IMAGE_URI_TEMPLATE.replace("{}", hash);
}
