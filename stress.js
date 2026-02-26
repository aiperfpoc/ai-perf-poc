import http from 'k6/http';
import { BASE_URL } from '../utils/config.js';

export let options = {
  stages: [
    { duration: '2m', target: 50 },
    { duration: '5m', target: 150 },
    { duration: '2m', target: 0 }
  ]
};

export default function () {
  http.get(`${BASE_URL}/users`);
}
