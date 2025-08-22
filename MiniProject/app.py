from flask import Flask, render_template, request, url_for, session
import subprocess

app = Flask(__name__)
app.secret_key = 'd04a0177ee3f235f95e354721bdabfdd'  # 세션 사용 위해 필요 (임시 키)

@app.route('/', methods=['GET'])
def index():
    preview = session.get('preview', [])
    return render_template('index.html', preview=preview)

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
            check=True
        )
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = f"❌ 오류 발생:\n{e.stderr}"

    summary_lines = result.stdout.split('\n')
    message = summary_lines[0]
    preview = summary_lines[1:]
    session['preview'] = preview  # 세션에 저장
    return render_template('index.html', message=message, preview=preview)

@app.route('/keyword_extractor', methods=['POST'])
def generate_wordcloud():
    try:
        subprocess.run(
            ['python3', 'scripts/keyword_extractor.py'],
            capture_output=True,
            text=True,
            check=True
        )
        image_path = url_for('static', filename='wordcloud.png')
        preview = session.get('preview', [])
        return render_template('index.html', image=image_path, message="✅ 워드클라우드 생성 완료!", show_modal=True, preview=preview)
    except subprocess.CalledProcessError as e:
        return render_template('index.html', message=f"❌ 워드클라우드 생성 오류:\n{e.stderr}")

@app.route('/scatter_plot', methods=['POST'])
def generate_scatter():
    try:
        subprocess.run(
            ['python3', 'scripts/scatter_plot.py'],
            capture_output=True,
            text=True,
            check=True
        )
        image_path = url_for('static', filename='scatter.png')
        preview = session.get('preview', [])
        return render_template('index.html', image=image_path, message="✅ 스캐터 플롯 생성 완료!", show_modal=True, preview=preview)
    except subprocess.CalledProcessError as e:
        return render_template('index.html', message=f"❌ 스캐터 플롯 생성 오류:\n{e.stderr}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)