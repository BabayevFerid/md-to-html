# app.py
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret-key') # production üçün dəyişdir




@app.route('/', methods=['GET', 'POST'])
def index():
"""Show form to paste/upload Markdown or convert on submit."""
if request.method == 'POST':
# two ways to get markdown: text area or uploaded file
md_text = ''
if 'md_file' in request.files and request.files['md_file'].filename:
uploaded = request.files['md_file']
try:
md_text = uploaded.read().decode('utf-8')
except Exception:
flash('Fayl oxunarkən xəta oldu. UTF-8 encoded fayl olduğundan əmin ol.')
return redirect(url_for('index'))
else:
md_text = request.form.get('markdown_text', '')


if not md_text.strip():
flash('Zəhmət olmasa Markdown mətnini yapışdırın və ya fayl yükləyin.')
return redirect(url_for('index'))


# convert
html_body = md_to_html(md_text)
# optionally wrap into a full HTML page in the template
return render_template('result.html', html_body=html_body, raw_md=md_text)


return render_template('index.html')




@app.route('/download', methods=['POST'])
def download():
"""Return converted HTML as a downloadable .html file."""
md_text = request.form.get('raw_md', '')
if not md_text:
flash('Heç bir Markdown mətn tapılmadı.')
return redirect(url_for('index'))


html_body = md_to_html(md_text)


# minimal full HTML document
full_html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Converted Markdown</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css">
<style>
body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; padding: 2rem; }}
pre code {{ white-space: pre; display:block; padding:1rem; border-radius:6px; background:#f5f5f5; overflow:auto; }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""


# return as attachment
return Response(
full_html,
mimetype='text/html',
headers={'Content-Disposition': 'attachment;filename=converted.html'}
)




if __name__ == '__main__':
app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
