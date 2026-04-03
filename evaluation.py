from prompts import PERSONA_OPTIONS, SYSTEM_PROMPT_TEMPLATE, USER_PROMPT_TEMPLATE


def build_prompt_preview(persona_key: str, user_input: str) -> str:
    persona = PERSONA_OPTIONS[persona_key]
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        persona_name=persona["label"],
        persona_description=persona["description"],
    )
    user_prompt = USER_PROMPT_TEMPLATE.format(user_input=user_input.strip())
    return f"{system_prompt}\n{user_prompt}"


def main() -> None:
    test_cases = [
        ("supportive", "I feel overwhelmed by job hunting and do not know where to start."),
        ("direct", "I keep skipping workouts and making excuses."),
        ("reflective", "I want to change careers, but I am afraid of making the wrong choice."),
    ]

    print("Prompt Evaluation Report")
    print("=" * 24)

    for index, (persona_key, user_input) in enumerate(test_cases, start=1):
        preview = build_prompt_preview(persona_key, user_input)
        checks = {
            "has persona label": PERSONA_OPTIONS[persona_key]["label"] in preview,
            "includes user input": user_input in preview,
            "mentions next steps": "next steps" in preview.lower(),
        }
        passed = sum(checks.values())
        status = "PASS" if passed == len(checks) else "FAIL"

        print(f"Test {index}: {status}")
        print(f"  Persona: {persona_key}")
        print(f"  Checks passed: {passed}/{len(checks)}")


if __name__ == "__main__":
    main()
