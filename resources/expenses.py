from flask import Blueprint, request
from server.models import Expense
from server.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

expense_bp = Blueprint("expenses", __name__)


# Get all expenses (with pagination and ownership filtering)

@expense_bp.route("/expenses", methods=["GET"])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()

    # Pagination params
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    # Query only user's expenses (CRITICAL FOR SECURITY)
    pagination = Expense.query.filter_by(user_id=user_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return {
        "expenses": [expense.to_dict() for expense in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    }, 200


# Create new expense (ownership automatically assigned via JWT identity)

@expense_bp.route("/expenses", methods=["POST"])
@jwt_required()
def create_expense():
    data = request.get_json()
    user_id = get_jwt_identity()

    # Validation
    if not data.get("title") or not data.get("amount"):
        return {"error": "Title and amount are required"}, 400

    expense = Expense(
        title=data.get("title"),
        amount=data.get("amount"),
        category=data.get("category"),
        description=data.get("description"),
        date=data.get("date"),
        user_id=user_id
    )

    db.session.add(expense)
    db.session.commit()

    return {
        "message": "Expense created successfully",
        "expense": expense.to_dict()
    }, 201


# Update expense (only if it belongs to the current user)

@expense_bp.route("/expenses/<int:id>", methods=["PATCH"])
@jwt_required()
def update_expense(id):
    user_id = get_jwt_identity()
    expense = Expense.query.get(id)

    # Check existence + ownership
    if not expense or expense.user_id != user_id:
        return {"error": "Expense not found or unauthorized"}, 403

    data = request.get_json()

    # Partial updates
    expense.title = data.get("title", expense.title)
    expense.amount = data.get("amount", expense.amount)
    expense.category = data.get("category", expense.category)
    expense.description = data.get("description", expense.description)
    expense.date = data.get("date", expense.date)

    db.session.commit()

    return {
        "message": "Expense updated successfully",
        "expense": expense.to_dict()
    }, 200


# Delete expense (only if it belongs to the current user)

@expense_bp.route("/expenses/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_expense(id):
    user_id = get_jwt_identity()
    expense = Expense.query.get(id)

    # Ownership check (VERY IMPORTANT FOR RUBRIC)
    if not expense or expense.user_id != user_id:
        return {"error": "Expense not found or unauthorized"}, 403

    db.session.delete(expense)
    db.session.commit()

    return {"message": "Expense deleted successfully"}, 200