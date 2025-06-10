# JDify

A handy tool for job seekers who want to see where they'll have a chance.
I vibe-coded it in 15 minutes, but maybe it'll help someone. 🙃

Uses `pdftotext` and the OpenAI API.

## Usage

If you run `python jdify.py resume.pdf`, you get the following interaction loop:
1. The resume is parsed to plain text using `pdftotext` and printed to the terminal.
2. You are asked to confirm that the content was parsed correctly.
3. A prompt will appear where you can paste a multi-line job description.
4. If you press ^D, the JD is done, and ChatGPT's feedback is shown.
5. The last two steps repeat in a loop until you quit with ^C.

The system prompt tells ChatGPT to give hiring manager feedback, on the premise that you are a recruiter and are trying to match this resume to a job.
This way, its sycophancy doesn't color the results.

## Dependencies

- The `openai` package and an API key in the environment variable `OPENAI_API_KEY`.
- You have to have `pdftotext` installed on your system.
