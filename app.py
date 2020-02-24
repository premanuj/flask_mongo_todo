from flask import Flask, render_template, url_for, jsonify, request, redirect
from manage import db, MongoEngineSessionInterface


app = Flask("__main__", template_folder="templates")
app.config["MONGODB_DB"] = "admin"
app.config["MONGODB_HOST"] = "localhost"
app.config["MONGODB_PORT"] = 27017
# app.config["MONGODB_USERNAME"] = "webapp"
# app.config["MONGODB_PASSWORD"] = "pwd123"

db.init_app(app)
app.session_interface = MongoEngineSessionInterface(db)


@app.route("/", methods=("GET", "POST",))
def index():
    if request.method == "POST":
        name = request.form["item"]
        item = Item(name=name).save()
    items = Item.objects
    return render_template("index.html", items=items)


@app.route("/delete/<item_id>", methods=("DELETE",))
def remove(item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    items = Item.objects()
    print(items)
    return jsonify([item.serialize() for item in items])


@app.route("/update/<item_id>", methods=("GET", "POST",))
def update(item_id):
    item = Item.objects.get(id=item_id)
    print(item.name)
    if request.method == "POST":
        data = request.form
        item.name = data.get("item", item.name)
        item.save()
        return redirect(url_for("index"))
    print("here")
    return render_template("edit.html", item=item)


class Item(db.Document):
    name = db.StringField(required=True, unique=True)

    def __repr__(self):
        return "<Item %r>" % self.name

    def serialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
        }


if __name__ == "__main__":
    app.run()
