import langchain
from langchain import PromptTemplate
from langchain.chains.openai_functions.base import create_structured_output_chain
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser

from config import config
from constants.prompt import PROMPT
from llm_provider.output_parser.code_review_comment_list import CodeReviewCommentList

langchain.verbose = True


class CodeCommentProcessor:

    def __init__(self):
        pass

    @staticmethod
    def generate_comments(file_contents, language, model_name='gpt-4'):
        output_parser = PydanticOutputParser(pydantic_object=CodeReviewCommentList)

        llm = ChatOpenAI(openai_api_key=config.open_ai_api_key, temperature=0, model=model_name)
        prompt_template = PromptTemplate(input_variables=["git_diff_content"], partial_variables={
            "format_instructions": output_parser.get_format_instructions(), "language": language}, template=PROMPT)

        chain = create_structured_output_chain(CodeReviewCommentList, llm, prompt_template)
        output = chain.run(file_contents)
        return output
