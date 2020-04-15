"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db
from flask import render_template, request, jsonify, redirect, url_for, flash, session, abort
from werkzeug.utils import secure_filename
from .models import UserProfile
from .forms import ProfileForm
import time

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

################################################################

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Shequan Ricketts")

####################################################################

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """new profile"""
    form = ProfileForm()
    if form.validate_on_submit(): 
        if request.method == 'POST':
            tcreated = str(time.strftime('%Y/%b/%d'))
            fname = request.form['first_name']
            lname = request.form['last_name']
            email = request.form['email']
            location = request.form['location']
            sex = request.form['gender']
            biography =request.form['bio']

            profilepic = request.files['image']
            if profilepic:
                uploadfolder = app.config['UPLOAD_FOLDER']
                filename = secure_filename(profilepic.filename)
                profilepic.save(os.path.join(uploadfolder, filename))
                
            user = UserProfile( first_name=fname, last_name=lname, email= email, location=location, gender=sex, bio=biography, created=tcreated, pic=filename)
            db.session.add(user)
            db.session.commit()
            flash('New user added successfully')
            return redirect(url_for('profiles'))
    return render_template('Profile.html', form=form)

#######################################################################

@app.route('/profiles', methods=['GET','POST'])
def profiles():
    """view profiles"""
    profile_list=[]
    
    profiles= UserProfile.query.filter_by().all()
    
    if request.method == 'POST':
        for profile in profiles:
            profile_list +=[{'username':profile.username, 'userID':profile.uid}]
        return jsonify(users=profile_list)
    elif request.method == 'GET':
        return render_template('profiles.html', profile=profiles)
    return redirect(url_for('home'))

##############################################################################
    
@app.route('/profile/<userid>', methods=['GET'])
def userprofile(userid):
    """view individual profile"""
    user = UserProfile.query.filter_by(id=userid).first()

    if request.method == 'GET' and user:
        return render_template('indiprofile.html', profile=user)

    return render_template('profile.html')


########################################################################################


###
# The functions below should be applicable to all Flask apps.
###


# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
