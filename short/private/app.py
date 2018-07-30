from flask import Flask, request, render_template, abort
from db import *
from random import choice
import string
import requests

app = Flask(__name__)
ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits
HEADERS = {
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
    "Accept": "text/html;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "close",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1"
}


def generate_slug(length):
    return "".join((choice(ALPHABET) for _ in range(5)))


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        link = request.form.get("link")
        if link is None:
            return render_template("main.html", error="Fill in the URL")

        if not link.startswith("http://") and not link.startswith("https://"):
            link = "http://" + link

        try:
            requests.head(link, headers=HEADERS, timeout=0.05)
        except:
            return render_template("main.html", error="Page does not exist")

        short_link = generate_slug(6)
        Link.create(
            id=short_link,
            url=link
        )

        return render_template("main.html", short_link=short_link)

    return render_template("main.html")


@app.route("/<slug>")
def follow(slug):
    try:
        link = Link.get(Link.id == slug)
    except Link.DoesNotExist:
        return render_template("unknown.html"), 404

    return render_template("preroll.html", page=link.url)


if __name__ == '__main__':
    app.run()
