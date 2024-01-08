from sys import argv
from application import app
from waitress import serve

mode=argv[1]
#Run the app in development mode
if mode == 'development':
    if __name__=="__main__":
        app.run(host="127.0.0.1",port=5000,debug=True)
#Run the app in production mode
if mode == 'production':
    serve(app,host="127.0.0.1",port=5000)