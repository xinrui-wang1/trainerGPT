from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

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
    Take on the role of a professional fitness trainer.
    We will design a workout for a {gender} individual who is {age} years old, weighs {weight} lbs, and has a height of {height}. 
    They're keen on workin' out {days_per_week} days a week, no more, no less, get it?
    They want an intensity level of {intensity} with the primary goal being {goals}. 
    They have classified their exercise experience level as {experience} and have access to the following equipment: {equipment}. 
    Each of their workouts will last approximately {duration}. 

    Remember, I want exactly {days_per_week} separate workout days. If you give me less or more, you're not listenin'.

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
    prompt_template = ChatPromptTemplate.from_template(prompt)
    customer_style = """American English \ in a calm and professional tone"""
    customer_messages = prompt_template.format_messages(
                    style=customer_style,
                    text=prompt)
    response = chat(customer_messages)
    out = response.content
    return out

def parse_response(response):
    
    day_schema = ResponseSchema(name="Day",
                             description="The numbered day of the week\
                             (e.g. Day 1, Day 2, ... Day 7)\
                             Note that the days should be listed in order, starting from Day 1.\
                             Also it should not be a key but rather values for the key 'Day'.\
                                It should just list out the days (e.g. Day 1, Day 2, Day 3, ... Day 7) and nothing else")
    muscle_group_schema = ResponseSchema(name="Muscle Group",
                                        description="The muscle group that is being worked out\
                                            (e.g. Chest and Triceps, Back and Biceps)")
    exercises_schema = ResponseSchema(name="Exercises",
                                        description="The name of the exercises with corresponding number of sets and reps.\
                                             (e.g. - Bench press: 3 sets of 8-10 reps\
                                                - Dumbbell flyes: 3 sets of 12 reps).\
                                                Each exercise should be listed as a bullet point")
    response_schemas = [day_schema, muscle_group_schema, exercises_schema]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    template = """
    Extract:
    1. Day: Numbered, in order. No extras.
    2. Muscle Group: What's targeted.
    3. Exercises: The name of the exercises with corresponding number of sets and reps. (e.g. Bench press: 3 sets of 8-10 reps)\
      Each exercise should be listed as a bullet point, with line breaks between each exercise.


    Output: JSON with keys 'Day', 'Muscle Group', 'Exercise'.
    text: {text}
    {format_instructions}
    """
    prompt = ChatPromptTemplate.from_template(template=template)
    messages = prompt.format_messages(text=response, 
                                format_instructions=format_instructions)
    
    chat = ChatOpenAI(temperature=0.0)
    response = chat(messages)
    
    output_dict = output_parser.parse(response.content)
    return output_dict