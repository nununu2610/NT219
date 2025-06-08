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
      headers['Authorization'] = 'Bearer ' + newAccessToken;

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
    const contentType = res.headers.get("Content-Type") || "";
    if (contentType.includes("application/json")) {
      const errorData = await res.json();
      throw new Error(errorData.message || "Lỗi khi gọi API");
    } else {
      const text = await res.text();
      throw new Error(text || "Lỗi không xác định");
    }
  }

  const contentType = res.headers.get("Content-Type") || "";
  if (contentType.includes("application/json")) {
    return res.json();
  } else {
    return res.text(); // hoặc trả về { message: text } nếu bạn cần đồng nhất
  }


}
