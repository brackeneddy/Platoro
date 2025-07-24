# Platoro Product Requirements Document (PRD)

## Document Version

- **Version**: 1.0
- **Date**: July 22, 2025
- **Author**: Bracken Eddy

---

## 1. Overview

Platoro is a premium personal finance platform built to help users connect financial accounts, track spending, set and monitor goals, and receive AI-generated financial recommendations. The platform aims to deliver a modern, gold-standard user experience with secure authentication and seamless backend integration using a serverless stack.

This PRD focuses on Phase 1: User Authentication and Account Management, covering features required to securely onboard and manage users through AWS Cognito, React frontend components, and a Flask backend.

---

## 2. Goals

- Secure and seamless authentication for users
- Cognito-backed user pool with email/password login
- Support for full auth lifecycle: signup, email verification, login, token management, password reset, and logout
- React frontend integration with protected routes
- Backend logging and monitoring through AWS CloudWatch
- Ensure scalability and extensibility for future OAuth and biometric integrations

---

## 3. Features

### 3.1 User Signup

- Email/password-based signup
- Email verification via Cognito-hosted UI
- Backend function handles call to `sign_up` API
- User status transitions from `UNCONFIRMED` to `CONFIRMED` post verification

### 3.2 Email Verification

- Cognito sends verification code
- User enters code via frontend
- Backend confirms signup using `confirm_sign_up`

### 3.3 Login

- User logs in using email/password
- AWS Cognito returns `accessToken`, `idToken`, and `refreshToken`
- Tokens stored locally in frontend (e.g. `localStorage`)

### 3.4 Token Handling

- Tokens are passed via Authorization headers for protected requests
- Refresh token workflow supported on token expiry

### 3.5 Logout

- Clears frontend tokens
- Optionally invalidates refresh token

### 3.6 Forgot Password

- User initiates password reset request
- Cognito sends verification code
- User submits code and new password to confirm

### 3.7 Resend Verification

- Optionally allow re-requesting a verification email for unconfirmed users

---

## 4. Frontend Requirements

### React Pages

- `SignupPage.tsx`
- `LoginPage.tsx`
- `VerifyEmailPage.tsx`
- `ForgotPasswordPage.tsx`
- `ResetPasswordPage.tsx`
- `Dashboard.tsx` (protected)

### State Management

- AuthContext tracks login state
- Axios interceptor injects access token
- ProtectedRoute redirects unauthenticated users

---

## 5. Backend Requirements

### Technologies

- Flask
- AWS Lambda (deployed via SAM/CDK)
- AWS Cognito (User Pool)

### Endpoints

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/account/signup` | POST | Sign up new users |
| `/account/confirm` | POST | Confirm signup with code |
| `/account/login` | POST | Login and return tokens |
| `/account/logout` | POST | Logout (token invalidation optional) |
| `/account/forgot-password` | POST | Initiate reset |
| `/account/reset-password` | POST | Confirm password reset |

---

## 6. Cognito Configuration

### User Pool

- Pool Name: `Platoro-Prod-Users`
- Email required and verified
- Password policy: 8+ chars, upper, lower, number
- Email-only sign-in
- App client without secret
- Token expirations:
  - Access: 60 mins
  - Refresh: 5 days
  - ID: 60 mins
- Hosted UI domain: `platoro.auth.us-east-1.amazoncognito.com`

### App Clients

- Traditional web app (`platoro-client-web`)
- No client secret
- Enabled auth flows:
  - ALLOW_USER_PASSWORD_AUTH
  - ALLOW_REFRESH_TOKEN_AUTH
  - ALLOW_USER_SRP_AUTH

---

## 7. Error Handling

- Frontend catches and displays user-friendly errors
- Backend returns consistent error format:
  ```json
  {
    "error": "User already exists"
  }
  ```

- Logs written to CloudWatch with structured JSON
- Monitoring alerts on auth failures > threshold

---

## 8. Security Considerations

- All API routes are HTTPS-only
- JWT tokens validated in backend
- User inputs validated client and server side
- Tokens stored securely (no localStorage for mobile apps)
- Brute-force protection via Cognito account lockout

---

## 9. Future Enhancements

- OAuth2 (Google, Apple)
- Biometric auth (TouchID, FaceID)
- Admin dashboard for user management
- User profile page
- MFA via SMS/email
- Consent and audit logs
- Sign-in with magic link

---

## 10. Project Milestones

| Milestone | Target Date |
|-----------|-------------|
| Setup Cognito user pool & app clients | Week 1 |
| Backend Lambda functions implemented | Week 2 |
| React auth flow integration | Week 3 |
| Testing and deployment | Week 4 |

---

## 11. Acceptance Criteria

- ✅ Users can sign up, receive email, and confirm
- ✅ Users can log in and receive tokens
- ✅ Users can reset passwords
- ✅ Auth state is tracked and respected in frontend
- ✅ All endpoints log errors and handle exceptions gracefully
- ✅ Deployed backend is live and reachable via gateway URL
- ✅ React app runs locally and in staging with full auth flow

---

## 12. Appendix

### JWT Token Example

```json
{
  "accessToken": "eyJraWQiOiJr...",
  "idToken": "...",
  "refreshToken": "..."
}
```

### Environment Variables

- `COGNITO_USER_POOL_ID`
- `COGNITO_APP_CLIENT_ID`
- `COGNITO_APP_CLIENT_SECRET` (if used)
- `REGION`
- `FRONTEND_URL`

---

**End of Document**
