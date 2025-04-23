from functools import wraps
from flask import flash, redirect, url_for
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

def handle_sqlalchemy_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)  # Call the original function
        except IntegrityError as e:
            db.session.rollback()
            flash("A database constraint error occurred. Please check your input.", 'danger')
            return redirect(url_for("auth.register"))  # Or wherever you want to redirect

        except OperationalError as e:
            db.session.rollback()
            flash("Database connection issue. Please try again later.", 'danger')
            return redirect(url_for("auth.register"))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash("An error occurred while accessing the database.", 'danger')
            return redirect(url_for("auth.register"))

        except Exception as e:
            db.session.rollback()
            flash(f"Unexpected error: {str(e)}", 'danger')
            return redirect(url_for("auth.register"))

    return wrapper
