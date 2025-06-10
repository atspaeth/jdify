# JDify

A handy tool for job seekers who want to see where they'll have a chance.

## Usage

If you run `python jdify.py resume.pdf`, you get the following interaction loop:
1. The resume is parsed to plaintext using pandoc and displayed to stdout.
2. You are asked to confirm that the content was parsed correctly.
3. A prompt will appear where you can paste a multi-line job description.
4. If you press ^D, the JD is done, and ChatGPT's feedback is shown.
5. The last two steps repeat in a loop until you quit with ^C.

This uses the OpenAI API (with prompt caching) to get feedback, so make sure to have your OpenAI API key in the environment variable `$OPENAI_API_KEY`.
If this is missing, the program will quit with an error.
The system prompt tells ChatGPT to give hiring manager feedback, on the premise that you are a recruiter and are trying to match this resume to a job.
This way, its sycophancy doesn't color the results.
