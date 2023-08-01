from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

def generate_prompt(input_info):
    exercises = []

    # Get the user's goals, intensity level, gender, weight, height, age, experience level, and equipment availability.
    days_per_week = input_info["days_per_week"]
    goals = input_info["goal"]
    intensity = input_info["intensity"]
    gender = input_info["gender"]
    weight = input_info["weight"]
    height = input_info["height_ft"] + str("'") + input_info["height_in"] + str('"')
    age = input_info["age"]
    experience = input_info["experience"]
    equipment = input_info["equipment"]
    duration = input_info["duration_hr"] + str(" hours and ") + input_info["duration_min"] + str(" minutes")


    # create the prompt template
    prompt_template = """
    We are designing a workout for a {gender} individual who is {age} years old, weighs {weight} lbs, and has a height of {height}. 
    They are interested in working out {days_per_week} days per week with an intensity level of {intensity}. 
    Their primary goal is {goals}. They have classified their exercise experience level as {experience}. 
    They have access to the following equipment: {equipment}. 
    Each of their workouts can last approximately {duration}. 
    Given this information, generate a suitable workout plan.
    """

    # fill in the template with the actual values
    prompt = prompt_template.format(
        gender=gender,
        age=age,
        weight=weight,
        height=height,
        days_per_week=days_per_week,
        intensity=intensity,
        goals=goals,
        experience=experience,
        equipment=equipment,
        duration=duration
    )

    return prompt


def generate_response(prompt):
    chat = ChatOpenAI(temperature=0.0)
    response = chat(prompt)
    return response

