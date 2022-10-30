from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # __name__ refer to the current module ,
print(__name__)
# ## configure the app
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///db.sqlite"
db=SQLAlchemy(app)  # you need to add the configuration
""" sqlAlchemy ---> support different databases """

# ## need a webserver
# # or
# # export FLASK_APP=app
# # then flask run

# ## define urls , views
def index():
    print(request)  # will use the request imported --> how can it reflect the different
    # requests ---> using context push
    return "<h1> Hello from flask Index </h1>"  # status code 200


# to define a url
@app.route("/")
def helloworld():
    # a
    print(request)
    return "<h1> Hello from flask  </h1>"


## method 2
app.add_url_rule("/index", view_func=index)


##############################
@app.route("/home/<name>/<track>/<int:id>")
def userhome(name, track, id):
    return f"<h1>Hello {name} {track} {id}</h1>"


# ####### response
# @app.route("/response")
# def response_test():
#     response = app.make_response("Sample response")
#     response.status_code=201
#     return response

# response 2

@app.route("/another-response")
def response_test():
    return "Another response", 203


# render template

@app.route("/homepage")
def template_homepage():
    return render_template("hello.html")


# ### send parameter to template


@app.route("/profile/<name>")
def profile(name):
    info = {
        "name": "Noha",
        "courses": ["python", "django", "flask"],
        "bio": "<a href=''> Bio </a>"
    }
    return render_template("profile.html", user_name=name, info=info)


# ###################################
@app.route("/template")
def template():
    name = 'Noha'
    return render_template("extended_template.html", name=name)


# ################## define error handler
@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


@app.route("/", endpoint="testroute")
def testroute():
    return "<h1> if you didn't add name to the route , " \
           "it takes the function name or pass the the endpoint </h1>"


@app.route("/Welcome/<user>", endpoint="welcomeuser")
def welcomeuser(user):
    return f"Welcome {user}"


"""
    add url root
    @app.add_url_rule('text', "endpoint", "function name")
"""
"""
    how to display urls in the system ?

    flask shell 
    app.url_map
    ---> flask defines the static file route 
    Map([<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,


"""

""" you can define the type of the method with your url"""

@app.route("/cutomPost", endpoint="custompost", methods=["POST"])
def customPost():
    return "Post function"

# @app.route('/')
# def staticfiles ():
#     pass

# #######################################################

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(64))
    email = db.Column(db.String(64), unique = True, nullable=True)
    accepted = db.Column(db.Boolean,default =False)

    """ IN flask shell --> import the db , then run db.create_all()
    
    pip install flask-shell-ipython
    db.session.add(s1, s2)
    db.session.commit()
    
    ## queries 
    Student.query.all()
    Student.query.filter_by(name='test')
    Student.query.filter(Student.name.like('n%')).all()
    
    Student.query.get_or_404(4) =---> 4 is the id 
    Student.query.get(id) =---> if not found will return none 
    no migration in flask 
    so ---< you need to do the migrations on your own
    ----> so you need to use the library 000> to be used ((Day02))
    """

@app.route("/db/Students", endpoint="db.students")
def get_all_students():
    students = Student.query.all()
    return render_template("students_index.html", students=students)

@app.route("/db/student/<int:student_id>",endpoint="db.student")
def get_student(student_id):
    # s = Student.query.get(student_id)
    s = Student.query.get_or_404(student_id)

    return render_template("student_info.html", student=s)

if __name__ == "__main__":
    # app.run()
    app.run(debug=True)  # enable debug mode
