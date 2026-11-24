
from getpass import getpass

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Create one account for each role so we can test permissions.
    for username, role in [("admin", "admin"), ("analyst", "analyst")]:
        if User.query.filter_by(username=username).first():
            print(f"{username} already exists.")
            continue

        password = getpass(f"Enter a password for {username}: ")

        # Use a strong password for each test account.
        if len(password) < 12:
            print("Password must be at least 12 characters.")
            continue

        user = User(
            username=username,
            email=f"{username}@example.test",
            role=role
        )

        # Store a hash rather than the password itself.
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        print(f"{role} account created successfully.")

