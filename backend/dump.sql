PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    );
INSERT INTO users VALUES(1,'12','$2b$12$IKSw7u2Fe22ehNsg7m55KuFoFfqfxmhoJy3MYt/3FMVOQh6sIlAWO','admin');
INSERT INTO users VALUES(2,'13','$2b$12$7z5xFZclYH8IQEj69KJ3o.2RsugzFanNiJ/syMZKeZpCg2wnpDwoi','user');
INSERT INTO users VALUES(3,'23521126','$2b$12$XMM/Ygi/KbRGibtz941emOoadsYp.xrSLRWJXrT2Vk9wdjYe9/uY.','user');
INSERT INTO users VALUES(4,'nunu1','$2b$12$g5L8ruHzIclWhjT18XGXFOe4PAksD7XrWnV./R8p9.CV1iQaIexfG','user');
INSERT INTO users VALUES(5,'1w32e','$2b$12$20wquZ9.7yanOfppw3cY/.zVrF7m4jEUATldRrL8kXHwCSxZf3Vu2','user');
INSERT INTO users VALUES(6,'2e2qe','$2b$12$nuYNscrJVOQ/TiHrVBy4WORPXOJhap20v9PA4SLSjIXP5TEDTx53.','admin');
INSERT INTO users VALUES(7,'qéq','$2b$12$LMk7Rqgor2afj5GqDurFvucDtcGMOmRT5coH/7WRGj0IHkOWkdzUi','user');
INSERT INTO users VALUES(8,'eqe','$2b$12$PyRm7bQ67eGVGexyYvj23.bwn0OSWn22UdtOkrvnsITizi7r1J/AG','user');
INSERT INTO users VALUES(9,'qedq','$2b$12$RrSA875sZBB6v0p/XKuFO..5P1As0f49jVWsmEcOynW1G1vm2mviO','admin');
INSERT INTO users VALUES(10,'ưđư','$2b$12$yXOthi35fLiDzWX8TQu5p.C11BH7wXh2VfBZfrq/SKXXfLh06PFVq','user');
INSERT INTO users VALUES(11,'qdqd','$2b$12$Ue5a8EmRUGILR5xIW/bPb./svkYCZCN6uHDNl3daUFFcV46eWTTCy','user');
INSERT INTO users VALUES(12,'1','$2b$12$8X186luBJZxN9jJBy6IQJ.1ar5S4sn9zFpkDT9ncfmoaOVmhhmCxi','user');
INSERT INTO users VALUES(13,'2','$2b$12$uVZCSFPlaNdIlIdwrTNfpOOgBY2idXNrlXFOTCIvhkOFcOJhvpXZy','user');
INSERT INTO users VALUES(14,'3','$2b$12$M9S7XmUcqRJagpjMUol8g.KXHsuQrhjJNAwiRQ3s3FI7.6dhh1uva','user');
INSERT INTO users VALUES(15,'4','$2b$12$Hkk9e57afSlpbEEUj3y4YOXf1LC8g6i3f.91iOCQzYd/8eg/pC7b.','user');
INSERT INTO users VALUES(16,'5','$2b$12$3gIeyApk3SDCnOgO3xgFleT/h0PjbX2nliSNFLBCVF9/IbagV/USa','user');
INSERT INTO users VALUES(17,'6','$2b$12$RVVzirPyrsioQV7J2qTYWez.8cj4psQbFwPExopQB5wshQ7JJaeTi','user');
INSERT INTO users VALUES(18,'11','$2b$12$vDomqKvnY5.Bg7hohBIc4urr.4roum0tl.WIKOKt02erIBlci.wgK','user');
INSERT INTO users VALUES(19,'a','$2b$12$FM286Bw2P9QU/HNh6dmZbeV2T0DYz6tGGCjqgwGj3dAa/r6qZmmKG','admin');
INSERT INTO users VALUES(20,'b','$2b$12$XYlihhrEiLuFv3AuI11ohu9K00H53aqm4l5jbis/mMpEL/Mv.53sW','user');
INSERT INTO users VALUES(21,'111','$2b$12$i6wp8qQlHCV3XULOI7WIYejXnYtYYzTkONY/q8QbNUQp74g8wAYwe','admin');
INSERT INTO users VALUES(22,'nunu11111','$2b$12$q7JPqILm2okGVt6c31ENUe7E/VXeADRUd3R1A65300DbVK/lu.mqG','admin');
INSERT INTO users VALUES(23,'hi','$2b$12$fc7M5E4gQ0kkSck0QbvpbevWsWp6KZ8Qf9GKPjKMm7VJcgSxpphCS','admin');
INSERT INTO users VALUES(24,'ju','$2b$12$BvVhCwlD9o1SvKHPq21KjOoFI.nlAU1Emgf6xFNQQ0gJVDv077W0y','admin');
INSERT INTO users VALUES(25,'ki','$2b$12$//9W7niklRlXAb7/dq..ruCK8Bnv3HXnPZ6DSXN8IPKSMc4/xUm1q','admin');
INSERT INTO users VALUES(26,'11111','$2b$12$P9KDiM8cexGtKfAzX/c7Au8yUDzFSqo1O.pUNkY2dYiQADz1jRm9K','user');
INSERT INTO users VALUES(27,'121','$2b$12$etWwq8glrZeKsng5Nxux2e6isE8QX8Cy40GLEqOwH.nNeYRcCPrBO','admin');
CREATE TABLE refresh_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token TEXT NOT NULL UNIQUE,
        expires_at DATETIME NOT NULL,
        revoked BOOLEAN NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
INSERT INTO refresh_tokens VALUES(1,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwianRpIjoiOGY3NGI0ZTQyYjJmZGMzNCIsImV4cCI6MTc0OTU0ODg2Mn0.IpTbFRF-DUApuTY7Il6p_dcyvrq1gVlmWrQiOHybSyI','2025-06-15 09:47:42.508857',1);
INSERT INTO refresh_tokens VALUES(2,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwianRpIjoiOGM3MTlhYjBkMDdmMGIxNSIsImV4cCI6MTc0OTU0ODg3N30.btttgo1cD1CDmrENwWJ2kTHFUhjwvd2uQaPGs_VI5Og','2025-06-15 09:47:57.579380',0);
INSERT INTO refresh_tokens VALUES(3,12,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTIsImp0aSI6IjNjMWU5OTk5NWNmOWVjMWIiLCJleHAiOjE3NDk2Mjc5Mjl9.3V7OZtJQIPIvpMsUeF_iSb77uQi3PEL5EXe9EK83S9U','2025-06-16 07:45:29.001898',0);
INSERT INTO refresh_tokens VALUES(4,14,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTQsImp0aSI6ImIzMzFkYzg2YWMzNzdhOTciLCJleHAiOjE3NDk2Mjc5NDV9.-A0gKdX511rIxyi7qMUtNrJRhF6D0sTEBdJnMV3wz50','2025-06-16 07:45:45.785845',0);
INSERT INTO refresh_tokens VALUES(5,15,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTUsImp0aSI6ImVjNjRlMzAwYzFmN2I5ODUiLCJleHAiOjE3NDk2Mjc5NTR9.py8rXxidVmfMs5pVyESvCIRGzzxZyxsEBDxleb6sgQ8','2025-06-16 07:45:54.145403',0);
INSERT INTO refresh_tokens VALUES(6,19,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTksImp0aSI6ImQxZWVhOTFkYmE5ZjRlOWIiLCJleHAiOjE3NDk2MjgyODh9.XYipmG4YxgLQr6Bjd5rb87fhyR7keunAAFeiaNfvTfE','2025-06-16 07:51:28.349394',1);
INSERT INTO refresh_tokens VALUES(7,20,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjAsImp0aSI6ImRmYTgzMTRmODE0OTE4ZjIiLCJleHAiOjE3NDk2MjgzNTh9.e3qZ0_P7uZTcznJu1oWeAD462j2kZVif3Jm4uJIOeoY','2025-06-16 07:52:38.299593',0);
INSERT INTO refresh_tokens VALUES(8,12,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTIsImp0aSI6ImFjZWVhNTFiOWEzYTRjMTYiLCJleHAiOjE3NDk2Mjk3Mjd9.m-NL64_6fxiOB6bYcrQQrZ3r7QYx0gfd_hbC5pPC83U','2025-06-16 08:15:27.452803',0);
INSERT INTO refresh_tokens VALUES(9,13,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTMsImp0aSI6ImQ5Y2JmYjQzZTc0YmQyYjYiLCJleHAiOjE3NDk2Mjk3MzN9.3-f4rdOpiSLKbQORGraTVi_jiITUPP0UM1DrQp1Qvzw','2025-06-16 08:15:33.369260',1);
INSERT INTO refresh_tokens VALUES(10,14,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTQsImp0aSI6ImM0NGIxZGQ5N2JkODJjZDciLCJleHAiOjE3NDk2Mjk4MTJ9.dZMm977qhDojgRDHK395kXcrCmoP1Y4lsIIWFI7LVXk','2025-06-16 08:16:52.953917',1);
INSERT INTO refresh_tokens VALUES(11,21,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjEsImp0aSI6IjAwOWMyYzZjNGZhMTJmNGYiLCJleHAiOjE3NDk2Mjk4NDR9.YvTXposL3y4aFhCBwdJj0492cAHKqbkUPGCWGGum9WY','2025-06-16 08:17:24.512514',0);
INSERT INTO refresh_tokens VALUES(12,12,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTIsImp0aSI6IjJlYjZiOGRiOTRmOGYwMjUiLCJleHAiOjE3NDk2Mjk5NDZ9.d5BjzglQeK-iShTpsKmd-AxHtDU4MzrVATm1uVyqgbI','2025-06-16 08:19:06.522212',0);
INSERT INTO refresh_tokens VALUES(13,12,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTIsImp0aSI6IjJjYjUwZTJlNzgxM2MwZTMiLCJleHAiOjE3NDk2NTYyODl9.xww-s5nTUACi5H8Tq79e5BPEZOtj08I8Y7fHjZz1NLU','2025-06-16 15:38:09.057188',1);
INSERT INTO refresh_tokens VALUES(14,12,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTIsImp0aSI6ImZlYzQ0NjQ5YzMxYjVhMGMiLCJleHAiOjE3NDk2NTY0MjJ9.uwRKHlGfl0CuBbcbfOUy_qFPmtLNSxkXubS5TMTOi5I','2025-06-16 15:40:22.804077',1);
INSERT INTO refresh_tokens VALUES(15,23,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjMsImp0aSI6ImI5NGUyOTIzMDFjNDY1YjciLCJleHAiOjE3NDk2NTY2NDB9.oOaSoOGIyFBDolDxgjPult4GrOgEGU9HW-Couzo_7FI','2025-06-16 15:44:00.311015',0);
INSERT INTO refresh_tokens VALUES(16,24,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjQsImp0aSI6IjQ2Y2E1ZmQ1ZTU4ZWRmZmMiLCJleHAiOjE3NDk2NTc4Njd9.3C_i4THwmYLMHjSTVoAvro2QQHwLHUwXWkTtN285g2k','2025-06-16 16:04:27.932167',0);
INSERT INTO refresh_tokens VALUES(17,25,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjUsImp0aSI6Ijk0ZDc3NDA5ZTkwOTZkMzQiLCJleHAiOjE3NDk3MDMxMzl9.2d_7ZC1rsVC7aM-6fXDLpdcK1RC0d1QnvWwU7J4eqFs','2025-06-17 04:38:59.131481',0);
INSERT INTO refresh_tokens VALUES(18,26,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjYsImp0aSI6ImFjNTM2M2I1ZWYyMWNiYTUiLCJleHAiOjE3NDk3MTQ1MDB9.kOZ5tYIEAzbWWoiDcfgXdMdWqk6-ooVpnjvLCzmKRs0','2025-06-17 07:48:20.198143',0);
INSERT INTO refresh_tokens VALUES(19,27,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjcsImp0aSI6IjBiMGFjMmNmNjhhMzhlNzkiLCJleHAiOjE3NDk3MTQ1Mzh9.Urc60nfLV-MGxZx1rO3zpaqBwyAk1OMybUILQE-766g','2025-06-17 07:48:58.811100',0);
CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL
    );
INSERT INTO products VALUES(1,'gAAAAABoRpijEQtbF0v4w1AQyeRqgjtKw3qr7ZUXjsM_quGCmv6UV7xaq_TzJbuXirIhGgMwkLj1R3sf3BMhE_-_l-ag3MOplw==','gAAAAABoRpijT9OSNwnSR5vBrgNEi46JrPLLQxrRm7nCPVH6y_TtSn7PcqCGfIMgu8pQ1SGLd_t-Gv1mnXLQMRP6WgsRN79lCA==',100000.0);
INSERT INTO products VALUES(2,'gAAAAABoRpisgLtMchEdqk90mxI5HjAi5lNu5f7yOQTyp57V4NcMAf74hG1yjyFNuR_GMrPQchvyLUul7N4epm9A2MKEOZvsIA==','gAAAAABoRpisOqKpdFCdex7n-6FFwE0gcvVCglrpOScynS_nT_Ru3fAniGqiiAWjon6E-T0bDoz3W97znyt6s1QE4J3_XPQ_gw==',120000.0);
INSERT INTO products VALUES(3,'gAAAAABoR-N0kSTUt9y8tfPApStC5tk3dJxG2BuCfVqyaY3XFSsW2NmkEMYFTTMf1p9RaNkkyHW3tKqY63q16-4jJ_FTJj5e1w==','gAAAAABoR-N0AMm2V0MsAdWvXv2K3CxaL5eY2JY7ijqEpVTFGwBiy6b4PhLDGZbTvukES2T4_QAnJPfDnXxZOFePt2Yn_uwYtg==',11111.0);
CREATE TABLE logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, ip_address TEXT, user_agent TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
INSERT INTO logs VALUES(1,2,'Đăng ký','2025-06-08 09:47:36','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(2,2,'Đăng nhập','2025-06-08 09:47:42','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(3,2,'Xem danh sách sản phẩm','2025-06-08 09:47:43',NULL,NULL);
INSERT INTO logs VALUES(4,2,'Đăng xuất','2025-06-08 09:47:46','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(5,2,'Đăng nhập thất bại (sai mật khẩu)','2025-06-08 09:47:51','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(6,2,'Đăng nhập thất bại (sai mật khẩu)','2025-06-08 09:47:54','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(7,2,'Đăng nhập','2025-06-08 09:47:57','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(8,2,'Xem danh sách sản phẩm','2025-06-08 09:47:58',NULL,NULL);
INSERT INTO logs VALUES(9,3,'Đăng ký','2025-06-09 07:42:58','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(10,4,'Đăng ký','2025-06-09 07:43:07','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(11,5,'Đăng ký','2025-06-09 07:43:13','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(12,6,'Đăng ký','2025-06-09 07:43:18','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(13,7,'Đăng ký','2025-06-09 07:43:25','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(14,8,'Đăng ký','2025-06-09 07:43:31','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(15,9,'Đăng ký','2025-06-09 07:43:37','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(16,10,'Đăng ký','2025-06-09 07:43:43','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(17,11,'Đăng ký','2025-06-09 07:43:49','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(18,4,'Đăng nhập thất bại (sai mật khẩu)','2025-06-09 07:44:40','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(19,12,'Đăng ký','2025-06-09 07:44:47','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(20,13,'Đăng ký','2025-06-09 07:44:53','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(21,14,'Đăng ký','2025-06-09 07:45:01','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(22,15,'Đăng ký','2025-06-09 07:45:08','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(23,16,'Đăng ký','2025-06-09 07:45:16','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(24,17,'Đăng ký','2025-06-09 07:45:23','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(25,12,'Đăng nhập','2025-06-09 07:45:29','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(26,12,'Xem danh sách sản phẩm','2025-06-09 07:45:30',NULL,NULL);
INSERT INTO logs VALUES(27,14,'Đăng nhập','2025-06-09 07:45:45','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(28,14,'Xem danh sách sản phẩm','2025-06-09 07:45:47',NULL,NULL);
INSERT INTO logs VALUES(29,15,'Đăng nhập','2025-06-09 07:45:54','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(30,15,'Xem danh sách sản phẩm','2025-06-09 07:45:55',NULL,NULL);
INSERT INTO logs VALUES(31,12,'Đăng nhập thất bại (sai mật khẩu)','2025-06-09 07:47:38','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(32,18,'Đăng ký','2025-06-09 07:47:43','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(33,18,'Đăng nhập thất bại (sai mật khẩu)','2025-06-09 07:47:49','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(34,19,'Đăng ký','2025-06-09 07:50:55','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(35,20,'Đăng ký','2025-06-09 07:51:21','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(36,19,'Đăng nhập','2025-06-09 07:51:28','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(37,19,'Xem danh sách sản phẩm','2025-06-09 07:51:29',NULL,NULL);
INSERT INTO logs VALUES(38,19,'Đăng xuất','2025-06-09 07:51:30','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(39,20,'Đăng nhập','2025-06-09 07:52:38','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(40,20,'Xem danh sách sản phẩm','2025-06-09 07:52:39',NULL,NULL);
INSERT INTO logs VALUES(41,12,'Đăng nhập','2025-06-09 08:15:27','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(42,13,'Đăng nhập','2025-06-09 08:15:33','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(43,13,'Xem danh sách sản phẩm','2025-06-09 08:15:34',NULL,NULL);
INSERT INTO logs VALUES(44,13,'Đăng xuất','2025-06-09 08:15:36','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(45,14,'Đăng nhập','2025-06-09 08:16:52','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(46,14,'Xem danh sách sản phẩm','2025-06-09 08:16:54',NULL,NULL);
INSERT INTO logs VALUES(47,14,'Xem danh sách sản phẩm','2025-06-09 08:16:57',NULL,NULL);
INSERT INTO logs VALUES(48,14,'Đăng xuất','2025-06-09 08:17:00','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(49,21,'Đăng ký','2025-06-09 08:17:18','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(50,21,'Đăng nhập','2025-06-09 08:17:24','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(51,21,'Xem danh sách sản phẩm','2025-06-09 08:17:25',NULL,NULL);
INSERT INTO logs VALUES(52,21,'Thêm sản phẩm: 1','2025-06-09 08:17:39',NULL,NULL);
INSERT INTO logs VALUES(53,21,'Thêm sản phẩm: 2','2025-06-09 08:17:48',NULL,NULL);
INSERT INTO logs VALUES(54,21,'Xem danh sách sản phẩm','2025-06-09 08:17:51',NULL,NULL);
INSERT INTO logs VALUES(55,21,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:18:03','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(56,21,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:18:14','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(57,12,'Đăng nhập','2025-06-09 08:19:06','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(58,12,'Xem danh sách sản phẩm','2025-06-09 08:19:07',NULL,NULL);
INSERT INTO logs VALUES(59,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:09','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(60,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:11','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(61,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:13','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(62,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:15','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(63,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:17','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(64,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:19','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(65,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:20','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(66,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:22','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(67,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:23','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(68,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:25','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(69,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:26','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(70,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:28','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(71,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:29','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(72,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:31','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(73,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:33','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(74,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:35','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(75,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:37','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(76,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:39','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(77,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:41','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(78,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 08:19:43','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(79,22,'Đăng ký','2025-06-09 15:37:51','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(80,4,'Đăng nhập thất bại (sai mật khẩu)','2025-06-09 15:37:58','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(81,4,'Đăng nhập thất bại (sai mật khẩu)','2025-06-09 15:38:02','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(82,12,'Đăng nhập','2025-06-09 15:38:09','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(83,12,'Xem danh sách sản phẩm','2025-06-09 15:38:10',NULL,NULL);
INSERT INTO logs VALUES(84,12,'Đăng xuất','2025-06-09 15:38:14','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(85,12,'Đăng nhập','2025-06-09 15:40:22','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(86,12,'Xem danh sách sản phẩm','2025-06-09 15:40:24',NULL,NULL);
INSERT INTO logs VALUES(87,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 15:40:30','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(88,12,'Thêm sản phẩm 2 vào giỏ hàng','2025-06-09 15:40:34','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(89,12,'Thêm sản phẩm 1 vào giỏ hàng','2025-06-09 15:40:44','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(90,12,'Xem danh sách sản phẩm','2025-06-09 15:40:54',NULL,NULL);
INSERT INTO logs VALUES(91,12,'Đăng xuất','2025-06-09 15:40:57','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(92,23,'Đăng ký','2025-06-09 15:43:52','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(93,23,'Đăng nhập','2025-06-09 15:44:00','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(94,23,'Xem danh sách sản phẩm','2025-06-09 15:44:02',NULL,NULL);
INSERT INTO logs VALUES(95,24,'Đăng ký','2025-06-09 16:04:21','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(96,24,'Đăng nhập','2025-06-09 16:04:27','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(97,24,'Xem danh sách sản phẩm','2025-06-09 16:04:29',NULL,NULL);
INSERT INTO logs VALUES(98,25,'Đăng ký','2025-06-10 04:38:51','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(99,25,'Đăng nhập','2025-06-10 04:38:59','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(100,25,'Xem danh sách sản phẩm','2025-06-10 04:39:00',NULL,NULL);
INSERT INTO logs VALUES(101,26,'Đăng ký','2025-06-10 07:48:14','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(102,26,'Đăng nhập','2025-06-10 07:48:20','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(103,26,'Xem danh sách sản phẩm','2025-06-10 07:48:21',NULL,NULL);
INSERT INTO logs VALUES(104,26,'Xem danh sách sản phẩm','2025-06-10 07:48:26',NULL,NULL);
INSERT INTO logs VALUES(105,26,'Xem danh sách sản phẩm','2025-06-10 07:48:28',NULL,NULL);
INSERT INTO logs VALUES(106,27,'Đăng ký','2025-06-10 07:48:52','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(107,27,'Đăng nhập','2025-06-10 07:48:58','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
INSERT INTO logs VALUES(108,27,'Xem danh sách sản phẩm','2025-06-10 07:49:00',NULL,NULL);
INSERT INTO logs VALUES(109,27,'Thêm sản phẩm: SẢN PHẨM 1','2025-06-10 07:49:08',NULL,NULL);
INSERT INTO logs VALUES(110,27,'Xem danh sách sản phẩm','2025-06-10 07:49:15',NULL,NULL);
CREATE TABLE carts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    );
INSERT INTO carts VALUES(1,21,1,2);
INSERT INTO carts VALUES(2,12,1,27);
INSERT INTO carts VALUES(3,12,2,1);
INSERT INTO sqlite_sequence VALUES('users',27);
INSERT INTO sqlite_sequence VALUES('logs',110);
INSERT INTO sqlite_sequence VALUES('refresh_tokens',19);
INSERT INTO sqlite_sequence VALUES('products',3);
INSERT INTO sqlite_sequence VALUES('carts',3);
COMMIT;
