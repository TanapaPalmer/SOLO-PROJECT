from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import fact, user, comment


# ---------------------------------------------------
# "Comment" CLASS

class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.fact_id = data['fact_id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.commenter = None

# ---------------------------------------------------
# VALIDATION

    @staticmethod
    def validate_comment(data):
        is_valid = True
        if len(data['comment']) < 3:
            flash("Comment must be at least 3 characters long","comment")
            is_valid = False
        return is_valid

# ---------------------------------------------------
# SAVE COMMENT AND (HIDDEN) FACT ID AND USER ID

    @classmethod
    def save_comment(cls, data):
        query = "INSERT INTO comments (comment, user_id, fact_id) VALUES (%(comment)s, %(user_id)s, %(fact_id)s);"
        return connectToMySQL('did_you_know').query_db(query,data)

# ---------------------------------------------------
# DELETE A COMMENT

    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        result = connectToMySQL('did_you_know').query_db(query,data)
        return result
