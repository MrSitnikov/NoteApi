from api import app, request, multi_auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema
from utility.helpers import get_object_or_404


@app.route("/users/<int:user_id>")
def get_user_by_id(user_id):
    user = get_object_or_404(UserModel, user_id)
    if user is None:
        return {"error": "User not found"}, 404
    return user_schema.dump(user), 200


@app.route("/users")
def get_users():
    users = UserModel.query.all()
    return users_schema.dump(users), 200


@app.route("/users", methods=["POST"])
def create_user():
    user_data = request.json
    user = UserModel(**user_data)
    # DONE: добавить обработчик на создание пользователя с неуникальным username
    if UserModel.query.filter_by(username = user.username).first():
        return {"error": "User alredy exists"}, 409
    user.save()
    return user_schema.dump(user), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
@multi_auth.login_required(role="admin")
def edit_user(user_id):
    user_data = request.json
    user = get_object_or_404(UserModel, user_id)
    user.username = user_data["username"]
    user.save()
    return user_schema.dump(user), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
@multi_auth.login_required(role="admin")
def delete_user(user_id):
    #user = UserModel.query.get(user_id)
    user = get_object_or_404(UserModel, user_id)
    user.delete()
    """
    Пользователь может удалять ТОЛЬКО свои заметки
    """
    return {'message': f'User witho id={user_id} has delete'}, 200
    #raise NotImplemented("Метод не реализован")