from app.database import SessionLocal
from app.models import User
from app.services.auth_service import hash_password

db = SessionLocal()

# Check if admin exists
admin = db.query(User).filter(User.email == "admin@gmail.com").first()

if not admin:
    admin = User(
        email="admin@gmail.com",
        hashed_password=hash_password("admin123"),
        is_admin=True,
        phone_number="0700000000"
    )
    db.add(admin)
    db.commit()
    print("✅ Admin user created: admin@gmail.com / admin123")
else:
    print("✅ Admin user already exists")

db.close()
