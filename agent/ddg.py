from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import  tool
import toml

def Agent(q:str, model:ChatOpenAI, tools:list[tool]):
    model_with_tools = model.bind_tools(tools)
    model_opt = model_with_tools.invoke(q)
    # print(model_opt)
    tool_resp  = call_tool(model_opt, tools)
    final_resp = model.invoke(
        f'original query:{q}\n\n\n  tool response:{tool_resp}',
    )
    return final_resp

def call_tool(model_opt, tools):
    tools_map = {tool.name.lower():tool for tool in tools}
    print(tools_map)
    tools_resp = {}
    for tool in model_opt.tool_calls:
        tool_name = tool['name'].lower()
        tool_args = tool['args']
        tool_instance = tools_map[tool_name]
        tool_resp = tool_instance.invoke(*tool_args.values())
        tools_resp[tool_name] = tool_resp
        print(tool_name, '  ', tool_resp)
    return tools_resp

with open(r".streamlit/secrets.toml", "r") as file:
    config = toml.load(file)

apikey = config.get("kimi_api_key")
model = ChatOpenAI(
    model="moonshot-v1-8k",
    api_key=apikey,
    temperature=0.7,
    base_url="https://api.moonshot.cn/v1",
)
tools = [DuckDuckGoSearchRun()]

res = Agent("今天日期是多少", model, tools)
print(res.content)