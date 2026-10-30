import { PublicClientApplication, InteractionRequiredAuthError } from '@azure/msal-browser';
import { msalConfig, loginRequest, API_SCOPE } from './config.js';
import './styles.css';

const status = document.querySelector('#status');
const signIn = document.querySelector('#sign-in');
const signOut = document.querySelector('#sign-out');
const dashboardLink = document.querySelector('#dashboard-link');
const userName = document.querySelector('#user-name');
const onDashboard = document.body.dataset.page === 'dashboard';
const apiResult = document.querySelector('#api-result');
const apiButtons = ['#test-no-token', '#test-valid-token', '#test-tampered-token']
  .map(selector => document.querySelector(selector)).filter(Boolean);

function setStatus(message, error = false) {
  status.textContent = message;
  status.classList.toggle('error', error);
}
function render(account) {
  if (account) {
    if (userName) userName.textContent = account.name || account.username || '認証済みユーザー';
    signIn?.classList.add('hidden');
    signOut?.classList.remove('hidden');
    dashboardLink?.classList.remove('hidden');
    setStatus('Microsoft Entra External ID による認証が完了しています。');
  } else {
    signIn?.classList.remove('hidden');
    signOut?.classList.add('hidden');
    dashboardLink?.classList.add('hidden');
    setStatus(onDashboard ? '未ログインです。トップページからサインインしてください。' : '未ログインです。');
  }
}
async function callApi(token) {
  const headers = token ? { Authorization: 'Bearer ' + token } : {};
  const response = await fetch('/api/protected', { headers, cache: 'no-store' });
  let data = {};
  try { data = await response.json(); } catch { /* Unavailable API */ }
  return { code: response.status, detail: data.message || data.error || 'API応答を確認してください。' };
}
async function runLab(label, getToken) {
  if (!apiResult) return;
  apiButtons.forEach(b => { b.disabled = true; });
  apiResult.textContent = label + '：APIに問い合わせています…';
  try {
    const token = getToken ? await getToken() : null;
    if (token === null && getToken) return; // Interactive login redirect started.
    const result = await callApi(token);
    apiResult.textContent = label + ' → HTTP ' + result.code + '：' + result.detail;
  } catch (e) {
    apiResult.textContent = label + ' → 実行エラー：' + (e.errorCode || e.message || 'network_error');
  } finally {
    apiButtons.forEach(b => { b.disabled = false; });
  }
}
function tamperJwt(token) {
  const parts = token.split('.');
  if (parts.length !== 3) throw Error('not_a_jwt');
  const i = Math.min(3, parts[1].length - 1);
  parts[1] = parts[1].slice(0, i) + (parts[1][i] === 'A' ? 'B' : 'A') + parts[1].slice(i + 1);
  return parts.join('.');
}

async function main() {
  try {
    const app = new PublicClientApplication(msalConfig);
    await app.initialize();
    const response = await app.handleRedirectPromise();
    if (response?.account) app.setActiveAccount(response.account);
    const account = app.getActiveAccount() || app.getAllAccounts()[0] || null;
    const loginPending = sessionStorage.getItem('ciam-poc-login-pending') === '1';
    if (account && !onDashboard && (response?.account || loginPending)) {
      sessionStorage.removeItem('ciam-poc-login-pending');
      window.location.replace('/dashboard.html');
      return;
    }
    render(account);

    signIn?.addEventListener('click', async () => {
      signIn.disabled = true;
      sessionStorage.setItem('ciam-poc-login-pending', '1');
      setStatus('Microsoft のサインイン画面へ移動します…');
      try { await app.loginRedirect(loginRequest); }
      catch (e) {
        sessionStorage.removeItem('ciam-poc-login-pending');
        setStatus('サインイン開始エラー: ' + (e.errorCode || 'unknown_error'), true);
        signIn.disabled = false;
      }
    });
    signOut?.addEventListener('click', async () => {
      signOut.disabled = true;
      try { await app.logoutRedirect({ account, postLogoutRedirectUri: window.location.origin + '/' }); }
      catch (e) {
        setStatus('ログアウトエラー: ' + (e.errorCode || 'unknown_error'), true);
        signOut.disabled = false;
      }
    });

    if (onDashboard) {
      const getToken = async () => {
        if (!account) throw Error('not_logged_in');
        const request = { scopes: [API_SCOPE], account };
        try { return (await app.acquireTokenSilent(request)).accessToken; }
        catch (e) {
          if (!(e instanceof InteractionRequiredAuthError) && e.errorCode !== 'interaction_required') throw e;
          sessionStorage.setItem('ciam-poc-api-pending', '1');
          await app.acquireTokenRedirect({ ...request, redirectStartPage: window.location.origin + '/dashboard.html' });
          return null;
        }
      };
      document.querySelector('#test-no-token')?.addEventListener('click', () =>
        runLab('トークンなし（期待 401）', null));
      document.querySelector('#test-valid-token')?.addEventListener('click', () =>
        runLab('正しいトークン（期待 200）', getToken));
      document.querySelector('#test-tampered-token')?.addEventListener('click', () =>
        runLab('改ざんトークン（期待 401）', async () => {
          const token = await getToken();
          return token ? tamperJwt(token) : null;
        }));
      if (sessionStorage.getItem('ciam-poc-api-pending') === '1') {
        sessionStorage.removeItem('ciam-poc-api-pending');
        if (account) void runLab('認証更新後の確認（期待 200）', getToken);
      }
    }
  } catch (e) {
    setStatus('認証初期化エラー: ' + (e.errorCode || 'unknown_error'), true);
  }
}
main();
