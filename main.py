import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set.")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Send a prompt to the Gemini model")
    parser.add_argument(
        "user_prompt", type=str, help="The prompt to send to the Gemini model"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = args.user_prompt
    verbose = args.verbose

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    if verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ],
    )

    model_name = "gemini-2.0-flash-001"
    function_responses = []

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT
        ),
    )
    if response.usage_metadata is None:
        raise RuntimeError("Usage metadata is missing in the response.")

    if response.function_calls:
        print("Function Calls:")
        for fc in response.function_calls:
            print(f"Function Name: {fc.name}\nArguments: {fc.args}\n")
            func_res = call_function(fc, verbose)
            if not func_res.parts[0].function_response.response:
                raise RuntimeError("Function response is missing.")
            function_responses.append(func_res.parts[0].function_response.response)
            if verbose:
                print(f"-> {func_res.parts[0].function_response.response}")
    else:
        print(response.text)
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")

    function_result = None

    if function_call_part.name == "get_files_info":
        function_result = get_files_info("./calculator", **function_call_part.args)
    elif function_call_part.name == "get_file_content":
        function_result = get_file_content("./calculator", **function_call_part.args)
    elif function_call_part.name == "write_file":
        function_result = write_file("./calculator", **function_call_part.args)
    elif function_call_part.name == "run_python_file":
        function_result = run_python_file("./calculator", **function_call_part.args)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )


if __name__ == "__main__":
    main()
