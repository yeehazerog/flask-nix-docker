from flask import Flask
from flask_wtf.csrf import CSRFProtect
#from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_lite import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Example model
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/stocks') 
def stocks(): 
    stocks = Stock.query.all() 
    return f"Current stocks: {stocks}"

@app.route('/verify_db') 
def verify_db(): 
    try: 
        # Check if the Stocks table exists; if not, create it 
        db.create_all() 
        
        # Perform a test query 
        result = Stock.query.first() 
        
        if result: 
            return jsonify(status="success", message="Database connection is working!", stock=result.symbol) 
        else:
            return jsonify(status="success", message="Database connection is working, but no stocks found.")
    except Exception as e:
        return jsonify(status="error", message=str(e))

def main():
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port="5000", debug=False)

if __name__ == '__main__':
    main()
