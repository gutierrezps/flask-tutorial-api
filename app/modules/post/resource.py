from flask import Blueprint
from app.globals import auth

from .model import Post, PostSchema


bp = Blueprint('posts', __name__, url_prefix='/posts')


@bp.route('', methods=['GET'])
def posts():
    """Get the list of posts
    ---
    tags:
      - Posts
    responses:
      200:
        description: List of posts
        schema:
          type: array
          items:
            type: object
            properties:
              title:
                type: string
              body:
                type: string
              author:
                type: string
              created_at:
                type: string
    """
    posts = Post.all()
    return PostSchema(many=True).dump(posts)


@bp.route('', methods=['POST'])
@auth.login_required
def new_post():
    """Create a new post
    ---
    tags:
      - Posts
    security:
      type: apiKey
      name: Authorization
      in: header
    parameters:
      - name: Authorization
        in: header
        required: true
      - name: title
        in: body
        required: true
    responses:
      201:
        description: Post created
        schema:
          type: object
          properties:
            id:
              type: number
            title:
              type: string
            body:
              type: string
            author:
              type: string
            created_at:
              type: string
      401:
        description: User not logged in
    """
    return auth.current_user()
