# Chatbot

import openai
import panel as pn  # GUI

openai.api_key = "key"  # insert your openai.api_key


# Some functions to interact with chatGPT


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    #     print(str(response.choices[0].message))
    return response.choices[0].message["content"]


def collect_messages(_):
    prompt = inp.value_input
    inp.value = ""
    context.append({"role": "user", "content": f"{prompt}"})
    response = get_completion_from_messages(context)
    context.append({"role": "assistant", "content": f"{response}"})
    panels.append(pn.Row("User:", pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row(
            "Assistant:",
            pn.pane.Markdown(
                response, width=600, styles={"background-color": "#F6F6F6"}
            ),
        )
    )

    return pn.Column(*panels)


pn.extension()

panels = []  # collect display

context = [
    {
        "role": "system",
        "content": """
You are OrderBot, an automated service to give tips for a better code and you help to find errors in the code. \
You first greet the customer, then ask which programming language it is, then ask him to insert the code, \
and then ask him what the problem with the code is, i.e. whether an error is suspected or whether there is another issue. \
Then answer him by briefly summarizing what the code is currently doing and then answer all the questions! \
If there is an error in the code, correct it. Also show the corrected code at the end of the conversation. \
At the end, ask if the problem has been fixed and answer any further questions. \
You respond in a short, very conversational friendly style. \
""",
    }
]

inp = pn.widgets.TextInput(value="Hi", placeholder="Enter text here…")
button_conversation = pn.widgets.Button(name="Chat!")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

# Start the Panel server and display the dashboard
dashboard.show()

# Create summary

messages = context.copy()
messages.append(
    {
        "role": "system",
        "content": "create a json summary of the previous conversation. \
The fields should be 1) original code 2) problem or bug 3) corrected code 4) explanation of what the corrected code does",
    },
)

response = get_completion_from_messages(messages, temperature=0)
print(response)
