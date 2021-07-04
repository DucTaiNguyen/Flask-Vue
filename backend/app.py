from warnings import resetwarnings
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime

# I used to have bug with the flask_marshmallow since the wrong Python interpre
# and used the old version.
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:" "@localhost/flask"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, title, body):
        self.title = title
        self.body = body


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "body", "date")


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)

###########################
# Hien tai van chua hieu ArticlesSchema va dump()
@app.route("/get", methods=["GET"])
def get_articles():
    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)
    print("ket qua cua results: ", results)
    print("ket qua cua jsonify(results): ", jsonify(results))
    return jsonify(results)


# <id> la tham so truyen vao
@app.route("/get/<id>/", methods=["GET"])
def post_details(id):
    article = Articles.query.get(id)
    print("ket qua cua article: ", article)
    print(
        "ket qua cua article_schema.jsonify(article): ", article_schema.jsonify(article)
    )

    return article_schema.jsonify(article)


@app.route("/add", methods=["POST"])
def add_article():
    title = request.json["title"]
    body = request.json["body"]

    # Create the Object of Class Articles
    articles = Articles(title, body)
    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)


@app.route("/update/<id>/", methods=["PUT"])
def update_article(id):
    # article = Articles.query.get(id)
    article = Articles.query.get(id)
    title = request.json["title"]
    body = request.json["body"]

    article.title = title
    article.body = body

    db.session.commit()
    return article_schema.jsonify(article)


@app.route("/delete/<id>/", methods=["DELETE"])
def update_delete(id):
    # article = Articles.query.get(id)
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return article_schema.jsonify(article)


if __name__ == "__main__":
    app.run(debug=True)
