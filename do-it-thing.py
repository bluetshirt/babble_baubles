from fastapi import FastAPI
import grottify
import ggpt
import os

os.system("")

app = FastAPI()

@app.get("/songs/like/{query}")
def like_song(query):
    return {"result":grottify.like(query)}

@app.get("/songs/enqueue/{query}")
def enqueue_song(query):
    return {"result":grottify.enqueue(query)}

@app.get("/gpt/top_k/{val}")
def top_k(val):
    return {"result":ggpt.top_k(val)}        

@app.get("/gpt/top_p/{val}")
def top_p(val):
    return {"result":ggpt.top_p(val)}        
        
@app.get("/gpt/{prompt}")
def gpt(prompt):
    return {"result":ggpt.gpt(prompt)}
    
    

