from langgraph.graph import StateGraph, MessagesState, END, START
from model_loader import ModelLoader
from prompt import SYSTEM_PROMPT
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages : Annotated[list, add_messages]
    subject: str


class GraphBuilder():
    def __init__(self, model_provider: str= "groq"):
        self.model_loader = ModelLoader(model_provider = model_provider)
        self.llm = self.model_loader.load_llm()

        self.graph = None
        self.system_prompt = SYSTEM_PROMPT

    def agent_function(self, state: State):
        user_question = state["subject"]
        return {"messages":[self.llm.invoke(f"Write an email about {user_question}")]}
    

    def build_graph(self):
        graph_builder= StateGraph(State)
        graph_builder.add_node("write_email", self.agent_function)
        graph_builder.set_entry_point("write_email")
        self.chain = graph_builder.compile()
        
        return self.chain
    

    def __call__(self):
        return self.build_graph()
    

if __name__ == "__main__":
    graph_builder = GraphBuilder(model_provider="groq")
    graph = graph_builder()
    # print(graph)
    # print("Graph built successfully.")
