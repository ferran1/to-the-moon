from webfiles import create_app

app = create_app()

if __name__ == '__main__':
    app.run('192.168.178.241', port=5000, debug=True, threaded=False)
    # app.run('192.168.178.241', ssl_context=('cert.pem', 'key.pem'), port=5000, debug=True, threaded=False)

