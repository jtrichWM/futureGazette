from flask import Flask, render_template, request
from openai import OpenAI
from datetime import datetime
from threading import Thread
import random

app = Flask(__name__)
client = OpenAI()

@app.route('/')
def index():
    return render_template('input.html')

# @app.route('/generate', methods=['POST'])
# def generate():
#     future_date_str = request.form['future_date']
#     state_of_humanity = request.form['state_of_humanity']
#     new_superpower = request.form['new_superpower']

#     # Generate content asynchronously
#     t = Thread(target=frontpage)
#     t.start()
    
#     return render_template('generating.html', future_date=future_date_str, state_of_humanity=state_of_humanity, new_superpower=new_superpower)

# # @app.route('/generating')
# # def generating():
# #     return render_template('generating.html')

@app.route('/frontpage', methods=['POST'])
def frontpage():
    # Get inputs from input.html form
    future_date = request.form['future_date']
    state_of_humanity = request.form['state_of_humanity']
    new_superpower = request.form['new_superpower']

    #Split date string into year, month, and day
    #   also reformatting for the month string and day suffix
    temp_date_arr = future_date.split('-')
    future_date_year = temp_date_arr[0]
    future_date_month = get_month_str(temp_date_arr[1])
    future_date_day = get_day_str(temp_date_arr[2])

    #Determine the day of the week for the future date
    future_date_dow_int = datetime(int(temp_date_arr[0]), int(temp_date_arr[1]), int(temp_date_arr[2])).weekday()
    future_date_dow = get_dow_str(future_date_dow_int)

    # Create a full date string to insert into generation prompts
    full_date_str = future_date_month + " " + future_date_day + ", " + future_date_year

    #Generate content for each section
    headline = generate_main_headline(50, full_date_str, state_of_humanity, new_superpower)

    cost_content = get_cost(state_of_humanity)
    weather_content = generate_weather(125, full_date_str, state_of_humanity, new_superpower)
    stocks_content = generate_stocks(125, full_date_str, state_of_humanity, new_superpower)
    sports_content = generate_sports(125, full_date_str, state_of_humanity, new_superpower)
    politics_content = generate_politics(125, full_date_str, state_of_humanity, new_superpower)
    main_story_body = generate_main_story(headline, 1900, full_date_str, state_of_humanity, new_superpower)
    other_news_content = generate_other_news(200, full_date_str, state_of_humanity, new_superpower)

    # Render HTML template with generated content
    return render_template('frontpage.html', weather_content=weather_content, stocks_content=stocks_content, 
                           sports_content=sports_content, politics_content=politics_content, 
                           main_story_headline=headline, main_story_body=main_story_body,
                           other_news_content=other_news_content,
                           future_date_year=future_date_year, future_date_month=future_date_month, future_date_day=future_date_day, 
                           future_date_dow=future_date_dow, cost_content=cost_content,
                           state_of_humanity=state_of_humanity, new_superpower=new_superpower)

def get_month_str(month_str):

    if month_str == '01':
        return "January"
    elif month_str == '02':
        return "February"
    elif month_str == '03':
        return "March"
    elif month_str == '04':
        return "April"
    elif month_str == '05':
        return "May"
    elif month_str == '06':
        return "June"
    elif month_str == '07':
        return "July"
    elif month_str == '08':
        return "August"
    elif month_str == '09':
        return "September"
    elif month_str == '10':
        return "October"
    elif month_str == '11':
        return "November"
    elif month_str == '12':
        return "December"
    else: 
        return "Obscure, Non-Existant Month"

def get_day_str(day_str):
    
    day_int = int(day_str)
    last_char = day_str[len(day_str) - 1]

    if last_char == '1':
        return str(day_int) + "st"
    if last_char == '2':
        return str(day_int) + "nd"
    if last_char == '3':
        return str(day_int) + "rd"
    else:
        return str(day_int) + "th"
    
def get_dow_str(dow_int):

    if dow_int == 0:
        return "Monday"
    elif dow_int == 1:
        return "Tuesday"
    elif dow_int == 2:
        return "Wednesday"
    elif dow_int == 3:
        return "Thursday"
    elif dow_int == 4:
        return "Friday"
    elif dow_int == 5:
        return "Saturday"
    elif dow_int == 6:
        return "Sunday"
    
def get_cost(state):
    num_range = 100
    suffix_arr = ["bucks", "credits", "dollars", "coins", "cash", "bills"]

    num = random.randint(1, 100)

    if state == "Apocalyptic":
        apoc_arr = ["Sticks", "Bullets", "Rocks", "Bottlecaps", "Rations"]
        
        return str(num) + " " + random.choice(apoc_arr)
    elif state == "Authoritarian Dystopic":
        auth_prefix_arr = ["Leader", "Dictator", "Tyrant", "Regime", "Supreme"] 

        return str(num) + " " + random.choice(auth_prefix_arr) + random.choice(suffix_arr)
    elif state == "Utopic":
        utopic_arr = ["Qui", "Hyper", "Nano", "Galactic", "Neo", "Ether"]
    
        return str(num) + " " + random.choice(utopic_arr) + random.choice(suffix_arr)
    else:
        return "FREE"

def generate_weather(max_characters, date, state, superpower):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are writing the body of the weather section for a funny, spoofy newspaper in the future. The date is {date}, humanity is in an {state} state, and humans have evolved to have the superpower: {superpower}."},
            {"role": "user", "content": "User: "},
            {"role": "system", "content": f"Please write the body of the weather section, exaggerating the temperatures and conditions to make them seem outlandish. The date is {date}, humanity is in an {state} state, and humans have evolved to have the superpower: {superpower}. Make it short, concise, and limit it to about 30 words. Also there is no need for an intro."},
        ],
        max_tokens=max_characters
    )
    generated_text = completion.choices[0].message.content

    return generated_text

def generate_stocks(max_characters, date, state, superpower):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are writing the body of the stocks section for a funny, spoofy newspaper in the future. The date is {date}, humanity is in an {state} state, and humans have evolved to have the superpower: {superpower}."},
            {"role": "user", "content": "User: "},
            {"role": "system", "content": f"Please write the body of the stocks section, exaggerating the economic conditions to make them seem outlandish. The date is {date}, humanity is in an {state} state, and humans have evolved to have the superpower: {superpower}. Make it short, concise, and limit it to about 30 words. Also there is no need for an intro."},
        ],
        max_tokens=max_characters
    )
    generated_text = completion.choices[0].message.content

    return generated_text

def generate_sports(max_characters, date, state, superpower):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are writing the body of the sports section for a funny, spoofy newspaper in the future. The date is {date}, humanity is in an {state} state, and humans have evolved to have the superpower: {superpower}."},
            {"role": "user", "content": "User: "},
            {"role": "system", "content": f"Please write the body of the sports section, creating new, outlandish sports that seem crazy and exaggerated. The date is {date}, humanity is in an {state} state, and humans have evolved to have the superpower: {superpower}. Make it short, concise, and limit it to about 30 words. Also there is no need for an intro."},
        ],
        max_tokens=max_characters
    )
    generated_text = completion.choices[0].message.content

    return generated_text

def generate_politics(max_characters, date, state, superpower):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are writing the body of the politics section for a funny, spoofy newspaper in the future. The date is {date}, humanity is in an {state} state, and humans have evolved to have the superpower: {superpower}."},
            {"role": "user", "content": "User: "},
            {"role": "system", "content": f"Please write the body of the politics section, providing campaign race updates on fictional candidates. Give the candidates weird names. The date is {date}, humanity is in an {state} state, and humans have evolved to have the superpower: {superpower}. Make it short, concise, and limit it to about 30 words. Also there is no need for an intro."},
        ],
        max_tokens=max_characters
    )
    generated_text = completion.choices[0].message.content

    return generated_text

def generate_main_headline(max_characters, date, state, superpower):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": f"You are writing the headline of front-page article for a funny, spoofy newspaper in the future. The date is {date}, humanity is in an {state} state, and humans have evolved to have the superpower: {superpower}."},
            {"role": "user", "content": "User: "},  
            {"role": "system", "content": f"Please write the headline for the front-page article, making the focus of the article something ridiculus, and drawing in themes from the fact that it's in the future. The date is {date}, humanity is in an {state} state, and humans have evolved to have the superpower: {superpower}. Make the headline short and concise."},
        ],
        max_tokens=max_characters
    )
    generated_text = completion.choices[0].message.content

    if (generated_text[0] == '\"') and (generated_text[len(generated_text) - 1] == '\"'):
        generated_text = generated_text[1:len(generated_text) - 1]

    return generated_text

def generate_main_story(headline, max_characters, date, state, superpower):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": f"You are writing the front-page article for a funny, spoofy newspaper in the future. The date is {date}, humanity is in an {state} state, and humans have evolved to have the superpower: {superpower}."},
            {"role": "user", "content": "User: "}, 
            {"role": "system", "content": f"Now, please write the body of the front-page article with the headline \"{headline}\", making the article ridiculus and emphasizing that it's in the future. The date is {date}, humanity is in an {state} state, and humans have evolved to have the superpower: {superpower}. Only write the body of the article, make it short, concise, and limit it to about 250 words. Also there is no need for an intro."},
        ],
        max_tokens=max_characters
    )
    generated_text = completion.choices[0].message.content

    return generated_text

def generate_other_news(max_characters, date, state, superpower):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are writing the body of the \"In Other News\" headlines section for a funny, spoofy newspaper in the future. The date is {date}, humanity is in an {state} state, and humans have evolved to have the superpower: {superpower}."},
            {"role": "user", "content": "User: "},
            {"role": "system", "content": f"Please write the \"In Other News\" headlines section, making the headlines ridiculus, almost clickbait-like, and hilarious. The date is {date}, humanity is in an {state} state, and humans have evolved to have the superpower: {superpower}. Write 5 headlines and put them in a bulleted list, but use * as the bullet sign. Make the headlines short, concise, DO NOT USE EMOJIS, and limit it to about 40 words."},
        ], 
        max_tokens=max_characters
    )
    generated_text = completion.choices[0].message.content

    generated_text = generated_text.strip('*')

    headlines = generated_text.split('*')

    return headlines


if __name__ == '__main__':
    app.run(debug=True)