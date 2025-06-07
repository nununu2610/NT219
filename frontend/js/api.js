const API_BASE = 'http://localhost:30000';

async function callAPI(endpoint, options = {}) {
  let token = localStorage.getItem('token');
  const refreshToken = localStorage.getItem('refresh_token');

  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  }

  if (token) {
    headers['Authorization'] = 'Bearer ' + token;
  }
  options.headers = headers;

  let res = await fetch(API_BASE + endpoint, options);

  if (res.status === 401) {
    // Access token hết hạn, thử refresh
    const newAccessToken = await refreshAccessToken(refreshToken);
    if (newAccessToken) {
      localStorage.setItem('token', newAccessToken);
      headers.set('Authorization', 'Bearer ' + newAccessToken);

      // Gọi lại API với token mới
      res = await fetch(API_BASE + endpoint, options);
    } else {
      alert('Phiên đăng nhập hết hạn, vui lòng đăng nhập lại.');
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
      window.location.href = 'login.html';
      throw new Error('Refresh token hết hạn');
    }
  }

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.message || 'Lỗi khi gọi API');
  }

  return res.json();
}
