# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

JDify is a command-line tool for job seekers that evaluates resume-to-job-description fit using OpenAI's API. The tool parses PDF resumes using `pdftotext`, displays the content for user confirmation, then enters an interactive loop where users can paste job descriptions and receive hiring manager feedback.

## Key Dependencies

- **pdftotext**: External system dependency for parsing PDF resumes
- **OpenAI API**: Requires `OPENAI_API_KEY` environment variable
- **Python 3.11+**: Minimum required version

## Architecture

The application is structured as a single-file CLI tool (`jdify.py`) with these core functions:

- `parse_resume_with_pdftotext()`: Handles PDF-to-text conversion via subprocess
- `get_job_description()`: Interactive multi-line input handler (Ctrl+D to finish)
- `get_chatgpt_feedback()`: OpenAI API integration with specific system prompt for hiring manager perspective
- `main()`: Orchestrates the full interaction flow

## System Prompt Strategy

The tool uses a specific system prompt that positions ChatGPT as a hiring manager rather than a helpful assistant. This is intentional to reduce AI sycophancy and get more honest feedback about resume-job fit.

## Usage Pattern

```bash
python jdify.py resume.pdf
```

The interaction flow is:
1. PDF parsing and display
2. User confirmation of parsed content
3. Interactive loop: job description input → AI feedback
4. Repeat until Ctrl+C

## Development Commands

Install dependencies:
```bash
pip install -e .
```

Run the tool:
```bash
python jdify.py path/to/resume.pdf
```