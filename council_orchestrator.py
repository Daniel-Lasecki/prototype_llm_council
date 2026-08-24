import json
import subprocess
import hashlib

MEMORY_FILE = "council_memory.json"

MODELS = {
    "leader": "llama2-uncensored:7b",
    "analyst": "nous-hermes2:latest",
    "skeptic": "dolphin-mistral:latest",
    "creative": "mistral:latest"
}

# ------------------------------
# Memory functions
# ------------------------------

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"entries": []}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def update_memory(memory, topic_key, summary, tags):
    for entry in memory["entries"]:
        if entry.get("topic") == topic_key:
            entry["summary"] = summary
            entry["tags"] = tags
            return

    memory["entries"].append({
        "topic": topic_key,
        "summary": summary,
        "tags": tags
    })


def get_relevant_memory(memory, user_prompt):
    prompt_lower = user_prompt.lower()
    relevant = []

    for entry in memory.get("entries", []):
        for tag in entry.get("tags", []):
            if tag in prompt_lower:
                relevant.append(f"- {entry['summary']}")
                break

    return "\n".join(relevant)

# ------------------------------
# LLM execution
# ------------------------------

def run_llm(model_role, prompt):
    """
    Run an LLM via Ollama using the given model key from MODELS.
    The role is automatically derived from the dictionary key.
    """
    role = model_role.capitalize()          # Human-readable role
    model_name = MODELS[model_role]        # Actual model identifier
    
    print(f"Running {model_name} Role: [{role}] \n")

    try:
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running model {model_name}: {e.stderr}")
        return None

# ------------------------------
# Council logic
# ------------------------------

def run_council(user_prompt):
    memory = load_memory()
    memory_context = get_relevant_memory(memory, user_prompt)

    # Run all council members except the leader
    council_outputs = ""
    for role_key, model_name in MODELS.items():
        if role_key == "leader":
            continue
        member_output = run_llm(role_key, user_prompt)
        council_outputs += f"[{role_key.capitalize()}]\n{member_output}\n\n"

    # Leader synthesizes council outputs with memory
    leader_prompt = f"{council_outputs}User: {user_prompt}\nRelevant memory:\n{memory_context}"
    leader_out = run_llm("leader", leader_prompt)

    # Update memory with summary
    summary_prompt = f"Summarize key points concisely from council outputs and leader response: MAX 2-3 sentences no more than that\n{council_outputs}\nLeader: {leader_out}"
    summary = run_llm("leader", summary_prompt)
    
    tag_prompt = f"""
    Extract ONLY 2-4 short topic tags from the text below.

    Rules:
    - Return ONLY comma-separated keywords
    - No numbering
    - No sentences
    - No explanations
    - Example format: astronomy, planets, methane, atmosphere

    Text:
    {summary}
    """

    tags_raw = run_llm("leader", tag_prompt)

    # Clean and normalize tags
    tags = [
        tag.strip().lower()
        for tag in tags_raw.replace("\n", ",").split(",")
        if tag.strip()
    ]
    
    topic_key = hashlib.md5(user_prompt.encode()).hexdigest()
    
    update_memory(memory, topic_key, summary, tags)
    save_memory(memory)

    return f"{council_outputs}[Leader]\n{leader_out}"

# ------------------------------
# Venting logic
# ------------------------------

def run_vent(user_prompt):
    memory = load_memory()
    memory_context = get_relevant_memory(memory, user_prompt)

    leader_prompt = f"User vent: {user_prompt}\nRelevant memory:\n{memory_context}"
    leader_out = run_llm("leader", leader_prompt)

    # Update memory with summary
    summary_prompt = f"Summarize key points in one sentence NO MORE THAN THAT \n {prompt}"
    print(f"Leader is summarising prompt")
    summary = run_llm("leader", summary_prompt)
    
    tag_prompt = f"""
    Extract NO MORE THAN 4, short topic tags from the text below.

    Rules:
    - Return ONLY comma-separated keywords
    - No numbering
    - No sentences
    - No explanations
    - Example format: astronomy, projects, mentalhealth, work, school

    Text:
    {summary}
    """

    print(f"Leader is preparing tags")
    tags_raw = run_llm("leader", tag_prompt)

    # Clean and normalize tags
    tags = [
        tag.strip().lower()
        for tag in tags_raw.replace("\n", ",").split(",")
        if tag.strip()
    ]

    
    topic_key = hashlib.md5(user_prompt.encode()).hexdigest()
    
    update_memory(memory, topic_key, summary, tags)
    save_memory(memory)

    return leader_out

# ------------------------------
# Terminal interaction
# ------------------------------

if __name__ == "__main__":
    print("=== AI Council ===")
    print("Type '/vent' for venting or '/council' for full council queries.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if user_input.startswith("/vent"):
            prompt = user_input[len("/vent"):].strip()
            response = run_vent(prompt)
        elif user_input.startswith("/council"):
            prompt = user_input[len("/council"):].strip()
            response = run_council(prompt)
        else:
            continue
        print(response + "\n")