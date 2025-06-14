from flask import Flask, request, jsonify
import os
from backend.parser import extract_text_from_file
from backend.matcher import compute_similarity

app = Flask(__name__)

@app.route('/match', methods=['POST'])
def match_resumes():
    job_desc = request.form['job_desc']
    files = request.files.getlist('resumes')
    
    os.makedirs('resumes', exist_ok=True)  # ✅ Ensure folder exists

    results = []

    for file in files:
        path = os.path.join('resumes', file.filename)
        file.save(path)
        resume_text = extract_text_from_file(path)
        result = compute_similarity(job_desc, resume_text)
        score = result["match_percent"]
        results.append({
    "filename": file.filename,
    "match_percent": score,
    "section_scores": result["section_scores"]
})

        
        os.remove(path)

    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render sets $PORT
    app.run(host='0.0.0.0', port=port, debug=False)

