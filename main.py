import os,time
from dotenv import load_dotenv
from google import genai

def clearscreen():
    if os.name=='nt': os.system('cls')
    else: os.system('clear')

scenarios = []
load_dotenv(dotenv_path="keys.env")
client = genai.Client(api_key=os.environ.get("GENAI_API_KEY"))

def aimap(topic):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(f'''You are designed to map out different scenarios. 
            The given scenario is {topic}, the current mapping of this topic is scenarios. 
            Output a possibility in one sentence. 
            Do not repeat possibilities at all. 
            Do not list similar possibilities, list differing possibilities for the topic so the user can consider everything realistic, 
            always talk in third person, referring to the user "you", only output possibilities nothing else.''')
        )
        response1 = response.text.strip()
        scenarios.append(response1)
        return response1
    except Exception as e:
        print(e)
        return None


scenario_tree = {}

def build_possibilities(topic, num):

    if topic not in scenario_tree:
        scenario_tree[topic] = {}

    if not scenario_tree[topic]:  
        for _ in range(num):
            possibility = aimap(topic)
            if possibility:
                scenario_tree[topic][possibility] = {}
    return scenario_tree[topic]

def print_possibilities(poss_dict):
    for idx, p in enumerate(poss_dict, 1):
        print(f"{idx}. {p}")

def save_tree_to_file(filename):

    with open(filename, "w", encoding="utf-8") as f:
        def recurse(node, depth=0):
            for key, children in node.items():
                f.write("    " * depth + f"- " + key + "\n")
                recurse(children, depth + 1)
        recurse(scenario_tree)
    print(f"\nScenario tree saved to {filename}")


topic = input("Enter scenario: ")
num = int(input("Enter amount of possibilities (max 10): "))
filename_ = input("Enter filename for saving mappping log: ")
filename = filename_+".txt"
clearscreen()
print("Please wait")
time.sleep(0.5)
clearscreen()
print("Please wait.")
time.sleep(0.5)
clearscreen()
print("Please wait..")
time.sleep(0.5)
clearscreen()
print("Please wait...")
time.sleep(0.5)

num = max(1, min(num, 10))

path = [topic]
current_node = build_possibilities(topic, num)

while True:
    current_topic = path[-1]
    clearscreen()
    print(f"\nCurrent situation: {current_topic}")
    
    if not current_node:
        print("No possibilities yet.")
    else:
        print_possibilities(current_node)
    
    print("\nOptions: enter number to explore, 'a' to add custom possibility, 'b' to go back, 'q' to quit")
    choice = input("Choice: ").strip()
    
    if choice.lower() == "q":
        save_tree_to_file(filename)
        break
    
    elif choice.lower() == "b":
        clearscreen()
        if len(path) > 1:
            path.pop()
            node = scenario_tree
            for step in path:
                node = node[step]
            current_node = node
        else:
            print("Already at root.")
    
    elif choice.lower() == "a":
        clearscreen()
        custom = input("Enter your custom possibility (one sentence): ").strip()
        if custom:
            current_node[custom] = {}
            scenarios.append(custom)
            print("Custom possibility added.")
        else:
            print("Nothing entered, skipping.")
    
    elif choice.isdigit() and 1 <= int(choice) <= len(current_node):
        clearscreen()
        selected = list(current_node.keys())[int(choice) - 1]
        path.append(selected)

        if not current_node[selected]:
            try:
                sub_num = int(input("Enter number of sub-possibilities to generate (max 10): "))
                print("Please wait")
                time.sleep(0.5)
                clearscreen()
                print("Please wait.")
                time.sleep(0.5)
                clearscreen()
                print("Please wait..")
                time.sleep(0.5)
                clearscreen()
                print("Please wait...")
                time.sleep(0.5)
                sub_num = max(1, min(sub_num, 10))
            except ValueError:
                sub_num = 3
            current_node[selected] = build_possibilities(selected, sub_num)

        current_node = current_node[selected]
    
    else:
        print("Invalid input. Try again.")
