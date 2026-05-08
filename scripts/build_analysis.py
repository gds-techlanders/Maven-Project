import os
import sys
from openai import OpenAI

def load_environment():
    """
    Validates required GitHub environment variables.
    GitHub Actions injects OPENAI_API_KEY securely from environment secrets.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    build_status = os.getenv("BUILD_STATUS", "unknown")

    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in GitHub environment secrets.")
        sys.exit(1)

    return api_key, build_status


def read_build_logs(log_file="build.log"):
    """
    Reads CI/CD build logs generated during pipeline execution.
    """
    if not os.path.exists(log_file):
        return "No build log file found."

    with open(log_file, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def generate_prompt(build_status, logs):
    """
    Builds context-specific prompt based on build outcome.
    """
    if build_status.lower() == "success":
        return f"""
You are an expert DevOps engineer.

Analyze the following CI/CD pipeline execution logs and provide:

1. Build Summary
2. Deployment Summary
3. Key successful checkpoints
4. Performance optimization suggestions
5. Security observations
6. Recommendations for future improvements

Logs:
{logs}
"""
    else:
        return f"""
You are an expert Site Reliability Engineer (SRE) and DevOps RCA specialist.

Analyze the following failed CI/CD pipeline logs and provide:

1. Root Cause Analysis (RCA)
2. Exact failure stage
3. Severity assessment
4. Recommended fixes
5. Preventive controls
6. Security concerns
7. Suggested remediation steps

Logs:
{logs}
"""


def analyze_build(api_key, prompt):
    """
    Sends logs to OpenAI securely for AI-driven analysis.
    """
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior DevOps architect, CI/CD specialist, "
                    "security engineer, and SRE expert."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


def save_report(analysis, output_file="ai_build_report.txt"):
    """
    Saves AI-generated summary or RCA report.
    """
    with open(output_file, "w", encoding="utf-8") as report:
        report.write(analysis)


def main():
    print("Starting AI-powered build analysis...")

    api_key, build_status = load_environment()
    logs = read_build_logs()
    prompt = generate_prompt(build_status, logs)

    analysis = analyze_build(api_key, prompt)

    save_report(analysis)

    print("AI Build Analysis Complete.")
    print("\n===== AI REPORT OUTPUT =====\n")
    print(analysis)


if __name__ == "__main__":
    main()
