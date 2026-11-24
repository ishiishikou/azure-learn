import { createRemoteJWKSet, jwtVerify } from 'jose';

export const TENANT_ID = '528ade2b-f668-438e-9b4d-c08877ea5f96';
export const API_CLIENT_ID = 'def986c6-008f-426e-9ec9-21074cbdaf62';
export const API_APP_ID_URI = 'api://' + API_CLIENT_ID;
export const REQUIRED_SCOPE = 'api.read';
// The exact 'issuer' and 'jwks_uri' were verified against this tenant's OIDC metadata.
export const ISSUER = 'https://' + TENANT_ID + '.ciamlogin.com/' + TENANT_ID + '/v2.0';
const JWKS_URL = 'https://externalidpoc2026test.ciamlogin.com/' + TENANT_ID + '/discovery/v2.0/keys';
const remoteKeys = createRemoteJWKSet(new URL(JWKS_URL), {
  timeoutDuration: 5000, cooldownDuration: 30000, cacheMaxAge: 600000
});

// Only validate API ACCESS tokens; never store, log or return credentials.
// The JWKS injection is ONLY for local signature-verification tests.
export async function authorizeBearer(header, jwks = remoteKeys) {
  if (typeof header !== 'string' || !/^Bearer\s+\S+$/i.test(header)) {
    return { ok: false, status: 401, error: 'missing_bearer_token' };
  }
  let payload;
  try {
    ({ payload } = await jwtVerify(header.replace(/^Bearer\s+/i, ''), jwks, {
      issuer: ISSUER,
      audience: [API_CLIENT_ID, API_APP_ID_URI],
      algorithms: ['RS256'],
      requiredClaims: ['tid', 'sub', 'iat', 'exp'],
      clockTolerance: 5
    }));
  } catch {
    return { ok: false, status: 401, error: 'invalid_access_token' };
  }
  if (payload.tid !== TENANT_ID || payload.ver !== '2.0') {
    return { ok: false, status: 401, error: 'invalid_access_token' };
  }
  const scopes = typeof payload.scp === 'string' ? payload.scp.split(/\s+/) : [];
  if (!scopes.includes(REQUIRED_SCOPE)) {
    return { ok: false, status: 403, error: 'insufficient_scope' };
  }
  return { ok: true, status: 200 };
}
