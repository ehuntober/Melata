
from flask import Blueprint , render_template , url_for , redirect , request
from flask_login import login_required , current_user 
from models import Guestlink, Userlink
from app import db

main = Blueprint('main',__name__)

@main.route('/<short_url>')
def redirect_to_url(short_url):
    link = Guestlink.query.filter_by(short_url=short_url).first_or_404()
    return redirect(link.original_url)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/add_link', methods=['GET','POST'])
def add_link():
    original_url = request.form['original_url']
    link = Guestlink(original_url = original_url,shortened="")
    db.session.add(link)
    db.session.commit()
    return render_template('guesspage.html', original_url = link.original_url , new_link=link.short_url )




@main.route('/<short_url_user>')
def redirect_to_url2(short_url_user):
    link = Userlink.query.filter_by(short_url=short_url_user).first_or_404()
    return redirect(link.original_url)
        
@main.route('/add_link2', methods=['GET','POST'])
def add_link2():
    original_url = request.form['original_url']
    userlink = Userlink(original_url = original_url,shortened="", user_id=current_user.id)
    db.session.add(userlink)
    db.session.commit()
    return render_template('dashboard.html', original_url = userlink.original_url , new_link = userlink.short_url, name = current_user.name)



@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html' , name = current_user.name)


@main.errorhandler(404)
def page_not_found(e):
    return ' <h1> Page not found (404) </h1>' , 404