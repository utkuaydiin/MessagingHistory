from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

model = ChatOpenAI(model="gpt-3.5-turbo")

store = {}


def get_session_history(session_id : str) -> BaseChatMessageHistory:  #string alır geriye BaseChatMessageHistory dödürür
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Answer all of the questions to the best of your ability"),
        MessagesPlaceholder(variable_name="messages")
    ]
)


chain = prompt | model
config = {"configurable" : {"session_id" : "abcde123"}}
with_message_history = RunnableWithMessageHistory(chain, get_session_history)

#if __name__ == '__main__':
#    messages = [
#        HumanMessage(content="Hello, my name is Utku"),
#        AIMessage(content = "Hello Utku, nice to meet you! How can I assist you today?"),
#        HumanMessage(content = "What is my name ? "),
#    ]
#    response = model.invoke(messages)
#    print(response.content)

if __name__ == '__main__':
    while True:
        user_input = input("\n>")
        for r in with_message_history.stream(
            [
                HumanMessage(content=user_input)
            ],
            config=config,
        ):
            print(r.content, end="")
