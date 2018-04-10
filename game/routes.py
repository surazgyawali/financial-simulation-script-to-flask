from game import app

@app.route('/')
@app.route('/index')
def index():
    return "Dry run test!!"