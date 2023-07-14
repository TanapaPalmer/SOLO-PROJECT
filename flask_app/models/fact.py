from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import fact
from flask_app.models import comment
from flask_app.models.user import User
from flask import flash

class Fact:
    def __init__(self, data):
        self.id = data['id']
        self.fact = data['fact']
        self.resource = data['resource']
        self.user_id = data['user_id']
        # self.fact_id = data['fact_id']
        self.poster = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM facts JOIN users ON facts.user_id = users.id;"
        results = connectToMySQL('did_you_know').query_db(query)
        facts = []
        for row in results:
            one_fact = cls(row)
            user_data = {
                "id": row['users.id'],
                "user_name": row['user_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            one_fact.poster = user.User(user_data)
            facts.append(one_fact)
        return facts
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM facts JOIN users ON facts.user_id = users.id WHERE facts.id = %(id)s;"
        result = connectToMySQL('did_you_know').query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_fact = cls(result)
        data = {
                "id": result['users.id'],
                "user_name": result['user_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at'],
        }
        this_fact.poster = user.User(data)
        return this_fact

    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM facts JOIN users ON comments.user_id = users.id;"
    #     results = connectToMySQL('did_you_know').query_db(query)
    #     facts = []
    #     for row in results:
    #         one_fact = cls(row)
    #         user_data = {
    #             "id": row['users.id'],
    #             "user_name": row['user_name'],
    #             "email": row['email'],
    #             "password": "",
    #             "created_at": row['users.created_at'],
    #             "updated_at": row['users.updated_at']
    #         }
    #         one_fact.poster = user.User(user_data)
    #         facts.append(one_fact)
    #     return facts
    
    # @classmethod
    # def get_by_id(cls,data):
    #     query = "SELECT * FROM facts JOIN users ON facts.user_id = users.id LEFT JOIN comments.fact.id WHERE facts.id = %(id)s;"
    #     result = connectToMySQL('did_you_know').query_db(query,data)
    #     one_fact = cls(result[0])
    #     data = {
    #             "id": result['users.id'],
    #             "user_name": result['user_name'],
    #             "email": result['email'],
    #             "password": "",
    #             "created_at": result['users.created_at'],
    #             "updated_at": result['users.updated_at']
    #     }
    #     one_fact.poster = user.User(data)
    #     for row in results:
    #         comment_fact = {
    #             "id": row['users.id'],
    #             "user_id": row['comments.user_id'],
    #             "fact_id": row['fact_id'],
    #             "comment": row['comments.comment'],
    #             "created_at": row['comments.created_at'],
    #             "updated_at": row['comments.updated_at']
    #         }
    #         one_comment = comment.Comment(comment_fact)
    #         one_fact.commends.append(one_comment)
    #     return one_fact


    @classmethod
    def save(cls, data):
        query = "INSERT INTO facts (fact,resource,user_id) VALUES (%(fact)s,%(resource)s,%(user_id)s);"
        return connectToMySQL('did_you_know').query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE facts SET fact = %(fact)s, resource = %(resource)s WHERE id = %(id)s;"
        result = connectToMySQL('did_you_know').query_db(query,data)
        return result

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM facts WHERE id = %(id)s;"
        result = connectToMySQL('did_you_know').query_db(query,data)
        return result
        
    @staticmethod
    def validate_fact(data):
        is_valid = True

        if len(data['fact']) < 5:
            flash("Fact must be at least 5 characters long.","details")
            is_valid = False
        if len(data['resource']) < 5:
            flash("Resource must be at least 5 characters long.","details")
            is_valid = False
            
        return is_valid