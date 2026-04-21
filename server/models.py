from server.extensions import db, bcrypt


# User model for authentication and ownership

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # Must be unique for login identification
    username = db.Column(db.String(80), unique=True, nullable=False)

    # NEVER store plain passwords
    password_hash = db.Column(db.String(255), nullable=False)

    # Relationship: One user → many expenses
    expenses = db.relationship(
        "Expense",
        backref="user",
        cascade="all, delete",
        lazy=True
    )


    # Password hashing

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)



# Expense model for tracking user expenses

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)

    # Core fields
    title = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    # Extra fields
    category = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String(255), nullable=True)

    # Optional date tracking
    date = db.Column(db.String(50), nullable=True)

    # Foreign key → ensures ownership
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Helper method to convert model instance to dictionary (for JSON responses)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
            "user_id": self.user_id
        }