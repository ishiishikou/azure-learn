import { PublicClientApplication, InteractionRequiredAuthError } from '@azure/msal-browser';
import { msalConfig, loginRequest, API_SCOPE } from './config.js';
import './styles.css';

const KEY = {
  signedOut: 'ciam-poc-signed-out',
  loginPending: 'ciam-poc-login-redirect',
  consentPending: 'ciam-poc-token-redirect'
};
const status = document.querySelector('#status');
const retry = document.querySelector('#retry');
const authShell = document.querySelector('#auth-shell');
const application = document.querySelector('#application');
const isDashboard = document.body.dataset.page === 'dashboard';

function setStatus(message, error = false) {
  status.textContent = message;
  status.classList.toggle('error', error);
}
function showRetry(message) {
  setStatus(message, true);
  retry?.classList.remove('hidden');
}
function safeErrorCode(error) {
  // Do not print tokens, raw server responses, or personal claims.
  return typeof error?.errorCode === 'string' && /^[a-z0-9_]+$/i.test(error.errorCode)
    ? error.errorCode : 'authentication_failed';
}
function showApplication(account, apiData) {
  if (!isDashboard || !application || !apiData || typeof apiData.message !== 'string') {
    throw new Error('invalid_api_response');
  }
  document.querySelector('#user-name').textContent =
    account.name || account.username || '認証済みユーザー';
  document.querySelector('#api-message').textContent = apiData.message;
  authShell.hidden = true;
  application.hidden = false;
}

async function validateWithApi(token) {
  // Only the backend decides whether access is allowed. No raw JWT is displayed.
  const res = await fetch('/api/protected', {
    method: 'GET',
    cache: 'no-store',
    headers: { Authorization: 'Bearer ' + token }
  });
  if (res.status !== 200) {
    const err = new Error('api_access_denied');
    err.httpStatus = res.status;
    throw err;
  }
  const data = await res.json();
  if (data.permission !== 'api.read' || typeof data.message !== 'string') {
    throw new Error('invalid_api_response');
  }
  return data;
}

async function startLogin(app) {
  retry?.classList.add('hidden');
  setStatus('Microsoft のログイン画面へ移動します…');
  sessionStorage.removeItem(KEY.signedOut);
  sessionStorage.setItem(KEY.loginPending, '1');
  await app.loginRedirect(loginRequest);
}

async function authenticate(app) {
  const redirectResult = await app.handleRedirectPromise();
  const account = redirectResult?.account || app.getActiveAccount() || app.getAllAccounts()[0];

  if (!account) {
    const signedOut = sessionStorage.getItem(KEY.signedOut) === '1';
    const interrupted = sessionStorage.getItem(KEY.loginPending) === '1';
    if (signedOut) {
      showRetry('ログアウトしました。再度利用する場合はサインインしてください。');
    } else if (interrupted) {
      sessionStorage.removeItem(KEY.loginPending);
      showRetry('ログインが完了しませんでした。再度サインインしてください。');
    } else {
      await startLogin(app); // No app UI; immediately go to Microsoft's sign-in.
    }
    return;
  }

  app.setActiveAccount(account);
  sessionStorage.removeItem(KEY.loginPending);
  sessionStorage.removeItem(KEY.signedOut);

  setStatus('APIの利用権限を確認しています…');
  let token;
  try {
    token = (await app.acquireTokenSilent({ scopes: [API_SCOPE], account })).accessToken;
  } catch (error) {
    if (!(error instanceof InteractionRequiredAuthError)) throw error;
    if (sessionStorage.getItem(KEY.consentPending) === '1') {
      sessionStorage.removeItem(KEY.consentPending);
      showRetry('API用トークンを取得できませんでした。再認証してください。');
      return;
    }
    sessionStorage.setItem(KEY.consentPending, '1');
    setStatus('MicrosoftでAPIの利用権限を確認します…');
    await app.acquireTokenRedirect({ scopes: [API_SCOPE], account });
    return;
  }
  sessionStorage.removeItem(KEY.consentPending);

  setStatus('APIでアクセストークンを検証しています…');
  const data = await validateWithApi(token);
  if (!isDashboard) {
    window.location.replace('/dashboard.html');
    return;
  }
  showApplication(account, data);
}

async function main() {
  let app;
  try {
    app = new PublicClientApplication(msalConfig);
    await app.initialize();

    retry?.addEventListener('click', async () => {
      retry.disabled = true;
      try {
        sessionStorage.removeItem(KEY.loginPending);
        sessionStorage.removeItem(KEY.consentPending);
        // Force a new interactive login; do not bypass the API check with cached UI state.
        await startLogin(app);
      } catch (e) {
        showRetry('サインインを開始できませんでした（' + safeErrorCode(e) + '）。');
        retry.disabled = false;
      }
    });
    document.querySelector('#sign-out')?.addEventListener('click', async event => {
      event.currentTarget.disabled = true;
      sessionStorage.setItem(KEY.signedOut, '1');
      try {
        await app.logoutRedirect({
          account: app.getActiveAccount(),
          postLogoutRedirectUri: window.location.origin + '/'
        });
      } catch {
        setStatus('ログアウトに失敗しました。');
        event.currentTarget.disabled = false;
      }
    });
    await authenticate(app);
  } catch (error) {
    // Show no application on any authentication, network, or permission failure.
    if (application) application.hidden = true;
    if (authShell) authShell.hidden = false;
    if (error?.httpStatus === 401) showRetry('APIによる認証に失敗しました（HTTP 401）。');
    else if (error?.httpStatus === 403) showRetry('APIの利用権限がありません（HTTP 403）。');
    else if (error?.httpStatus) showRetry('APIへの接続に失敗しました（HTTP ' + error.httpStatus + '）。');
    else showRetry('認証を完了できませんでした（' + safeErrorCode(error) + '）。');
  }
}
void main();
