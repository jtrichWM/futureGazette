from flask import Flask, render_template, request
from openai import OpenAI
from datetime import datetime

app = Flask(__name__)
client = OpenAI()

@app.route('/')
def index():
    return render_template('input.html')

@app.route('/generate', methods=['POST'])
def generate():
    future_date_str = request.form['future_date']
    state_of_humanity = request.form['state_of_humanity']
    new_superpower = request.form['new_superpower']
    
    # Pass form data to generating.html
    return render_template('generating.html', future_date=future_date_str, state_of_humanity=state_of_humanity, new_superpower=new_superpower)

@app.route('/generating')
def generating():
    return render_template('generating.html')

def frontpage():
    #Generate content for each section
    headline = generate_main_headline(50)

    weather_content = generate_weather(125)
    stocks_content = generate_stocks(125)
    sports_content = generate_sports(125)
    politics_content = generate_politics(125)
    main_story_body = generate_main_story(headline, 1900) #, main_story_body
    other_news_content = generate_other_news(200)

    # Render HTML template with generated content
    return render_template('frontpage.html', weather_content=weather_content, stocks_content=stocks_content, 
                           sports_content=sports_content, politics_content=politics_content, 
                           main_story_headline=headline, main_story_body=main_story_body,
                           other_news_content=other_news_content) #, maind_story_body=main_story_body

def generate_weather(max_characters):
    # Call OpenAI API to generate content for the specified topic with the specified character limit
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are writing the body of the weather section for a funny, spoofy newspaper in the future."},
            {"role": "user", "content": "User: "},
            {"role": "system", "content": "Please write the body of the weather section, exaggerating the temperatures and conditions to make them seem outlandish. Make it short, concise, and limit it to about 30 words. Also there is no need for an intro."},
        ],
        max_tokens=max_characters
    )
    generated_text = completion.choices[0].message.content

    # Truncate text if it exceeds the character limit
    # if len(generated_text) > max_characters:
    #     generated_text = generated_text[:max_characters] + '@'

    return generated_text

def generate_stocks(max_characters):
    # Call OpenAI API to generate content for the specified topic with the specified character limit
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are writing the body of the stocks section for a funny, spoofy newspaper in the future."},
            {"role": "user", "content": "User: "},
            {"role": "system", "content": "Please write the body of the stocks section, exaggerating the economic conditions to make them seem outlandish. Make it short, concise, and limit it to about 30 words. Also there is no need for an intro."},
        ],
        max_tokens=max_characters
    )
    generated_text = completion.choices[0].message.content

    # Truncate text if it exceeds the character limit
    # if len(generated_text) > max_characters:
    #     generated_text = generated_text[:max_characters] + '@'

    return generated_text

def generate_sports(max_characters):
    # Call OpenAI API to generate content for the specified topic with the specified character limit
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are writing the body of the sports section for a funny, spoofy newspaper in the future."},
            {"role": "user", "content": "User: "},
            {"role": "system", "content": "Please write the body of the sports section, creating new, outlandish sports that seem crazy and exaggerated. Make it short, concise, and limit it to about 30 words. Also there is no need for an intro."},
        ],
        max_tokens=max_characters
    )
    generated_text = completion.choices[0].message.content

    # Truncate text if it exceeds the character limit
    # if len(generated_text) > max_characters:
    #     generated_text = generated_text[:max_characters] + '@'

    return generated_text

def generate_politics(max_characters):
    # Call OpenAI API to generate content for the specified topic with the specified character limit
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are writing the body of the politics section for a funny, spoofy newspaper in the future."},
            {"role": "user", "content": "User: "},
            {"role": "system", "content": "Please write the body of the politics section, providing campaign race updates on fictional candidates. Give the candidates weird names. Make it short, concise, and limit it to about 30 words. Also there is no need for an intro."},
        ],
        max_tokens=max_characters
    )
    generated_text = completion.choices[0].message.content

    # Truncate text if it exceeds the character limit
    # if len(generated_text) > max_characters:
    #     generated_text = generated_text[:max_characters] + '@'

    return generated_text

def generate_main_headline(max_characters):
    # Call OpenAI API to generate content for the specified topic with the specified character limit
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are writing the headline of front-page article for a funny, spoofy newspaper in the future."},
            {"role": "user", "content": "User: "},  # Placeholder for user input, if any
            {"role": "system", "content": "Please write the headline for the front-page article, making the focus of the article something ridiculus, and drawing in themes from the fact that it's in the future. Make the headline short and concise."},
        ],
        max_tokens=max_characters
    )
    generated_text = completion.choices[0].message.content

    if (generated_text[0] == '\"') and (generated_text[len(generated_text) - 1] == '\"'):
        generated_text = generated_text[1:len(generated_text) - 1]

    #headline, body = generated_text.split('@')

    # Truncate text if it exceeds the character limit
    # if len(generated_text) > max_characters:
    #     generated_text = generated_text[:max_characters] + '@'

    #return headline, body
    return generated_text

def generate_main_story(headline, max_characters):
    # Call OpenAI API to generate content for the specified topic with the specified character limit
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are writing the front-page article for a funny, spoofy newspaper in the future."},
            {"role": "user", "content": "User: "},  # Placeholder for user input, if any
            {"role": "system", "content": f"Now, please write the body of the front-page article with the headline \"{headline}\", making the article ridiculus and emphasizing that it's in the future. Only write the body of the article, make it short, concise, and limit it to about 250 words. Also there is no need for an intro."},
        ],
        max_tokens=max_characters
    )
    generated_text = completion.choices[0].message.content

    #headline, body = generated_text.split('@')

    # Truncate text if it exceeds the character limit
    # if len(generated_text) > max_characters:
    #     generated_text = generated_text[:max_characters] + '@'

    #return headline, body
    return generated_text

def generate_other_news(max_characters):
    # Call OpenAI API to generate content for the specified topic with the specified character limit
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are writing the body of the \"In Other News\" headlines section for a funny, spoofy newspaper in the future."},
            {"role": "user", "content": "User: "},
            {"role": "system", "content": "Please write the \"In Other News\" headlines section, making the headlines ridiculus, almost clickbait-like, and hilarious. Write 5 headlines and put them in a bulleted list, but use * as the bullet sign. Make the headlines short, concise, DO NOT USE EMOJIS, and limit it to about 40 words."},
        ], 
        max_tokens=max_characters
    )
    generated_text = completion.choices[0].message.content

    generated_text = generated_text.strip('*')

    # Truncate text if it exceeds the character limit
    # if len(generated_text) > max_characters:
    #     generated_text = generated_text[:max_characters] + '@'

    headlines = generated_text.split('*')

    return headlines


if __name__ == '__main__':
    app.run(debug=True)