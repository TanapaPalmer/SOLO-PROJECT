from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user ,comment
from flask_app.models.user import User
from flask import flash

# ---------------------------------------------------
# "Fact" CLASS

class Fact:
    def __init__(self, data):
        self.id = data['id']
        self.fact = data['fact']
        self.resource = data['resource']
        self.user_id = data['user_id']
        self.poster = None
        # self.commenter = None
        self.comments = []
        
# ---------------------------------------------------
# VALIDATION

    @staticmethod
    def validate_fact(data):
        is_valid = True

        if len(data['fact']) < 5:
            flash("Fact must be at least 5 characters long","details")
            is_valid = False
        if len(data['resource']) < 5:
            flash("Resource must be at least 5 characters long","details")
            is_valid = False
            
        return is_valid
    
# ---------------------------------------------------
# GET ALL FACTS

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

# ---------------------------------------------------
# GET ALL USERS, FACTS AND COMMENTS BY USER ID

    # @classmethod
    # def get_users_facts_comments_by_user_id(cls,data):
    #     query = "SELECT * FROM facts LEFT JOIN users ON facts.user_id = users.id LEFT JOIN comments ON facts.id = comments.fact_id WHERE facts.id = %(id)s;"
    #     results = connectToMySQL('did_you_know').query_db(query,data)
    #     one_fact = cls(results[0])
    #     user_data = {
    #             "id": results[0]['users.id'],
    #             "user_name": results[0]['user_name'],
    #             "email": "",
    #             "password": "",
    #             "created_at": results[0]['users.created_at'],
    #             "updated_at": results[0]['users.updated_at']
    #     }
    #     one_fact.poster = user.User(user_data)
    #     for row in results:
    #         comment_fact = {
    #             "id": row['comments.id'],
    #             "user_id": row['comments.user_id'],
    #             "fact_id": row['fact_id'],
    #             "comment": row['comment'],
    #             "created_at": row['comments.created_at'],
    #             "updated_at": row['comments.updated_at'],
    #             "commenter" : None
    #         }
    #         one_comment = comment.Comment(comment_fact)
    #         one_fact.comments.append(one_comment)
    #     return one_fact

    @classmethod
    def get_users_facts_comments_by_user_id(cls,data):
        query = "SELECT * FROM facts LEFT JOIN users ON facts.user_id = users.id LEFT JOIN comments ON facts.id = comments.fact_id WHERE facts.id = %(id)s;"
        results = connectToMySQL('did_you_know').query_db(query,data)
        one_fact = cls(results[0])
        user_data = {
                "id": results[0]['users.id'],
                "user_name": results[0]['user_name'],
                "email": "",
                "password": "",
                "created_at": results[0]['users.created_at'],
                "updated_at": results[0]['users.updated_at']
        }
        one_fact.poster = user.User(user_data)

        print('fact', results)

        for row in results:
            if row['comments.id'] is None:
                continue

            commenter_id = row['comments.user_id']
               
            comment_fact = {
                "id": row['comments.id'],
                "user_id": commenter_id,
                "fact_id": row['fact_id'],
                "comment": row['comment'],
                "created_at": row['comments.created_at'],
                "updated_at": row['comments.updated_at'],
                "commenter" : None
            }
            query2 = "SELECT * FROM users WHERE users.id = {};".format(commenter_id)
            results = connectToMySQL('did_you_know').query_db(query2,data)
            print(results)

            commenter_data = {
                "id": results[0]['id'],
                "user_name": results[0]['user_name'],
                "email": "",
                "password": "",
                "created_at": results[0]['created_at'],
                "updated_at": results[0]['updated_at']
            }
            one_comment = comment.Comment(comment_fact)
            one_comment.commenter = user.User(commenter_data)
            one_fact.comments.append(one_comment)
            

        return one_fact

# ---------------------------------------------------
# GET FACT BY ID

    @classmethod
    def get_fact_by_id(cls, data):
        query = "SELECT * FROM facts WHERE id = %(id)s;"
        result = connectToMySQL('did_you_know').query_db(query,data)
        if result:
            fact = cls(result[0])
            return fact
        else:
            return False

# ---------------------------------------------------
# SAVE FACT AND RESOURCE

    @classmethod
    def save(cls, data):
        query = "INSERT INTO facts (fact,resource,user_id) VALUES (%(fact)s,%(resource)s,%(user_id)s);"
        return connectToMySQL('did_you_know').query_db(query,data)

# ---------------------------------------------------
# UPDATE FACT

    @classmethod
    def update(cls,data):
        query = "UPDATE facts SET fact = %(fact)s, resource = %(resource)s WHERE id = %(id)s;"
        result = connectToMySQL('did_you_know').query_db(query,data)
        return result

# ---------------------------------------------------
# DELETE A FACT

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM facts WHERE id = %(id)s;"
        result = connectToMySQL('did_you_know').query_db(query,data)
        return result

