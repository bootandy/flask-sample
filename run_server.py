from product import app
import os

if __name__ == '__main__':
    app.secret_key = '093284302121073532498' #os.urandom(24)
    app.debug = True

    if app.config['DEBUG']:
        from werkzeug import SharedDataMiddleware
        import os
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
          '/': os.path.join(os.path.dirname(__file__), 'static')
        })
    app.run()
