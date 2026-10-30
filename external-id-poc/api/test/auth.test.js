import test from 'node:test';
import assert from 'node:assert/strict';
import { generateKeyPair, exportJWK, createLocalJWKSet, SignJWT } from 'jose';
import { authorizeBearer, TENANT_ID, API_CLIENT_ID, API_APP_ID_URI, ISSUER } from '../src/auth.js';

const { privateKey, publicKey } = await generateKeyPair('RS256');
const jwk = await exportJWK(publicKey);
Object.assign(jwk, { kid: 'local-test-key', alg: 'RS256', use: 'sig' });
const keys = createLocalJWKSet({ keys: [jwk] });

async function tokenFor({ audience = API_CLIENT_ID, issuer = ISSUER,
  scopes = 'api.read', tenant = TENANT_ID, expiry = '1h' } = {}) {
  return new SignJWT({ tid: tenant, ver: '2.0', scp: scopes })
    .setProtectedHeader({ alg: 'RS256', kid: 'local-test-key' })
    .setSubject('sample-user')
    .setIssuer(issuer)
    .setAudience(audience)
    .setIssuedAt()
    .setExpirationTime(expiry)
    .sign(privateKey);
}
test('no bearer => 401', async () => {
  assert.deepEqual(await authorizeBearer(null, keys), {ok:false,status:401,error:'missing_bearer_token'});
});
test('valid signed token => 200', async () => {
  assert.equal((await authorizeBearer('Bearer ' + await tokenFor(), keys)).status, 200);
});
test('App ID URI audience => 200', async () => {
  assert.equal((await authorizeBearer('Bearer ' + await tokenFor({audience:API_APP_ID_URI}), keys)).status, 200);
});
test('tampered signature => 401', async () => {
  const parts = (await tokenFor()).split('.');
  parts[1] = parts[1].slice(0, 3) + (parts[1][3] === 'A' ? 'B' : 'A') + parts[1].slice(4);
  assert.equal((await authorizeBearer('Bearer '+parts.join('.'),keys)).status,401);
});
test('expired => 401', async () => {
  assert.equal((await authorizeBearer('Bearer '+await tokenFor({expiry:Math.floor(Date.now()/1000)-120}),keys)).status,401);
});
test('wrong audience => 401', async () => {
  assert.equal((await authorizeBearer('Bearer '+await tokenFor({audience:'other-resource'}),keys)).status,401);
});
test('wrong issuer => 401', async () => {
  assert.equal((await authorizeBearer('Bearer '+await tokenFor({issuer:'https://untrusted.example/v2.0'}),keys)).status,401);
});
test('wrong tenant => 401', async () => {
  assert.equal((await authorizeBearer('Bearer '+await tokenFor({tenant:'00000000-0000-0000-0000-000000000000'}),keys)).status,401);
});
test('valid signed token without scope => 403', async () => {
  assert.deepEqual(await authorizeBearer('Bearer '+await tokenFor({scopes:'other.permission'}),keys),
    {ok:false,status:403,error:'insufficient_scope'});
});
