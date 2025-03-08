from typing_extensions import TypedDict
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_together import ChatTogether

from util import PdfRead

class PDFState(TypedDict):
    pdf_content: str
    outline: str
    structured_outline: str
    podcast_dialog: str

class Agent:
    def __init__(self, model):
        
        self.model = model
        graph = StateGraph(PDFState)
<<<<<<< HEAD
        graph.add_node("outline", self.create_outline)
        graph.add_node("structured_outline", self.create_structured_outline)
        graph.add_node("podcast_dialog", self.generate_podcast_dialog)
        graph.add_edge("structured_outline", END)
        graph.add_edge("outline", "structured_outline")
        graph.add_edge("revision","podcast_dialog")
        graph.compile()
=======
        graph.add_node("create_outline", self.create_outline)
        graph.add_node("create_structured_outline", self.create_structured_outline)
        graph.add_edge("create_structured_outline", END)
        graph.add_edge("create_outline", "create_structured_outline")
        graph.set_entry_point("create_outline")
        self.graph = graph.compile()
>>>>>>> c1fef6bf6320ba67ed4ae6aaf717ed910c73b0f7

    def create_outline(self, state: PDFState):
        print("Creating Outline")
        prompt = f"""
                You are an expert at creating structured outlines based on content.
                Your task is to deeply think about the content understand its meaning and create a high-level structural outline of the Content given below inside the angle brackets.

                Expected Output: A hierarchical outline with main topics and subtopics

                <{state['pdf_content']}>.

                Make sure to only include the high level struture only. Do not include any other data.
            """
        # state['outline'] = self.llm(prompt)
        result = self.llm(prompt)
        print(result)
        return {'outline': result}

    def create_structured_outline(self, state: PDFState):
        prompt = f"""
            You are an expert at transforming basic outlines into an outline suitable for a 2 person conversation.
            Your task is to create a conversation plan between two people based on the outline provided below inside the angle barackets.
            This plan or outline should be very structured and should include,
                1) Introduction
                2) Main Segment
                3) transition
                4) Conclusion
            Expected Output: A conversion plan that organizes content for spoken delivery

            The content: <{state['outline']}>.

        """
        state['structured_outline'] = self.llm(prompt)

    def llm(self, prompt):
        prompt = HumanMessage(prompt)
        return self.model.invoke(prompt)
        
<<<<<<< HEAD
    def generate_podcast_dialog(self, state: PDFState):
        prompt = f"""
                You are an expert in generating podcast scripts, take the given transcript and create a script for the podcast with the conversation being funny, engaging and having a 
                like they are hearing from a friend, keep the language well structured, less formal but should not be completely informal
                it must feel natural. 
                """
=======
def main():
    llm = ChatTogether(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        together_api_key="84e8df9a595039765758ae96105665d37e873e9619a2c209ee31a108db5875ef"
    )
    content = PdfRead("PDF's/dbms.pdf")
    agent = Agent(llm)
    content = HumanMessage(content)
    result = agent.graph.invoke({'pdf_content': content})
    print(result['structured_outline'])


main()
>>>>>>> c1fef6bf6320ba67ed4ae6aaf717ed910c73b0f7
