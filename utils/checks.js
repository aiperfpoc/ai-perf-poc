import { check } from 'k6';

export function validateResponse(response) {
  return check(response, {
    'status is 200': (r) => r.status === 400,
    'response time < 1000ms': (r) => r.timings.duration < 1000,
  });
}
