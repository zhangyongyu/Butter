from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *
import json

from models.topic import Topic
from models.board import Board

main = Blueprint('topic', __name__)


@main.route("/")
def index():
    board_id = request.args.get('board_id', 'all')
    if board_id == 'all':
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)

    # if r.exists(board_id):
    #     log('hit redis')
    #     json_string = r.get(board_id)
    #     json_list = json.loads(json_string)
    # else:
    #     print('not hit redis')
    #     json_list = []
    #     for m in ms:
    #         j = m.json()
    #         j['replies'] = m.replies()
    #         j['user_image'] = m.user().user_image
    #         json_list.append(j)
    #     json_string = json.dumps(json_list)
    #     r.set(board_id, json_string)
    # ms = json_list

    token = new_csrf_token()
    bs = Board.all()
    return render_template("topic/index.html", ms=ms, token=token, bs=bs, bid=board_id)


@main.route('/<string:id>')
def detail(id):
    m = Topic.one(id=id)
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m)


@main.route("/add", methods=["POST"])
# @login_required
@csrf_required
def add():
    form = request.form
    u = current_user()
    Topic.new(form, user_id=u.id)
    return redirect(url_for('.index'))


@main.route("/delete")
@csrf_required
def delete():
    id = request.args.get('id')
    u = current_user()
    print('删除 topic 用户是', u, id)
    Topic.delete(id)
    return redirect(url_for('.index'))


@main.route("/new")
def new():
    board_id = request.args.get('board_id')
    token = new_csrf_token()
    bs = Board.all()
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id)
