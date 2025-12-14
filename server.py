from flask import Flask, Response, request
import json
from pathlib import Path


app = Flask(__name__)

@app.get('/all_transcripts')
def all_transcripts():
    folder = Path('/home/destreza/Documents/1515/myproject/data')
    data_files = folder.glob('*.json')
    student_transcripts = []
    
    for file in data_files:
        with file.open() as f:
            data = json.load(f)
            student_transcripts.append(data)

    length = len(student_transcripts)
    
    for i in range(length):
        print(i)
        for j in range(0, length - i - 1):
            print(j)
            if student_transcripts[j]["transcript_id"] > student_transcripts[j + 1]["transcript_id"]:
                temp = student_transcripts[j]
                student_transcripts[j] = student_transcripts[j + 1]
                student_transcripts[j + 1] = temp
            

    return student_transcripts

# Get by ID
@app.get('/transcript/<id>')
def transcript(id):
    folder = Path('/home/destreza/Documents/1515/myproject/data')
    data_files = folder.glob('*.json')
    
    for file in data_files:
        with file.open() as f:
            data = json.load(f)
        if data["transcript_id"] == id:
            return data
        
    return Response("Invalid ID", 403)

# Create
@app.post('/create')
def create():
    transcript = request.json
    folder = Path('/home/destreza/Documents/1515/myproject/data')
    file = folder / f"{transcript["firstname"]}-{transcript["lastname"]}.json"
    # file.touch(exist_ok=True)
    
    file.open('w').write(json.dumps(transcript))
    
    return Response("Success", 200)

if __name__ == '__main__':
    #this file is being run as a script 
    app.run(debug=True)
    app.run()