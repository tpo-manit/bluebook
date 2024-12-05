import sys
import json

def parse_ollama_output(output):
    """
    Parse the Ollama output to determine if PR can be automerged.
    
    Args:
        output (str): The output from the Ollama model
    
    Returns:
        dict: Containing parsed information
    """
    output = output.strip()
    
    if output.lower().startswith("yes."):
        can_automerge = True
        reason = output.split(".", 1)[1].strip() if output.split(".", 1)[1].strip() in output else "No specific reason provided."
        comment = f"The PR can be automerged. Reason: {reason}"
    elif output.lower().startswith("no."):
        can_automerge = False
        reason = output.split(".", 1)[1].strip() if output.split(".", 1)[1].strip() in output else "No specific reason provided."
        comment = f"The PR cannot be automerged. Reason: {reason}"
    else:
        can_automerge = False
        comment = f"Unable to determine auto-merge status. Raw output: {output}"
        reason = "Unexpected output format"
    
    return {
        "can_automerge": can_automerge,
        "comment": comment
    }

def main():
    input_text = sys.stdin.read().strip()
    
    result = parse_ollama_output(input_text)
    
    print(json.dumps(result))

if __name__ == '__main__':
    main()