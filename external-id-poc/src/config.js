// Public MSAL.js configuration; never put secrets in browser source.
export const API_SCOPE = 'api://def986c6-008f-426e-9ec9-21074cbdaf62/api.read';
export const msalConfig = {
  auth: {
    clientId: '8fc65eb9-6112-4c8b-acd3-c6a348c36e19',
    authority: 'https://externalidpoc2026test.ciamlogin.com/externalidpoc2026test.onmicrosoft.com/',
    knownAuthorities: [
      'externalidpoc2026test.ciamlogin.com',
      '528ade2b-f668-438e-9b4d-c08877ea5f96.ciamlogin.com'
    ],
    redirectUri: window.location.origin + '/redirect.html',
    postLogoutRedirectUri: window.location.origin + '/',
    navigateToLoginRequestUrl: false
  },
  cache: { cacheLocation: 'sessionStorage' }
};
export const loginRequest = { scopes: ['openid', 'profile'] };
