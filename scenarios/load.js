import http from 'k6/http';
import { BASE_URL, DEFAULT_HEADERS } from '../utils/config.js';
import { validateResponse } from '../utils/checks.js';

export let options = {
  stages: [
    { duration: '1m', target: 1 },
    { duration: '1m', target: 1 },
    { duration: '1m', target: 0 }
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99']
  }
};

export default function () {
  let res = http.get(`${BASE_URL}/users`, {
    headers: DEFAULT_HEADERS
  });

  validateResponse(res);
}