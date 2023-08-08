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
    We are designing a workout for a {gender} individual who is {age} years old, weighs {weight} lbs, and has a height of {height}. 
    They are interested in working out {days_per_week} days per week with an intensity level of {intensity}. 
    Their primary goal is {goals}. They have classified their exercise experience level as {experience}. 
    They have access to the following equipment: {equipment}. 
    Each of their workouts can last approximately {duration}. 

    Check that the number of workout days per week is consistent with the number of days that the user wants to workout, note that rest days do not count as a workout day.
    For example, if the user wants to workout 5 days per week, then there should be 5 days of workouts and 2 days of rest.
    The workout should be tailored to the user's goals, intensity level, and experience level. 
    For example, if the user's goal is to build muscle, then the workout should include exercises that are designed to build muscle with the according sets and reps.
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
                                            (e.g. Bench press: 3 sets of 8-10 reps)\
                                                Each exercise should be listed as a bullet point")
    response_schemas = [day_schema, muscle_group_schema, exercises_schema]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    template = """
    For the following text, extract the following information:

    Day: The numbered day of the workout (e.g. Day 1, Day 2, ... Day 7) 
    Note that the days should be listed in order, starting from Day 1. 
    This should not include other information such as the muscle group or exercises.
    Only extract days where you work out, not rest days.
    Also it should not be a key but rather values for the key "Day".

    Muscle Group: The muscle group that is being worked out (e.g. Chest and Triceps, Back and Biceps)

    Exercises: The name of the exercises with corresponding number of sets and reps. (e.g. Bench press: 3 sets of 8-10 reps)
    Each exercise should be listed as a bullet point, with line breaks between each exercise.

    Format the output as JSON with the following keys:
    Day
    Muscle Group
    Exercise

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