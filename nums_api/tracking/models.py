from nums_api.database import db

class Tracking(db.Model):
    """Information about request type and frequency."""

    __tablename__ = "tracking"

    req_item = db.Column(
        db.String(100),
        primary_key=True,
    )
    
    category = db.Column(
        db.String(10),
        primary_key=True,
    )
    
    num_reqs = db.Column(
        db.Integer,
        nullable=False,
    )
    
    @classmethod
    def update_request_count(cls, req_item, category):
        """Queries database and creates or updates table with item request total."""
        #if in DB, increment
        
        if Tracking.query.get((req_item, category)):
            ###increment num_reqs
        else:
            ###write to DB
        