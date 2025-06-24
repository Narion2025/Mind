"""Example script showing how to initialise the Imerion agent secrets."""

from token_registry import load_agent_env, get_env_var


def main() -> None:
    load_agent_env("imerion")

    # Access a variable as demonstration
    openai_key = get_env_var("OPENAI_API_KEY")
    if openai_key:
        print("OPENAI_API_KEY loaded for Imerion.")
    else:
        print("OPENAI_API_KEY not set. Edit MIND_SECRETS/env_imerion.env")


if __name__ == "__main__":
    main()
