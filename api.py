from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class UserData(resource):
    def put(self, user_id):
        pass

    def get(self, user_id):
        pass

    def delete(self, user_id):
        pass


api.add_resource(UserData, '/user')
if __name__ == "__main__":
    app.run(debug=True)
