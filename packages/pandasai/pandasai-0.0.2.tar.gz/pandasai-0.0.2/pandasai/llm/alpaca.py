import requests
from .base import LLM

class Alpaca(LLM):
  max_tokens: int = 512
  temperature: float = 0.1
  top_p: float = 0.75
  top_k: float = 40.0
  beams: int = 4

  def __init__(self, max_tokens: int = None, temperature: float = None, top_p: float = None, top_k: float = None, beams: int = None):
    self.max_tokens = max_tokens or self.max_tokens
    self.temperature = temperature or self.temperature
    self.top_p = top_p or self.top_p
    self.top_k = top_k or self.top_k
    self.beams = beams or self.beams

  def call(self, instruction: str, input: str) -> str:
      response = requests.post("https://tloen-alpaca-lora.hf.space/run/predict", json={
        "data": [
          instruction,
          input,
          self.temperature,
          self.top_p,
          self.top_k,
          self.beams,
          self.max_tokens
        ]
      }).json()
      
      if "error" in response:
        raise Exception("Error while calling Alpaca LLM")

      return response["data"][0]

  @property
  def _type(self) -> str:
      return "alpaca-lora"