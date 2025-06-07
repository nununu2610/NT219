const API_BASE = 'http://localhost:30000';

async function callAPI(endpoint, options = {}) {
  let token = localStorage.getItem('token');
  const refreshToken = localStorage.getItem('refresh_token');

  if (!options.headers) options.headers = {};
  options.headers['Content-Type'] = 'application/json';
  if (token) {
    options.headers['Authorization'] = 'Bearer ' + token;
  }

  let res = await fetch(API_BASE + endpoint, options);

  if (res.status === 401) {
    // Access token hết hạn, thử refresh
    const newAccessToken = await refreshAccessToken(refreshToken);
    if (newAccessToken) {
      localStorage.setItem('token', newAccessToken);
      token = newAccessToken;
      options.headers['Authorization'] = 'Bearer ' + newAccessToken;

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

  // Trả về dữ liệu JSON
  return res.json();
}

async function refreshAccessToken(refreshToken) {
  if (!refreshToken) return null;

  try {
    // Thường backend nhận refresh token qua header Authorization
    const res = await fetch(API_BASE + '/auth/refresh', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + refreshToken
      }
    });

    if (!res.ok) return null;

    const data = await res.json();
    return data.access_token;
  } catch (e) {
    console.error('Lỗi khi refresh token:', e);
    return null;
  }
}
