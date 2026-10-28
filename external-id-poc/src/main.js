import { PublicClientApplication } from '@azure/msal-browser';
import { msalConfig, loginRequest } from './config.js';
import './styles.css';

const status = document.querySelector('#status');
const signIn = document.querySelector('#sign-in');
const signOut = document.querySelector('#sign-out');
const dashboardLink = document.querySelector('#dashboard-link');
const userName = document.querySelector('#user-name');
const onDashboard = document.body.dataset.page === 'dashboard';

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
      try { await app.logoutRedirect({account, postLogoutRedirectUri: window.location.origin + '/'}); }
      catch (e) {
        setStatus('ログアウトエラー: ' + (e.errorCode || 'unknown_error'), true);
        signOut.disabled = false;
      }
    });
  } catch (e) {
    // Do not render JWT, claims, or authentication responses.
    setStatus('認証初期化エラー: ' + (e.errorCode || 'unknown_error'), true);
  }
}
main();
