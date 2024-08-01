from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

def generate_safe_script(level, format):
    content = ""
    if format == '.py':
        if level == 'basic':
            content = "print('This is a harmless basic Python script')"
        elif level == 'medium':
            content = "import os\nprint('This is a harmless medium risk Python script')"
        elif level == 'high':
            content = "import random\nprint('This is a high-risk Python script simulation')"
            content += "\nfor i in range(5):\n    print(f'Random number: {random.randint(1, 100)}')"

    elif format == '.bash':
        if level == 'basic':
            content = "#!/bin/bash\n# This is a harmless basic Bash script\necho 'This is a harmless basic Bash script'"
        elif level == 'medium':
            content = "#!/bin/bash\n# This is a harmless medium risk Bash script\necho 'This is a harmless medium risk Bash script'\n"
            content += "for i in {1..5}; do\n    echo 'Loop iteration: $i'\ndone"
        elif level == 'high':
            content = "#!/bin/bash\n# This is a high-risk Bash script simulation\necho 'This is a high-risk Bash script simulation'\n"
            content += "for i in {1..5}; do\n    echo 'Random number: $((RANDOM % 100))'\ndone"

    elif format == '.exe':
        if level == 'basic':
            content = "@echo off\nREM This is a harmless basic .exe script\necho This is a harmless basic .exe script"
        elif level == 'medium':
            content = "@echo off\nREM This is a harmless medium risk .exe script\necho This is a harmless medium risk .exe script\n"
            content += "for /L %%i in (1,1,5) do echo Loop iteration %%i"
        elif level == 'high':
            content = "@echo off\nREM This is a high-risk .exe script simulation\necho This is a high-risk .exe script simulation\n"
            content += "for /L %%i in (1,1,5) do echo Random number %%i"

    file_name = f"test_script_{level}{format}"
    with open(f"static/{file_name}", 'w') as file:
        file.write(content)
    return file_name, content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    level = request.form['level']
    format = request.form['format']
    file_name, content = generate_safe_script(level, format)
    return render_template('result.html', file_name=file_name, content=content)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(debug=True)
