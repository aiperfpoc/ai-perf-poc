import http from 'k6/http';
import { BASE_URL, DEFAULT_HEADERS } from '../utils/config.js';
import { validateResponse } from '../utils/checks.js';

export let options = {
  vus: 5,
  duration: '1m',
};

export default function () {
  let res = http.get(`${BASE_URL}/users`, {
    headers: DEFAULT_HEADERS
  });

  validateResponse(res);
}
