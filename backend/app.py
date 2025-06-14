from flask import Flask, request, jsonify
import os
from utils import extract_text_from_file
from matcher import compute_similarity

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
    app.run(debug=True, port=8000)
