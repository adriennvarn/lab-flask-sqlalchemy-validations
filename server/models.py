from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name required.")
        duplicate_name = db.session.query(Author.name).filter_by(name = name).first()
        if duplicate_name is not None:
            raise ValueError("Name must be unique.")
        return name
    
    @validates("phone_number")
    def validate_phone(self, key, number):
        if len(number) != 10:
            raise ValueError("Phone number must be 10 digits.")
        
        try:
            int(number)
        except:
            raise ValueError("Phone number must only contain digits.")
        
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("title")
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title is required.")
        if not isinstance(title, str):
            raise ValueError("Title must be valid string.")
        if not any(kw.lower() in title.lower() for kw in ["Won't Believe", "Secret", "Top", "Guess"]):
            raise ValueError("Title must contain secret keywords...")
        return title
    
    @validates("content")
    def validate_content(self, key, content):
        if not content:
            raise ValueError("Content is required.")
        if not isinstance(content, str):
            raise ValueError("Content must be a valid string.")
        if not len(content) >= 250:
            raise ValueError("Content must be at least 250 characters.")
        return content
    
    @validates("category")
    def validate_category(self, key, category):
        if not category:
            raise ValueError("Category is required.")
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be 'Fiction' or 'Non-Fiction' only.")
        return category
    
    @validates("summary")
    def validate_summary(self, key, summary):
        if not summary:
            raise ValueError("Summary is required.")
        if len(summary) > 250:
            raise ValueError("Summary must not be longer than 250 characters.")
        return summary


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
