from flask import Blueprint, request
from app.globals import auth, db, swag

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
    """
    posts = db.session.execute(db.select(Post)).scalars()
    return PostSchema(many=True).dump(posts)


@bp.route('', methods=['POST'])
@auth.login_required
@swag.validate('PostCreate')
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
        example: Bearer ...
      - name: body
        in: body
        required: true
        schema:
          id: PostCreate
          required:
            - title
            - body
          properties:
            title:
              type: string
              description: Post title
              minLength: 4
              maxLength: 128
            body:
              type: string
              description: Post contents
              minLength: 4
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
    title = request.json['title']
    body = request.json['body']
    post = Post(
        title=title,
        body=body,
        author_id=auth.current_user().id)
    db.session.add(post)
    db.session.commit()
    return PostSchema().dump(post)
