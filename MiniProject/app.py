import os
import re
from flask import Flask, render_template, request, url_for, session
import subprocess
import glob


app = Flask(__name__)
app.secret_key = 'd04a0177ee3f235f95e354721bdabfdd'  # 세션 사용 위해 필요 (임시 키)

@app.route('/', methods=['GET'])
def index():
    preview = session.get('preview', [])
    return render_template('index.html', preview=preview)

@app.route('/run', methods=['POST'])
def run_script():
    global result
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

    # ✅ 상대 경로로 csv_path 파싱 (대괄호 내부만 추출)
    for line in summary_lines:
        print(f"[디버그] summary line: {line}")
        match = re.search(r"\[(hotplaces/.*?\.csv)\]", line)  # ✅ 대괄호 안만 추출
        if match:
            relative_path = match.group(1)
            print(f"[디버그] 상대 경로 추출됨: {relative_path}")
            session['csv_path'] = relative_path
            break

    return render_template('index.html', message=message, preview=preview)
@app.route('/keyword_extractor', methods=['POST'])
def generate_wordcloud():
    csv_path = session.get('csv_path')
    if not csv_path:
        return render_template('index.html', message="❌ 먼저 데이터를 수집해주세요.")

    try:
        subprocess.run(
            ['python3', 'scripts/keyword_extractor.py', csv_path],
            capture_output=True,
            text=True,
            check=True
        )
        latest_image = max(glob.glob("wordcloud/wordcloud_*.png"), key=os.path.getmtime)
        image_path = '/' + latest_image.replace("\\", "/")
        return render_template('index.html', image=image_path, message="✅ 워드클라우드 생성 완료!", show_modal=True,
                               preview=session.get('preview', []))
    except subprocess.CalledProcessError as e:
        return render_template('index.html', message=f"❌ 워드클라우드 생성 오류:\n{e.stderr}")
@app.route('/scatter_plot', methods=['POST'])
def generate_scatter():
    csv_path = session.get('csv_path')
    if not csv_path:
        return render_template('index.html', message="❌ 먼저 데이터를 수집해주세요.")

    try:
        subprocess.run(
            ['python3', 'scripts/scatter_plot.py', csv_path],
            capture_output=True,
            text=True,
            check=True
        )
        latest_image = max(glob.glob("scatter/scatter_avgviews_*.png"), key=os.path.getmtime)
        image_path = '/' + latest_image.replace("\\", "/")
        return render_template('index.html', image=image_path, message="✅ 스캐터 플롯 생성 완료!", show_modal=True,
                               preview=session.get('preview', []))
    except subprocess.CalledProcessError as e:
        return render_template('index.html', message=f"❌ 스캐터 플롯 생성 오류:\n{e.stderr}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)