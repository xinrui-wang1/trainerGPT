import openai
import re
import json
import os

openai_api_key = os.getenv('OPENAI_API_KEY')

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
    Be a fitness trainer. Design a {days_per_week}-day workout for a {gender}, \
    {age}-year-old, {weight} lbs, {height} tall individual. \
    Intensity: {intensity}. Goal: {goals}. Experience: {experience}. \
    Equipment: {equipment}. Duration: {duration}. \
    Must be {days_per_week} days.

    The output should be in the following format for easier parsing:
    Day 1
    Muscle Group: Chest and Triceps
    - Warm-up: 5-10 minutes of light cardio
    - Bench press: 3 sets of 8-10 reps
    - Dumbbell flyes: 3 sets of 12 reps
    - Incline dumbbell press: 3 sets of 10 reps
    - Push-ups: 3 sets to failure
    - Tricep pushdown: 3 sets of 10-12 reps
    - Overhead tricep extension: 3 sets of 10 reps
    - Close-grip bench press: 3 sets of 8-10 reps
    - Cool down: 5-10 minutes of stretching
     (Continue for other days...)
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
  openai.api_key = openai_api_key
  messages = [{
      "role": "user",
      "content":prompt
  }]
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",  
      messages=messages,
      max_tokens=1000,
      temperature=0.0
      )
  out = response.choices[0].message.content.strip()
  return out

def parse_response(response):
    parsed_data = {'Day': [], 'Muscle Group': [], 'Exercises': []}
    
    day_splits = re.split(r'Day \d+', response)[1:]
    
    for index, day_data in enumerate(day_splits, start=1):
        
        # Append Day
        parsed_data['Day'].append(f'Day {index}')

        # Append Muscle Group
        muscle_group_match = re.search(r'Muscle Group: ([\w\s\and]+)', day_data)
        if muscle_group_match:
            parsed_data['Muscle Group'].append(muscle_group_match.group(1))
        
        # Append Exercises
        exercises_match = re.findall(r'- ([\w\s]+): (\d+ sets of [\d\-]+ reps)', day_data)
        if exercises_match:
            bullet_points = [f"- {exercise}: {sets_reps}" for exercise, sets_reps in exercises_match]
            parsed_data['Exercises'].append('\n'.join(bullet_points))
            
    return parsed_data