from app import db


class ProductlineModel(db.Model):
    __tablename__ = 'productlines'
    productLine = db.Column(db.VARCHAR(50), primary_key=True, nullable=False)
    textDescription = db.Column(db.VARCHAR(4000), nullable=True)
    htmlDescription = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text, nullable=True)

    product = db.relationship('ProductModel', backref='productlines', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self,
             productLine,
             textDescription,
             htmlDescription,
             image,
             ):
        self.productLine = productLine
        self.textDescription = textDescription
        self.htmlDescription = htmlDescription
        self.image = image

    def json(self):
        return {
            "productLine": self.productLine,
            "textDescription": self.textDescription,
            "htmlDescription": str(self.htmlDescription),
            "image": str(self.image),
        }

    @classmethod
    def find_by_productLine(cls, productLine):
        return cls.query.filter_by(
            productLine=productLine
        ).first()

    def save_to_db(self):

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):

        db.session.delete(self)
        db.session.commit()
