from nums_api.database import db

class Email(db.Model):
    """Emails in the system."""

    __tablename__ = 'emails'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    @classmethod
    def subscribe(cls, email):
        """Add email to mailing list."""

        email = Email(
            email=email,
         )

        db.session.add(email)
        return email