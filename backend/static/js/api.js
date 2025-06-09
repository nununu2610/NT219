const API_BASE = 'https://flask-backend-s1fn.onrender.com';

async function refreshAccessToken(refreshToken) {
  try {
    const res = await fetch(API_BASE + "/auth/refresh", {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + refreshToken,
        'Content-Type': 'application/json'
      }
    });

    if (res.ok) {
      const data = await res.json();
      localStorage.setItem('refresh_token', data.refresh_token); // Cập nhật refresh token mới
      return data.access_token;
    } else {
      return null;
    }
  } catch (err) {
    console.error("Lỗi khi gọi refresh token:", err);
    return null;
  }
}

async function callAPI(endpoint, options = {}) {
  let token = localStorage.getItem('token');
  const refreshToken = localStorage.getItem('refresh_token');

  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };

  if (token) {
    headers['Authorization'] = 'Bearer ' + token;
  }
  options.headers = headers;

  let res = await fetch(API_BASE + endpoint, options);

  if (res.status === 401 && refreshToken) {
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
