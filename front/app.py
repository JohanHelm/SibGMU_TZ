from flask import Flask, render_template, request, redirect
import asyncio


app = Flask(__name__)


async def send_to_back(command: str) -> str:
    HOST = 'backend'
    PORT = 57360
    BUFSIZ = 1024
    reader, writer = await asyncio.open_connection(HOST, PORT)
    writer.write(command.encode('utf-8'))
    data = await reader.read(BUFSIZ)
    return data.decode('utf-8').replace("&", ", ")


@app.route('/')
def index():
    command = "SELECT&all"
    db_data = asyncio.run(send_to_back(command))
    return render_template('index.html', names=db_data)
    # return render_template('index.html', names='hello')


@app.route('/get_data', methods=['POST'])
def get_data():
    name = request.form['name']
    command = f"SELECT&{name}"
    db_data = asyncio.run(send_to_back(command))
    return f"Данные для {name} из базы данных...{db_data}"


@app.route('/add_person', methods=['POST'])
def add_person():
    name = request.form['name']
    height = request.form['height']
    weight = request.form['weight']
    age = request.form['age']
    command = f"INSERT&{name}&{height}&{weight}&{age}"
    db_data = asyncio.run(send_to_back(command))
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
