from server.app import app
from server.extensions import db
from server.models import User, Expense
from faker import Faker
import random

fake = Faker()


def seed_data():
    with app.app_context():

        # Reset database (DANGER: THIS WILL DELETE ALL DATA)

        db.drop_all()
        db.create_all()

        print("Database reset complete.")

        # Create test users

        user1 = User(username="demo_user")
        user1.set_password("password123")

        user2 = User(username="test_user")
        user2.set_password("password123")

        db.session.add_all([user1, user2])
        db.session.commit()

        print("Test users created.")

        # Create expenses

        categories = ["Food", "Transport", "Utilities", "Entertainment", "Shopping"]

        expenses = []

        # Expenses for user1
        for _ in range(10):
            expense = Expense(
                title=fake.sentence(nb_words=3),
                amount=round(random.uniform(5, 500), 2),
                category=random.choice(categories),
                description=fake.text(max_nb_chars=50),
                date=str(fake.date_this_year()),
                user_id=user1.id
            )
            expenses.append(expense)

        # Expenses for user2
        for _ in range(10):
            expense = Expense(
                title=fake.sentence(nb_words=3),
                amount=round(random.uniform(5, 500), 2),
                category=random.choice(categories),
                description=fake.text(max_nb_chars=50),
                date=str(fake.date_this_year()),
                user_id=user2.id
            )
            expenses.append(expense)

        db.session.add_all(expenses)
        db.session.commit()

        print(f"{len(expenses)} fake expenses created for both users.")


if __name__ == "__main__":
    seed_data()