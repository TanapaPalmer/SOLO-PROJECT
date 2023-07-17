from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import fact, user, comment


class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.fact_id = data['fact_id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.commenter = None
        # self.comments = []

    @staticmethod
    def validate_comment(data):
        is_valid = True
        if len(data['comment']) < 3:
            flash("Comment must be at least 3 characters long","comment")
            is_valid = False
        return is_valid
    
    @classmethod
    def save_comment(cls, data):
        query = "INSERT INTO comments (comment, user_id, fact_id) VALUES (%(comment)s, %(user_id)s, %(fact_id)s);"
        return connectToMySQL('did_you_know').query_db(query,data)
    
    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        result = connectToMySQL('did_you_know').query_db(query,data)
        return result

    # @classmethod
    # def get_comment_id(cls,id):
    #     query = "SELECT * FROM facts LEFT JOIN users ON facts.user_id = users.id LEFT JOIN comments ON comments.fact_id = facts.id WHERE facts.id = %(id)s;"
    #     results = connectToMySQL('did_you_know').query_db(query,{'id': id})
        
    #     if not results:
    #         return False
        
    #     results = results[0]
    #     this_comment = cls(results)
    #     data = {
    #             # "user_id": results['comments.user_id'],
    #             "fact_id": results['comments.fact_id'],
    #             "comment": results['comment'],
    #             "created_at": results['comments.created_at'],
    #             "updated_at": results['comments.updated_at']
    #     }
    #     this_comment.commenter = fact.Fact(data)
    #     return this_comment