from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from model_loader import ModelLoader
from prompt import SYSTEM_PROMPT


class GraphBuilder():
    def __init__(self, model_provider: str= "groq"):
        self.model_loader = ModelLoader(model_provider = model_provider)
        self.llm = self.model_loader.load_llm()

        self.graph = None
        self.system_prompt = SYSTEM_PROMPT

    def agent_function(self, state: MessagesState):
        user_question = state["messages"]
        return {"messages":[self.llm.invoke(f"Write an email about {state['messages']}")]}


    def build_graph(self):
        graph_builder= StateGraph(MessagesState)
        graph_builder.add_node("write_email", self.agent_function)
        graph_builder.set_entry_point("write_email")
        self.chain = graph_builder.compile()
        
        return self.chain
    

    def __call__(self):
        return self.build_graph()
