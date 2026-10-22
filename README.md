# FreshTrace UI Prototype

A responsive, interactive frontend prototype for the FreshTrace Smart Supermarket Management System.

## Run
- Extract the ZIP.
- Open `index.html` in a modern browser, or run a local static server:
  - `python -m http.server 8000`
  - Open `http://localhost:8000`

## Included interactions
- Dashboard sales filters and charts
- Sidebar navigation
- Product creation with image file selection and camera capture fallback
- Product search, edit, and stock adjustment
- Product-name POS search and cart
- Cash confirmation flow, session-level stock deduction, receipt preview and browser printing
- Purchase entry, expiry alert views, purchase suggestions, CSV export
- Rule-based demo assistant and expense entry

## Important limitation
This is a **frontend prototype**, not the production Flask/MySQL application. Demo records are stored in browser memory and reset on refresh. Do not use it for real supermarket transactions. The next step is to connect all modules to the Flask backend and MySQL database, implement server-side transactions, scheduled expiry notifications, authentication/authorization, and tested reporting.
