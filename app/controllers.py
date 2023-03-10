from flask import Blueprint, render_template, request, flash
from flask.helpers import url_for

from .models import Shows

controllers = Blueprint('controllers', __name__)

movies = [
    {
        "show_id": "kgf2021",
        "poster": "kgf2.jpg",
        "title": "kgf-2",
        "tags": ["action", "drama", "crime"],
        "description": "In the blood-soaked Kolar Gold Fields, Rocky's name strikes fear into his foes. While his allies look up to him, the government sees him as a threat to law and order. Rocky must battle threats from all sides for unchallenged supremacy."
    },
    {
        "show_id": "pat2023",
        "poster": "pathaan.jpg",
        "title": "Pathaan",
        "tags": ["action", "drama", "crime"],
        "description": "An Indian spy takes on the leader of a group of mercenaries who have nefarious plans to target his homeland."
    },
    {
        "show_id": "pushpa2022",
        "poster": "pushpa.jpg",
        "title": "Pushpa",
        "tags": ["action", "drama", "crime"],
        "description": "A labourer rises through the ranks of a Red sandal smuggling syndicate, making some powerful enemies in the process."
    },
    {
        "show_id": "quantumania2023",
        "poster": "Quantumania.jpg",
        "title": "Quantumania",
        "tags": ["action", "drama", "crime"],
        "description": "Scott Lang and Hope Van Dyne, along with Hank Pym and Janet Van Dyne, explore the Quantum Realm, where they interact with strange creatures and embark on an adventure that goes beyond the limits of what they thought was possible."
    },
    {
        "show_id": "rrr2022",
        "poster": "rrr.jpg",
        "title": "RRR",
        "tags": ["action", "drama", "crime"],
        "description": "A fictitious story about two legendary revolutionaries and their journey away from home before they started fighting for their country in the 1920s."
    },
    {
        "show_id": "wf2023",
        "poster": "https://m.media-amazon.com/images/M/MV5BNTM4NjIxNmEtYWE5NS00NDczLTkyNWQtYThhNmQyZGQzMjM0XkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_FMjpg_UX1000_.jpg",
        "title": "Wakanda Forever",
        "tags": ["action", "drama", "crime"],
        "description": "The people of Wakanda fight to protect their home from intervening world powers as they mourn the death of King T'Challa."
    }
]

@controllers.route('/')
def index():
    return render_template('index.html.jinja2', SHOWS=movies)


@controllers.route("/book_tickets/<show_id>")
def book_tickets(show_id):
    return render_template("bookshow.html.jinja2", SHOWS=movies, show_id=show_id)