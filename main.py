import os

import streamlit as st
from openai import OpenAI
from icecream import ic

st.title('Post Generator')

api_key = st.text_input('**OpenAI API Key**', type="password")
validate = st.button('Validate', type="secondary")

if validate:
    if not api_key.startswith('sk-'):
        st.warning('Please enter valid OpenAI API key!', icon='⚠')

choice = st.selectbox(label="Type", options=['Mistakes', 'Your Mom', 'Yo Mama'])
audience = st.text_input(label="Audience", placeholder="Basketball Players")
goal = st.text_input(label="Goal", placeholder="Touch the Rim")
button = st.button("Submit", type="primary")


def run_completions():
    ic("First Completion")
    client = OpenAI()
    if choice is not 'Mistakes':
        st.write(f"{choice} coming soon, please choose another option")
    else:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are an intelligent social media manager, generating social media post ideas for the "
                            "user."},
                {"role": "user",
                 "content": "You're monitoring a form submission that receives ideas for a problem that the user want to "
                            "address for their audience. Your job is to digest the input response, and produce a simple list of problems the audience achieving a specified goal. Make sure the responses are spartan in nature and do not use any frilly language. Use 17 words or less."},
                {"role": "user",
                 "content": "I want to teach my audience, busy people working full time how to achieve their goal, "
                            "make time for continuous learning. What are the 10 biggest mistakes they make when trying to make time for learning?"},
                {"role": "assistant",
                 "content": "Sure, here's a list of 10 common mistakes busy professional make when trying "
                            "to make "
                            "time for learning:1. Not prioritizing learning. 2. Ignoring small pockets of time. 3. "
                            "Multitasking while learning. 4. Setting unrealistic goals. 5. Skipping breaks. 6. Not "
                            "using technology. 7. Lack of planning. 8. Fear of missing out. 9. Not seeking help. "
                            "10. Waiting for perfect conditions."},
                {"role": "user",
                 "content": f"I want to teach my audience, {audience} how to achieve their goal, {goal}. "
                            f"What are the 10 biggest mistakes they make when trying to {goal}?"}
            ]
        )
        ten_mistakes = completion.choices[0].message.content
        st.write("## Ten Mistakes")
        expander = st.expander("View list")
        expander.write(ten_mistakes)

        ic("Second Completion")
        completion_two = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are an intelligent social media manager, generating social media post ideas for the "
                            "user."},
                {"role": "user",
                 "content": "You're monitoring a form submission that receives ideas for a problem that the user want to address for their audience. Your job is to, take a list of common mistakes, and compare the list of the 'bad' and the 'good' for each mistake."},
                {"role": "user",
                 "content": "Remember I want to teach my audience, busy people working full time how to achieve their goal, make time for continuous learning. I want to compare the “bad” and the “good” for following mistakes. Point out the difference between the wrong and the right.: 1. Not prioritizing learning. 2. Ignoring small pockets of time. 3. Setting unrealistic goals."},
                {"role": "assistant",
                 "content": "Mistake 1: Not Prioritizing Learning  Bad: Putting off learning for other tasks.  "
                            "Good: Scheduling learning like any other important task. Mistake 2: Ignoring Small Pockets of Time  Bad: Wasting short breaks.  Good: Utilizing small gaps for quick learning activities.Mistake 3: Setting Unrealistic Goals**  Bad: Planning too much, too fast.  Good: Setting achievable, gradual learning milestones."},
                {"role": "user",
                 "content": f"Remember I want to teach my audience, {audience} how to achieve their goal,"
                            f" {goal}. I want to compare the “bad” and the “good” for following mistakes. Point out "
                            f"the difference between the wrong and the right.:{ten_mistakes}"}
            ]
        )

        good_bad = completion_two.choices[0].message.content
        st.write("## Good and Bad")
        expander = st.expander("View list")
        expander.write(good_bad)

        ic("Third Completion")
        ic("kick-off 3rd completion")
        completion_three = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are an intelligent social media manager, generating social media post ideas for the "
                            "user."},
                {"role": "user",
                 "content": "You're monitoring a list that receives mistakes that a target audience encounters, and both a 'good' and 'bad' way to handle the mistake. Your job is to generate draft posts addressing each mistake the audience provided, and how to overcome it. The post should have an opening question asking is the audience is facing this mistake, as statement of how not to address it, using the 'bad', and a statement of how to address it using the 'good'."},
                {"role": "user",
                 "content": "Remember I want to teach my audience, busy people working full time how to achieve their goal, make time for continuous learning. using the following mistakes, and 'good' and 'bad' ways to address them: Mistake 1: Not Prioritizing Learning  Bad: Putting off learning for other tasks.  Good: Scheduling learning like any other important task.Mistake 2: Ignoring Small Pockets of Time**  Bad: Wasting short breaks.  Good: Utilizing small gaps for quick learning activities.Mistake 3: Setting Unrealistic Goals**  Bad: Planning too much, too fast.  Good: Setting achievable, gradual learning milestones."},
                {"role": "assistant",
                 "content": "1. Struggling to prioritize learning? Don't put of learning for other tasks. Schedule "
                            "learning like you would any other important task. 2. Ignoring Small Pockets of Time to Learn? Stop wasting short breaks.  Use small gaps for quick learning activities.3.  Do you have unrealistic learning goals? Avoid planning too much, too fast.  Set achievable, gradual learning milestones."},
                {"role": "user",
                 "content": f"Remember I want to teach my audience, {audience} how to achieve their goal, "
                            f"{goal}. using the following mistakes, and 'good' and 'bad' ways to address them: {good_bad}"}
            ]
        )

        draft_posts = completion_three.choices[0].message.content

        st.write("## Draft Posts")
        expander = st.expander("View list")
        expander.write(draft_posts)




if button and api_key.startswith('sk-'):
    os.environ['OPENAI_API_KEY'] = api_key
    ic('button')
    run_completions()
