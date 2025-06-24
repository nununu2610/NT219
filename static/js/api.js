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
      localStorage.setItem('refresh_token', data.refresh_token);
      return data.access_token;
    } else {
      return null;
    }
  } catch (err) {
    console.error("Lỗi khi gọi refresh token:", err);
    return null;
  }
}

async function callAPI(url, options = {}) {
  const token = localStorage.getItem('token');
  const refreshToken = localStorage.getItem('refresh_token');

  const defaultHeaders = {
    'Content-Type': 'application/json',
  };

  if (token) {
    defaultHeaders['Authorization'] = `Bearer ${token}`;
  }

  let res = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...(options.headers || {})
    }
  });

  // Nếu token hết hạn (401), thử làm mới access_token
  if (res.status === 401 && refreshToken) {
    const newToken = await refreshAccessToken(refreshToken);
    if (newToken) {
      localStorage.setItem('token', newToken);

      // Gọi lại request với token mới
      res = await fetch(`${API_BASE}${url}`, {
        ...options,
        headers: {
          ...defaultHeaders,
          Authorization: `Bearer ${newToken}`,
          ...(options.headers || {})
        }
      });
    }
  }

  const contentType = res.headers.get("Content-Type") || "";
  const isJson = contentType.includes("application/json");
  const data = isJson ? await res.json() : await res.text();

  if (!res.ok) {
    throw new Error(data.message || data || 'Lỗi không xác định');
  }

  return data;
}
