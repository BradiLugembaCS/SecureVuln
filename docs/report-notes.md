# SecureVuln — Development Notes

## Application Overview

SecureVuln is a web application designed to help security analysts manually record, track and manage vulnerabilities identified within an organisation.

The application will support vulnerability CRUD operations, authentication, role-based authorisation and security auditing.

## Technology Decisions

- **Python and Flask:** Selected because they provide a lightweight framework for developing the application's backend.
- **SQLite:** Selected because the application requires a relatively small local database and does not need a separate database server for demonstration.
- **SQLAlchemy:** Used to define database models and handle database operations without manually concatenating SQL queries.
- **HTML, CSS and JavaScript:** Used to build the application interface.

## Database Design

Three database tables are planned:

1. Users — stores account details, password hashes and assigned roles.
2. Vulnerabilities — stores manually submitted security findings and their status.
3. Audit Logs — records important user actions.

## Security Considerations

- Passwords will be stored using secure password hashing.
- Different user roles will have different permissions.
- Database operations will use SQLAlchemy to help prevent SQL injection.
- Form inputs will be validated on the server.
- Sensitive configuration and database files will not be committed to GitHub.

## Testing Evidence

Database creation and table verification will be documented with screenshots.

-----------------------------------------------------------------

### Authentication Implementation

- Implemented user authentication using Flask-Login.
- Used Werkzeug to hash passwords before storing them in SQLite.
- Protected the dashboard using `@login_required`.
- Implemented logout using POST requests with CSRF protection.
- Used generic error messages for incorrect login attempts.

### Authentication Testing

- Verify successful administrator login.
- Verify successful analyst login.
- Verify incorrect-password handling.
- Verify logout and unauthenticated access restrictions.
- Inspect database records to confirm passwords are hashed.

**Evidence:** Screenshots 02–06, with test outcomes recorded after execution.