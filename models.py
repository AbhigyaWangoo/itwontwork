"""
Models for the LLMs.

"""

DO_TEMPURATURE = False
TEMPURATURE = 0.0
OLLAMA_TIMEOUT = 600

class ModelOllama:
    "Load the Ollama llama2:7b LLM"
    models = {
        "2": "llama2",
        "zephyr": "zephyr",
        "3": "llama3:instruct", # "lama3:8b-instruct-q5_1",
        "mistral": "mistral:instruct",
    }
    default_key = "zephyr"

    def load(self, key=None):
        from llama_index.llms.ollama import Ollama
        default_model = self.models[self.default_key]
        model = self.models.get(key, default_model)
        if DO_TEMPURATURE:
            llm = Ollama(model=model, request_timeout=OLLAMA_TIMEOUT, temperature=TEMPURATURE)
        else:
            llm = Ollama(model=model, request_timeout=OLLAMA_TIMEOUT)
        return llm, model

class ModelGemini:
    models = {"pro": "models/gemini-1.5-pro-latest"}
    default_key = "pro"

    def load(self, key=None):
        "Load the Gemini LLM. I found models/gemini-1.5-pro-latest with explore_gemini.py. "
        from llama_index.llms.gemini import Gemini
        default_model = self.models[self.default_key]
        model = self.models.get(key, default_model)
        if DO_TEMPURATURE:
            return Gemini(model_name=model, temperature=TEMPURATURE), "Gemini"
        else:
            return Gemini(model_name=model, request_timeout=10_000), "Gemini"

class ModelClaude:
    models = {
        "haiku": "claude-3-haiku-20240307",
        "sonnet": "claude-3-5-sonnet-20240620",
        "opus": "claude-3-opus-20240229",
    }
    default_key = "sonnet"

    def load(self, key=None):
        "Load the Claude (Haiku | Sonnet | Opus) LLM."
        from llama_index.llms.anthropic import Anthropic
        default_model = self.models[self.default_key]
        model = self.models.get(key, default_model)
        if DO_TEMPURATURE:
            llm = Anthropic(model=model, max_tokens=4024, temperature=TEMPURATURE)
        else:
            llm = Anthropic(model=model, max_tokens=4024)
        # Settings.llm = llm
        return llm, model

class ModelOpenAI:
    models = {"openai": "openai"}
    default_key = "openai"

    def load(self, key=None):
        "Load the OpenAI GPT-3 LLM."

        if not key:
            key = self.default_key
        
        from llama_index.llms.openai import OpenAI
        
        default_model = self.models[self.default_key]
        model = self.models.get(key, default_model)
        
        if DO_TEMPURATURE:
            llm = OpenAI(model="o1-mini", temperature=TEMPURATURE)
        else:
            llm = OpenAI(model="o1-mini")

        return llm, model

LLM_MODELS = {
    "llama":  ModelOllama,
    "gemini": ModelGemini,
    "claude": ModelClaude,
    "openai": ModelOpenAI,
}

def sub_models(key):
    "Return the submodels of the specified model."
    model = LLM_MODELS[key]
    return  f"{key}: ({' | '.join(model.models.keys())})"

# https://huggingface.co/Snowflake/snowflake-arctic-embed-m
EMBEDDING_NAME = "Snowflake/snowflake-arctic-embed-m"

def set_best_embedding():
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.core.settings import Settings

    embed_model = HuggingFaceEmbedding(
            model_name=EMBEDDING_NAME,
            trust_remote_code=True
        )
    Settings.embedding = embed_model
