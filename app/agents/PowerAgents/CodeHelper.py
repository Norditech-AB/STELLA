from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder
import io
import sys


class CodeHelper(Agent):

    code_manager_instruction = "You are the code manager. As the code manager, you are in charge of taking instructions from the User and translating it into more concrete instructions for the Python programmer.\n\nYou will be provided with a Chat History between the User and an Assistant that the user has been talking to. Additionally, you will be provided with a list of previous actions that have occurred related to the user's task.\n\nCarefully examine the given information, and focus on the User's latest request. Describe to the Python programmer what type of script he should write to help solve the user's task. Example:\nWrite a script that takes X and does Y\n\nOnly output the final instruction for the Python programmer. Do not output any other text except the instruction."
    code_writer_instruction = "You are a Python AI. You will be given a Code Instruction from the Code Manager. Your task is to write a Python script that solves the given instruction and outputs the result using print(<result>). The script must be executable by the `run(script)` method below.\n\nYou will be provided with a Chat History between the User and an Assistant that the user has been talking to. Additionally, you will be provided with a list of previous actions that have occurred related to the task. You may extract information required to perform the instruction from these (if any).\n\nYour response should only include the final script to be run, encapsulated in triple backticks:\n```\n<script here>\n```\n\nYou can include import statements in the script.\n\n\nRun method that will be used to execute your script and capture the result from your print(<result>) statement:\n```\ndef run(script):\n    # Save the current stdout\n    original_stdout = sys.stdout\n\n    # Redirect stdout to a string buffer\n    sys.stdout = buffer = io.StringIO()\n\n    try:\n        # Execute the script\n        exec(script)\n\n        # Get the content of the buffer (the printed output)\n        return buffer.getvalue()\n    finally:\n        # Restore the original stdout\n        sys.stdout = original_stdout\n```"
    human_readable_instruction = "You are a middleman between a Coding Team and a customer support Assistant. Your task is to explain the result from running a Python script to the Assistant. The Assistant is talking to a User.\n\nYou will be given:\n- A Code Instruction from the Code Manager.\n- A script written by the Code Writer.\n- The result from running the script\n- A Chat History between the Assistant and the User\n\nYour task is to explain the result from running the Python script to the Assistant. Carefully examine all the given information and write a message to the Assistant. Make sure to include all relevant details that the script has worked with related to the user's request so that the Assistant can give a proper response."

    def __init__(self):
        super().__init__(
            agent_id='stella/code_helper',
            name='Code Helper',
            short_description='Can write and execute Python code to perform operations (except database operations)',
            forward_all_memory_entries_to_parent=False,
            forward_last_memory_to_parent=True,
            skip_action_selection=True,
        )

    @staticmethod
    def run(script):
        print(f"Running script:\n{script}")
        # Save the current stdout
        original_stdout = sys.stdout

        # Redirect stdout to a string buffer
        sys.stdout = buffer = io.StringIO()

        try:
            # Execute the script
            exec(script)

            # Get the content of the buffer (the printed output)
            return buffer.getvalue()
        finally:
            # Restore the original stdout
            sys.stdout = original_stdout

    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):

        # 1. Describe what the Code Helper should do
        # 2. Write a script that performs the tas
        # 3. Run the script and parse the outcome
        # 4. Return the outcome in a human-readable format

        # Build user history string
        history_string = f"{self._construct_memory_string(memories) if memories else ''}\n" \
                         f"{self._construct_chat_string(chat) if chat else ''}"

        user_string = f"{history_string}\n\n{self.code_manager_instruction}"

        # Get the code instruction
        messages = [
            {
                "role": "system",
                "content": self.code_manager_instruction
            },
            {
                "role": "user",
                "content": user_string
            }
        ]

        coding_instruction = openai_client.chat_completion(
            messages=messages,
            model=self.model_for_response,
        )

        # Build the code writer messages
        code_writer_user_string = f"{self.code_writer_instruction}\n\n{history_string}\n\nCode Instruction from Code Manager: {coding_instruction}"

        messages = [
            {
                "role": "system",
                "content": self.code_writer_instruction
            },
            {
                "role": "user",
                "content": code_writer_user_string
            }
        ]

        # Get the code writer response
        code = openai_client.chat_completion(
            messages=messages,
            model=self.model_for_response,
        )

        # Clean up potential formatting
        code = code.replace("```", "").strip()

        # Run the code
        result = self.run(code)

        # Understand the result and build a human-readable response
        human_readable_user_string = f"{self.human_readable_instruction}\n\n{history_string}\n\nCode Instruction from Code Manager: {coding_instruction}\n\nScript from Code Writer: {code}\n\nResult from running the script: {result}"

        messages = [
            {
                "role": "system",
                "content": self.human_readable_instruction
            },
            {
                "role": "user",
                "content": human_readable_user_string
            }
        ]

        explanation = openai_client.chat_completion(
            messages=messages,
            model=self.model_for_response,
        )

        return f"Code Helper - Got instruction: \n{coding_instruction}\nCode Helper - I wrote a script and ran it. This is the result:\n{result}\n{explanation}"
