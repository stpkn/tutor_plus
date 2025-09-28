from flask import Flask, render_template, send_from_directory, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Главная страница с React приложением"""
    return render_template('index.html')

@app.route('/cabinet')
def cabinet():
    """Страница личного кабинета"""
    return render_template('cabinet.html')

@app.route('/App.js')
def serve_app_js():
    """Обслуживание App.js"""
    return send_file('App.js', mimetype='application/javascript')

@app.route('/index.js')
def serve_index_js():
    """Обслуживание index.js"""
    return send_file('index.js', mimetype='application/javascript')

@app.route('/styles.css')
def serve_css():
    """Обслуживание styles.css"""
    return send_file('styles.css', mimetype='text/css')

@app.route('/me.jpg')
def serve_photo():
    """Обслуживание фото"""
    return send_file('me.jpg', mimetype='image/jpeg')

@app.route('/Cabinet.js')
def serve_cabinet_js():
    """Обслуживание Cabinet.js"""
    return send_file('Cabinet.js', mimetype='application/javascript')

@app.route('/cabinet-index.js')
def serve_cabinet_index_js():
    """Обслуживание cabinet-index.js"""
    return send_file('cabinet-index.js', mimetype='application/javascript')

if __name__ == '__main__':
    print("🚀 Flask сервер запущен!")
    print("📱 Откройте: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
