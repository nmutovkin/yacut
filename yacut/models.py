from datetime import datetime

from . import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self, root):
        return dict(
            url=self.original,
            short_link=f'{root}{self.short}',
        )

    def from_dict(self, data):
        self.original = data['url']
        self.short = data['custom_id']
