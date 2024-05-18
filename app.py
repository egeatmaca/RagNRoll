from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from core.rag import RAG


app = FastAPI()
templates = Jinja2Templates(directory='templates')
static_files = StaticFiles(directory='static')
app.mount('/static', static_files, name='static')

rag = RAG()
rag.semantic_search.inject_documents()

@app.get('/')
def get_index():
    return RedirectResponse(url='/chat')

@app.get('/chat')
def get_chat(request: Request):
    return templates.TemplateResponse('chat.html', context={'request': request})

@app.post('/chat')
async def post_chat(request: Request, prompt: str):
    if not prompt:
        return Response(status_code=400, content="'prompt' parameter should be provided!")
    
    generated_text = rag.generate(prompt)
    if generated_text == '':
        generated_text = "Sorry, I couldn't generate an answer for that. Please try again rephrasing your request."

    return generated_text

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=3000)