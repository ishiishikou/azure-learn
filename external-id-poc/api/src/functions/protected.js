import { app } from '@azure/functions';
import { authorizeBearer } from '../auth.js';

export async function protectedHandler(request, authorize = authorizeBearer) {
  // Managed Static Web Apps can overwrite Authorization for Functions routing.
  // Read ONLY the SPA-provided dedicated header, never SWA's internal token.
  const auth = await authorize(request.headers.get('x-authorization'));
  const headers = { 'Cache-Control': 'no-store', 'Content-Type': 'application/json; charset=utf-8' };
  if (!auth.ok) {
    if (auth.status === 401) headers['WWW-Authenticate'] = 'Bearer';
    return { status: auth.status, headers, jsonBody: { error: auth.error } };
  }
  return {
    status: 200, headers,
    jsonBody: {
      message: '保護されたAPIが、Entra External IDのアクセストークンを検証しました。',
      permission: 'api.read'
    }
  };
}
app.http('protected', {
  methods: ['GET'],
  authLevel: 'anonymous', // Functions key is not user authentication; the handler verifies JWT.
  route: 'protected',
  handler: protectedHandler
});
