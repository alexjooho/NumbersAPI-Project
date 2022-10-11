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
        """Queries database and creates/updates table with item request total."""
        
        req_item = str(req_item)
        
        request = Tracking.query.get((req_item, category))
        
        if request:
            ###increment num_reqs
            request.num_reqs = Tracking.num_reqs + 1
            db.session.commit()
        else:
            ###write new entry to DB
            new_request_item = Tracking(
                req_item = req_item,
                category = category,
                num_reqs = 1
            )
            
            db.session.add(new_request_item)
            db.session.commit()
        