from flask import Flask, render_template, request, url_for
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

# 워드클라우드
@app.route('/keyword_extractor', methods=['POST'])
def generate_wordcloud():
    try:
        result = subprocess.run(
            ['python3', 'scripts/keyword_extractor.py'],
            capture_output=True,
            text=True,
            check=True
        )
        image_path = url_for('static', filename='wordcloud.png')
        return render_template('index.html', image=image_path, message="✅ 워드클라우드 생성 완료!", show_modal=True)
    except subprocess.CalledProcessError as e:
        return render_template('index.html', message=f"❌ 워드클라우드 생성 오류:\n{e.stderr}")

# 스캐터 플롯
@app.route('/scatter_plot', methods=['POST'])
def generate_scatter():
    try:
        result = subprocess.run(
            ['python3', 'scripts/scatter_plot.py'],
            capture_output=True,
            text=True,
            check=True
        )
        image_path = url_for('static', filename='scatter.png')
        return render_template('index.html', image=image_path, message="✅ 스캐터 플롯 생성 완료!", show_modal=True)
    except subprocess.CalledProcessError as e:
        return render_template('index.html', message=f"❌ 스캐터 플롯 생성 오류:\n{e.stderr}")

if __name__ == '__main__':
    app.run(debug=True)