import functools
from flask import Flask, request, jsonify
import requests

smart_pipes = []

class SmartPipeInstance:
    def __init__(
            self, 
            func=None,
            path=None, 
            method=None, 
            id=None            
      ):
      self.func = func
      self.path = path
      self.method = method
      self.id = id
      self.coprocessors = []        

    def add_coprocessor(self, coprocessor):
        self.coprocessors.append(coprocessor)

def inference(version):
    def model(input_data):
      headers = {
      "Authorization": "Token da392854c77ea7339b9acd8181f8055169bac763"
      }

      payload = {
        "version": version, 
        "input": {
            "width": 256,
            "height": 256,
            "prompt": input_data["prompt"],
            "seed": input_data["seed"]
        }      
      }
      response = requests.post(
          "https://api.replicate.com/v1/predictions",
          json=payload,
          headers=headers,
      )

      if response.ok:
        result = response.json()
        id = result["id"]
        print(id)        

        while not result["output"]:
          endpoint = f"https://api.replicate.com/v1/predictions/{id}"          
          response = requests.get(
              endpoint,              
              headers=headers,
          )

          print("Attempt")
          if response.ok:
            result = response.json()
            print(result["output"])

            if result["output"]:
              return result
      else:
        return response.text 
    
    return model

class Coprocessor:
    def __init__(self, func=None, type=None, model=None, id=None, args=None, kwargs=None):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.type = type
        self.model = model
        self.id = id

    def process(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        if self.model:
            print(f"Coprocessor type '{self.type}' Model ID {self.model}")                
            
            self.args= self.args + (inference(self.model),)

            return self.func(*self.args, **self.kwargs)
        else:            
            print(f"Coprocessor type '{self.type}' ID {self.id}")                
            return self.func(*self.args, **self.kwargs)
        


def smartpipe(_func=None, path=None, method=None, id=None):
    def decorator_smartpipes(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):            
            print(f"SmartPipe Path: {path}, Method: {method}, ID: {id}")            

            result = func(*args, **kwargs)            
            print(f"Something happening after {path}")
            return result

        smart_pipes.append(SmartPipeInstance(func, path, method, id))
        return wrapper

    if not _func:
        return decorator_smartpipes
    else:
        return decorator_smartpipes(_func)

def coprocessor(_func = None, type = None, model = None, id=None):    
    def decorator_coprocessor(func):        
        @functools.wraps(func)        
        def wrapper(*args, **kwargs):            
            print(f"Coprocessor Type: {type}")
            
            result = coprocessor.process(*args, **kwargs)            
            return result

        coprocessor = Coprocessor(func, type, model, id)                    
        smart_pipes[0].add_coprocessor(coprocessor)
        return wrapper
    
    if not _func:        
        return decorator_coprocessor
    else:        
        return decorator_coprocessor(_func)



def start():
    app = Flask(__name__)
        
    for smart_pipe in smart_pipes:        
      def endpoint():
          data = request.get_data()
          result = smart_pipe.func(data)
          return { "result": result }
      
      app.add_url_rule(smart_pipe.path, smart_pipe.id, endpoint, methods=[smart_pipe.method])      

    def health():
      return 'Seaplane SmartPipes Demo'
    app.add_url_rule("/", "health", health, methods=["GET"])
    app.run(debug=True)