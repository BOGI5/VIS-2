from app import app
from werkzeug.serving import make_ssl_devcert 
make_ssl_devcert('./ssl', host='localhost')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('./ssl.crt', './ssl.key'))