import typer
from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL
from langchain.llms.openai import OpenAI
import os

app = typer.Typer()

@app.command()
def pythonagent(temp: int = typer.Option(...), tokens: int = typer.Option(...)):
    """
    function pythonagent():
    
    parameters:
        --temp: temprature of model
        --token: total number of tokens
    
    usage:
        pythonagent --temp 0 --tokens 1024
    
    description:
        This is a toolkit, or an agent applied to a particular use case. The pythonagent is designed to write and execute Python code to answer a question. It will first ask you for your OpenAI API key, and then it will ask you for your question.
    """
    os.environ["OPENAI_API_KEY"] = input("Please enter your OpenAI API key: ")
    agent_executor = create_python_agent(
        llm=OpenAI(temperature=temp, max_tokens=tokens),
        tool=PythonREPLTool(),
        verbose=True
    )
    question = input("Please enter your question: ")
    agent_executor.run(question)

@app.command()
def version():
    """
    Shows the version of the package installed.
    """
    print("0.0.1")