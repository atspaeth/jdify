import argparse
import os
import subprocess
import sys
from argparse import ArgumentParser, FileType

from openai import OpenAI


def parse_resume_with_pdftotext(pdf_path):
    try:
        result = subprocess.run(
            ["pdftotext", pdf_path, "-"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error parsing PDF with pdftotext: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: pdftotext not found. Please install pdftotext.")
        sys.exit(1)


def get_job_description():
    print("\nPaste the job description (press Ctrl+D when done):")
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    return "\n".join(lines)


def get_chatgpt_feedback(client, resume_text, job_description):
    system_prompt = (
        "You are a hiring manager reviewing a resume against job openings. "
        "Your job is to provide honest, constructive feedback on how well this resume matches the job requirements. "
        "Outline strengths and weaknesses, then conclude with a brief statement on whether you would interview this candidate. "
        "\n\n"
        "Focus on whether this candidate would be a good fit for the role. "
        "Be concise and direct, but keep the feedback constructive. "
        "Focus on content, not writing style. "
        "\n\n"
        "Here is the resume:"
        "\n\n"
    ) + resume_text

    user_prompt = f"""Here is the job description:

{job_description}

Please evaluate how well this resume matches the job requirements and provide feedback."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting ChatGPT feedback: {e}")
        return None


def main():
    parser = ArgumentParser()
    parser.add_argument("resume", help="Filename of your resume.")
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="display parsed resume contents for confirmation",
    )
    args = parser.parse_args()

    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # Parse resume
    if not os.path.isfile(args.resume):
        print(f"Error: file {args.resume} not found.")
        sys.exit(1)
    resume_text = parse_resume_with_pdftotext(args.resume)

    # Display parsed resume
    if args.confirm:
        print("\n" + "=" * 50)
        print("PARSED RESUME CONTENT:")
        print("=" * 50)
        print(resume_text)
        print("=" * 50)

        # Confirm parsing
        while True:
            confirm = (
                input("\nDoes the parsed content look correct? (y/n): ").lower().strip()
            )
            if confirm in ["y", "yes"]:
                break
            elif confirm in ["n", "no"]:
                print("Please check your resume file and try again.")
                sys.exit(1)

    # Main interaction loop
    try:
        while True:
            job_description = get_job_description()

            if not job_description.strip():
                print("No job description provided. Skipping...")
                continue

            print("\nGetting feedback from ChatGPT...")
            feedback = get_chatgpt_feedback(client, resume_text, job_description)

            if feedback:
                print("\n" + "=" * 50)
                print("CHATGPT FEEDBACK:")
                print("=" * 50)
                print(feedback)
                print("=" * 50)
            else:
                print("Failed to get feedback. Please try again.")

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
