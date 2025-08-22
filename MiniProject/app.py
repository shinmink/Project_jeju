from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_script():
    query = request.form['query']
    limit = request.form['limit']
    sort = request.form['sort']

    try:
        result = subprocess.run(
            ['python3', 'scripts/youtube_crawler_clean.py', query, limit, sort],
            capture_output=True,
            text=True,
            check=True  # 실패시 CalledProcessError 발생
        )
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = f"❌ 오류 발생:\n{e.stderr}"

    summary_lines = result.stdout.split('\n')
    message = summary_lines[0]
    preview = summary_lines[1:]  # 상위 5개 영상
    return render_template('index.html', message=message, preview=preview)

if __name__ == '__main__':
    app.run(debug=True)