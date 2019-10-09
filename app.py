from flask import Flask,render_template
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

# 全文处理，包括错误处理和预处理等

# @app.before_first_request
# def create_tables():
#     db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    # 页面未找到
    return render_template('errorpage/404.html'), 404

# 连接地址
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/elements')
def elements():
    return render_template('elements.html')

@app.route('/generic')
def generic():
    return render_template('generic.html')

if __name__ == '__main__':
    # db.init_app(app)
    app.run(port=5000, debug=True)