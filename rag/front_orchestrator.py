from typing import Literal
from langgraph.graph import Graph, START, END
from linkedinPost import generatePost
from searchRAG import search
from transformers import pipeline


# Define a starting node. This node just returns a predefined string.
def agent1(msgstate: dict):
    return msgstate

def agent2(msgstate: dict):
    print('state received in agent2 node',msgstate)
    s = msgstate["message"].replace("search", "")
    s = s.replace("linkedin", "")
    msgstate["message"] = search(s)
    return msgstate

def agent3(msgstate: dict):
    print('state received in agent3 node',msgstate)
    msgstate["message"] = generatePost(msgstate["message"])
    print('final state in agent3 node',msgstate)
    return msgstate

def agent1_next(msgstate: dict) -> Literal["agent2", "agent3"]:
    print("message in agent1_next", msgstate)
    input_prompt = msgstate['message']

    if (len(input_prompt) > 200) & ("linkedin" in input_prompt.lower()):
        print("agent1_next agent3")
        msgstate["flow"] = "agent3"
        return "agent3"
    elif ("search" in input_prompt.lower()) & ("linkedin" in input_prompt.lower()):
        print("agent1_next agent2")
        msgstate["flow"] = "agent3"
        return "agent2"
    elif "search" in input_prompt.lower():
        print("agent1_next agent2")
        msgstate["flow"] = END
        return "agent2"

def agent2_next(msgstate: dict) -> Literal[END, "agent3"]:
    print("message in agent2_next", state)
    return msgstate["flow"]

# Create a new Graph
workflow = Graph()
workflow.add_node("agent1", agent1)
workflow.add_node("agent2", agent2)
workflow.add_node("agent3", agent3)

workflow.add_edge(START, "agent1")
workflow.add_conditional_edges("agent1", agent1_next)
workflow.add_conditional_edges("agent2", agent2_next)
workflow.add_edge("agent3", END)

app = workflow.compile()
state = {"message": "search lion  tiger", "flow": "agent1"}
msg = app.invoke(state)
print("FINAL MESSAGE:\n", msg["message"])


ner = pipeline("ner", grouped_entities=True)
result = ner(msg["message"])
for r in result:
    print(r)

