# User API Endpoints

16 endpoints for user operations.

## Endpoints

### PUT /public/api/v1/user/change_login

**Description**: Change User Login.

**Documentation**: [put_public_api_v1_user_change_login.md](put_public_api_v1_user_change_login.md)

---

### PUT /public/api/v1/user/change_password

**Description**: Change User Password.

**Documentation**: [put_public_api_v1_user_change_password.md](put_public_api_v1_user_change_password.md)

---

### POST /public/api/v1/user/create

**Description**: Create User

**Documentation**: [post_public_api_v1_user_create.md](post_public_api_v1_user_create.md)

---

### DELETE /public/api/v1/user/{userId}

**Description**: Delete User.

**Documentation**: [delete_public_api_v1_user_userId.md](delete_public_api_v1_user_userId.md)

---

### GET /public/api/v1/user/{adminId}/can_create_users

**Description**: Get information about admin's ability to create users

**Documentation**: [get_public_api_v1_user_adminId_can_create_users.md](get_public_api_v1_user_adminId_can_create_users.md)

---

### PUT /public/api/v1/user/{adminId}/can_create_users

**Description**: Set if admin can create another users.

**Documentation**: [put_public_api_v1_user_adminId_can_create_users.md](put_public_api_v1_user_adminId_can_create_users.md)

---

### GET /public/api/v1/user/{userId}/hide_profit

**Description**: HideProfit Info.

**Documentation**: [get_public_api_v1_user_userId_hide_profit.md](get_public_api_v1_user_userId_hide_profit.md)

---

### PUT /public/api/v1/user/{userId}/hide_profit

**Description**: Edit User HideProfit.

**Documentation**: [put_public_api_v1_user_userId_hide_profit.md](put_public_api_v1_user_userId_hide_profit.md)

---

### PUT /public/api/v1/user/{userId}/permissions

**Description**: Edit User Permissions.

**Documentation**: [put_public_api_v1_user_userId_permissions.md](put_public_api_v1_user_userId_permissions.md)

---

### PUT /public/api/v1/user/{userId}/edit

**Description**: Edit User.

**Documentation**: [put_public_api_v1_user_userId_edit.md](put_public_api_v1_user_userId_edit.md)

---

### GET /public/api/v1/user/log

**Description**: Get Users Events log.

**Documentation**: [get_public_api_v1_user_log.md](get_public_api_v1_user_log.md)

---

### GET /public/api/v1/user/log/types

**Description**: Get Users Events log.

**Documentation**: [get_public_api_v1_user_log_types.md](get_public_api_v1_user_log_types.md)

---

### POST /public/api/v1/user/2fa/disable

**Description**: Disable two-factor verification for current user

**Documentation**: [post_public_api_v1_user_2fa_disable.md](post_public_api_v1_user_2fa_disable.md)

---

### POST /public/api/v1/user/2fa/enable

**Description**: Enable two-factor verification for current user

**Documentation**: [post_public_api_v1_user_2fa_enable.md](post_public_api_v1_user_2fa_enable.md)

---

### PUT /public/api/v1/user/2fa/secret/generate

**Description**: Generate two-factor secrets for current user, when two-factor authentication is disabled

**Documentation**: [put_public_api_v1_user_2fa_secret_generate.md](put_public_api_v1_user_2fa_secret_generate.md)

---

### GET /public/api/v1/user/2fa/status

**Description**: Get information about if two-factor verification enabled for current user

**Documentation**: [get_public_api_v1_user_2fa_status.md](get_public_api_v1_user_2fa_status.md)

---

