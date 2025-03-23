from flask import Flask, request, render_template, redirect, url_for, flash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

UPLOAD_FOLDER = "uploads"
FLAG_PATH = "flag.txt"

with open(FLAG_PATH, "w") as f:
    f.write("practice{this_is_flag}")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            flash("File uploaded successfully!", "success")  # Добавляем flash-сообщение
            return redirect(url_for("upload_file"))  # Перенаправляем обратно на страницу загрузки
    return render_template("upload.html")

@app.route("/view", methods=["GET", "POST"])
def view_file():
    content = None
    if request.method == "POST":
        filename = request.form.get("filename")  # Получаем имя файла от пользователя

        # Формируем путь, разрешая переход на уровень выше
        filepath = os.path.abspath(os.path.join(UPLOAD_FOLDER, filename))

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()  # Читаем содержимое файла
        except Exception as e:
            content = f"Error: {e}"  # Выводим ошибку, если файл не найден или нельзя прочитать

    return render_template("view.html", content=content)


if __name__ == "__main__":
    app.run(debug=True)