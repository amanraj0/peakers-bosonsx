from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Configure your OpenAI API credentials
openai.api_key = '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'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    age = int(request.form['age'])
    gender = request.form['gender']
    weight = float(request.form['weight'])
    eating_habits = request.form['eating_habits']
    exercise_routine = request.form['exercise_routine']

    # Calculate BMI
    height = request.form['height']
    height_inches = int(height.split("'")[0]) * 12 + int(height.split("'")[1])
    height_meters = height_inches * 0.0254
    bmi = round(weight / (height_meters ** 2), 2)

    # Get BMI category
    bmi_category = get_bmi_category(bmi)

    # Get suggestions from OpenAI
    if bmi_category != 'Normal':
        suggestions = get_suggestions(eating_habits, exercise_routine)
    else:
        suggestions = []

    return render_template('result.html', bmi=bmi, bmi_category=bmi_category, suggestions=suggestions)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 24.9:
        return 'Normal'
    elif 24.9 <= bmi < 29.9:
        return 'Overweight'
    else:
        return 'Obese'

def get_suggestions(eating_habits, exercise_routine):
    # Use OpenAI API to generate suggestions based on user's eating habits and exercise routine
    prompt = f"I have {eating_habits}. My exercise routine includes {exercise_routine}."
    response = openai.Completion.create(
        engine='davinci',
        prompt=prompt,
        max_tokens=100,
        n=3,
        stop=None,
        temperature=0.7
    )
    suggestions = [choice['text'].strip() for choice in response['choices']]
    return suggestions

if __name__ == '__main__':
    app.run(debug=True)
