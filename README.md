# Secure Authentication System with Flask 🔐

🔐 A beginner-friendly Flask web app demonstrating secure login and registration with CSRF protection, session handling, and key HTTP security headers. Built to practice secure authentication workflows.

## 🚀 Features

- User Registration & Login
- Secure password hashing
- Session-based authentication
- CSRF protection using Flask-WTF
- Route protection (dashboard access only after login)
- Logout functionality
- Security headers via Flask-Talisman

## 🛠️ Tech Stack

- Python 3.9
- Flask
- Flask-WTF
- Flask-Talisman
- HTML/CSS (Jinja templates)

## 🔐 Security Best Practices Implemented

- CSRF tokens on all forms
- Session cookies configured (`HttpOnly`, `Secure`, `SameSite`)
- Route access control (`@login_required` style logic)
- Security headers (XSS, CSP, X-Frame options)

## 💻 Running Locally
