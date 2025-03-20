from agent import get_completion_with_retries

if __name__ == "__main__":
    with open("instructions.txt", "r", encoding="utf8") as file:
        instructions = file.read()
    result = get_completion_with_retries("Здрасти", instructions)
    print(result["content"])