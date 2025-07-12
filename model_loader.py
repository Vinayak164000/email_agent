import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from config_loader import load_config
from langchain.chat_models import  init_chat_model


class ConfigLoader:
    def __init__(self):
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]
    

class ModelLoader(BaseModel):
    model_provider: Literal["groq"] = "groq"
    config: Optional[ConfigLoader] = Field(default = None, exclude= True)
    
    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        if self.model_provider == "groq":
            print("Loading LLM from Groq..............")
            os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
            llm= init_chat_model("google_genai:gemini-2.0-flash")
        
        return llm