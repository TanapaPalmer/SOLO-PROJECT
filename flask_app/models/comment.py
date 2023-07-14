from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.fact_id = data['fact_id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_comment(request):
        is_valid = True
        if len(request['comment']) < 1:
            flash('Cannot Be Blank')
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO comments (comment, user_id, fact_id) VALUES (%(comment)s, %(user_id)s, %(fact_id)s);"
        return connectToMySQL('did_you_know').query_db(query,data)
    
    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        result = connectToMySQL('did_you_know').query_db(query,data)
        return result