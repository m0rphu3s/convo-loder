from flask import Flask, request, render_template_string, redirect, url_for, session
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.secret_key = "supersecretkey"  # session ke liye

# Login credentials
APP_USERNAME = "Lucifer"
APP_PASSWORD = "Lucifer_xd"

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

# Function: Messages send karna
def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Sent Failed From token {access_token}: {message}")
                time.sleep(time_interval)

# Route: Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == APP_USERNAME and password == APP_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('welcome'))
        else:
            return "❌ Invalid Username or Password!"
    return render_template_string(f'''
    <html>
    <head><title>❤️Muddassir 𝘙𝘶𝘭𝘦𝘹❤️ - Login</title></head>
    <body style="text-align:center; background:url('https://i.ibb.co/LRrPTkG/c278d531d734cc6fcf79165d664fdee3.jpg') no-repeat center center fixed; background-size:cover; color:white; font-family:sans-serif;">
    <h2>🔐 Login Required</h2>
    <form method="post">
        <input type="text" name="username" placeholder="Enter Username" required><br><br>
        <input type="password" name="password" placeholder="Enter Password" required><br><br>
        <button type="submit">Login</button>
    </form>
    <br>
    <p>📞 Contact Developer:
    <a href="https://wa.me/+923243037456" target="_blank">WhatsApp</a> |
    <a href="https://www.facebook.com/muddassir.OP" target="_blank">Facebook</a>
    </p>
    </body>
    </html>
    ''')

# Route: Welcome Animation Page
@app.route('/welcome')
def welcome():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template_string(f'''
    <html>
    <head>
    <title>❤️Muddassir 𝘙𝘶𝘭𝘦𝘹❤️ - Welcome</title>
    <style>
    body {{ background:url('https://i.ibb.co/LRrPTkG/c278d531d734cc6fcf79165d664fdee3.jpg') no-repeat center center fixed; background-size:cover; color:white; text-align:center; font-family:sans-serif; }}
    h1 {{ animation: glow 2s infinite alternate; }}
    @keyframes glow {{
        from {{ text-shadow: 0 0 10px red; }}
        to {{ text-shadow: 0 0 30px yellow; }}
    }}
    </style>
    </head>
    <body>
    <h1>✨ Welcome to my Tool ✨</h1>
    <h2>👑 Developer: Muddassir</h2>
    <p>📞 WhatsApp: <a href="https://wa.me/+923243037456" target="_blank">+923243037456</a></p>
    <p>🌐 Facebook: <a href="https://www.facebook.com/muddassir.OP" target="_blank">Muddassir.OP</a></p>
    <br><br>
    <a href="/">👉 Enter Tool</a>
    </body>
    </html>
    ''')

# Route: Main Tool Page
@app.route('/', methods=['GET', 'POST'])
def send_message():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':  
        token_option = request.form.get('tokenOption')  
        if token_option == 'single':  
            access_tokens = [request.form.get('singleToken')]  
        else:  
            token_file = request.files['tokenFile']  
            access_tokens = token_file.read().decode().strip().splitlines()  

        thread_id = request.form.get('threadId')  
        mn = request.form.get('kidx')  
        time_interval = int(request.form.get('time'))  

        txt_file = request.files['txtFile']  
        messages = txt_file.read().decode().splitlines()  

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  
        stop_events[task_id] = Event()  
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))  
        threads[task_id] = thread  
        thread.start()  

        return f'Task started with ID: {task_id}'  

    return render_template_string(f'''  
        <html>
        <head><title>❤️Muddassir 𝘙𝘶𝘭𝘦𝘹❤️ - Tool</title></head>
        <body style="text-align:center; background:url('https://i.ibb.co/LRrPTkG/c278d531d734cc6fcf79165d664fdee3.jpg') no-repeat center center fixed; background-size:cover; color:white; font-family:sans-serif;">
        ❤️MUDDASSIR INSID3W-❤️<br>  
        # ♛♥彡MUDDASSIR W3B-♛♥☨<br><br>  

        <form method="post" enctype="multipart/form-data">  
            <label>Select Token Option</label><br>  
            <input type="radio" name="tokenOption" value="single" required> Single Token  
            <input type="radio" name="tokenOption" value="file"> Token File <br><br>  

            <label>Enter Single Token</label><br>  
            <input type="text" name="singleToken"><br><br>  

            <label>Choose Token File</label><br>  
            <input type="file" name="tokenFile"><br><br>  

            <label>Enter Inbox/convo uid</label><br>  
            <input type="text" name="threadId" required><br><br>  

            <label>Enter Your Hater Name</label><br>  
            <input type="text" name="kidx" required><br><br>  

            <label>Enter Time (seconds)</label><br>  
            <input type="number" name="time" required><br><br>  

            <label>Choose Your Txt File</label><br>  
            <input type="file" name="txtFile" required><br><br>  

            <button type="submit">Run</button>  
        </form>  

        <form method="post" action="/stop">  
            <label>Enter Task ID to Stop</label><br>  
            <input type="text" name="taskId" required><br>  
            <button type="submit">Stop</button>  
        </form>  

        <br><br>  
        © 2023 ᴅᴇᴠʟᴏᴩᴇᴅ ʙʏ 🥀✌️MUDD9SSIR 😈🐧  
        <br>DR39M 𝐑𝐔𝐋𝐄X 𝐇𝐄𝐑𝐄  
        </body>
        </html>
    ''')

# Route: Stop Task
@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Task with ID {task_id} has been stopped.'
    else:
        return f'No task found with ID {task_id}.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
