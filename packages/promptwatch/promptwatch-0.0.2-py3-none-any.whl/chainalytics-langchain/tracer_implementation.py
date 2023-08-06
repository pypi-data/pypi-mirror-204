"""A Tracer implementation that records to LangChain endpoint."""
from __future__ import annotations
import inspect
import logging
import os
from abc import ABC
from typing import Any, Dict, Optional, Union
from uuid import uuid4
import requests
import datetime
from langchain.callbacks.tracers.base import BaseTracer
from langchain.prompts.base import BasePromptTemplate
from langchain.callbacks.tracers.schemas import (
    ChainRun,
    LLMRun,
    ToolRun,
    TracerSession,
    TracerSessionCreate,
)
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks import BaseCallbackHandler, get_callback_manager
from langchain.agents import  AgentExecutor
from langchain.schema import AgentAction, AgentFinish, LLMResult, BaseRetriever, Document

from .data_model import Session, ActivityBase, LlmPrompt, ParallelPrompt, ChainSequence, Log, Answer, Action, Question, RetrievedDocuments, DocumentSnippet
from .repository import Client

from typing import List, Dict

        
def _find_the_caller_in_the_stack(name):
        caller_frame = inspect.currentframe().f_back
        while caller_frame:
            caller_locals = caller_frame.f_locals
            caller_instance = caller_locals.get("self", None)
            if name==caller_instance.__class__.__name__:
                return caller_instance
            caller_frame = caller_frame.f_back

class SessionTracker():

    def __init__(self, session_id:Optional[str]=None):
        self.tracer=BlipTracer(session_id)
        self.callback_manager=get_callback_manager()
 
        


    def __enter__(self):
        self.callback_manager.set_handler(self.tracer)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tracer.end_session()
        self.callback_manager.remove_handler(self.tracer)

    def log(self, text:str, metadata:Optional[Dict[str,Any]]=None):
        self.tracer._add_activity(Log(self.tracer.current_session, text=text, metadata=metadata))
        


class BlipTracer(BaseCallbackHandler, ABC):
    """An implementation of the SharedTracer that POSTS to the langchain endpoint."""

    def __init__(self, api_key:Optional[str]=None, session_id:Optional[str]=None) -> None:
        super().__init__()
        if not api_key:
            api_key=os.environ.get("blip-api-key")
        self.session_repository = Client(api_key=api_key)
        self.current_llm_chain:Optional[LLMChain]=None
        
        if session_id:
            self.current_session = self.session_repository.get_session(session_id)
        else:
            self.current_session = Session(id=session_id or str(uuid4()))
        self.chain_hierarchy=[]
        self.pending_stack=[]
        self.tracing_handlers={}
        #we keep these in order to reverse
        self.monkey_patched_functions=[]

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True
    
    @property
    def current_activity(self) -> ActivityBase:
        if self.chain_hierarchy:
            return self.chain_hierarchy[-1]
        

    def reverse_monkey_patches(self):
        for func in self.monkey_patched_functions:
            pass
            #func.__original_implementation

    def _open_activity(self, activity:ActivityBase):
        if not self.current_session.start_time:
            self.start_session()
        if self.current_activity:
            if isinstance(self.current_activity,ChainSequence) or isinstance(self.current_activity,Action):
                activity.parent_activity_id=self.current_activity.id
            else:
                activity.parent_activity_id=self.current_activity.parent_activity_id
    
        self.pending_stack.append(activity)
        self.chain_hierarchy.append(activity)
        
    

    def _add_activity(self, activity:ActivityBase):
        
        activity.end_time=datetime.datetime.now(tz=datetime.timezone.utc)
        if self.current_activity:
            if isinstance(self.current_activity,ChainSequence):
                activity.parent_activity_id=self.current_activity.id
            else:
                activity.parent_activity_id=self.current_activity.parent_activity_id
        self.pending_stack.append(activity)
        
        
        
    
    def _close_current_activity(self):
        self.current_activity.end_time=datetime.datetime.now(tz=datetime.timezone.utc)
        if self.chain_hierarchy and self.current_activity==self.current_activity:
            closing_chain = self.chain_hierarchy.pop()
            closing_chain.end_time = datetime.datetime.now(tz=datetime.timezone.utc)
            if closing_chain not in self.pending_stack:
                self.pending_stack.append(closing_chain)
        self._flush_stack()

    def _flush_stack(self):
        if self.pending_stack:
            self.session_repository.save_activities(self.current_session.id, self.pending_stack)
            for activity in self.pending_stack:
                if activity.end_time:
                    self.pending_stack.remove(activity)


    def start_session(self):
        self.current_session.start_time=self.current_session.start_time or datetime.datetime.now(tz=datetime.timezone.utc)
        self.session_repository.save_session(self.current_session)

    def end_session(self):
        self.current_session.end_time=datetime.datetime.now(tz=datetime.timezone.utc)
        self._flush_stack()
        self.session_repository.save_session(self.current_session)

    def _on_error(self, error, kwargs):
        self.current_activity.error=str(error)
        self.current_activity.metadata["error_kwargs"]=kwargs
        self.current_session.is_error=True
        self._close_current_activity()



    def _try_to_deconstruct_prompt(self, promptTemplate:BasePromptTemplate):
        input_variables_names = promptTemplate.input_variables
        input_variables={}
        if promptTemplate.input_variables:
            input_variables = {input_variable_name:self.current_activity.inputs[input_variable_name] for input_variable_name in input_variables_names}
        template = promptTemplate.template if hasattr(promptTemplate,"template") else None
        return template, input_variables

    
    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""

        prompt_template = None
        prompt_input_param = None
        if self.current_llm_chain:
            prompt_template, prompt_input_params = self._try_to_deconstruct_prompt(self.current_llm_chain.prompt)
            

        if len(prompts)==1:
            
            self._open_activity(LlmPrompt(
                self.current_session,
                prompt=prompts[0], #why we have here more than one prompt?
                prompt_template=prompt_template,
                prompt_input_params=prompt_input_params,
                metadata={**serialized,**kwargs} if serialized and kwargs else (serialized or kwargs)
                ))
        elif len(prompts)>1:
            thoughts = []
            for prompt in prompts:
                thoughts.append( LlmPrompt(
                            self.current_session,
                            prompt=prompt, #why we have here more than one prompt?
                            prompt_template=prompt_template,
                            prompt_input_params=prompt_input_params,
                        ))
            self._open_activity(ParallelPrompt(
                self.current_session,
                    thoughts=thoughts,
                    metadata={**serialized,**kwargs} if serialized and kwargs else (serialized or kwargs),
                    order=self.current_session.steps_count+1, 
                    session_id=self.current_session.id,
                )
            )


    
    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""
        pass

    
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        if len(response.generations)>1:
            thoughts =  self.current_activity.thoughts
        else:
            thoughts=[self.current_activity]
        
        if not self.current_activity.metadata:
            self.current_activity.metadata={}

        for thought, generated_responses in zip(thoughts, response.generations):
            thought.though = "--- OR ---".join([resp.text for resp in generated_responses])
            thought.metadata["generation_info"] = [resp.generation_info for resp in generated_responses]

        if response.llm_output is not None:
            self.current_activity.metadata["llm_output"]=response.llm_output
            if "token_usage" in response.llm_output:
                token_usage = response.llm_output["token_usage"]
                if "total_tokens" in token_usage:
                    self.current_activity.metadata["total_tokens"] = self.current_activity.metadata.get("total_tokens",0)+ token_usage["total_tokens"]
        self._close_current_activity()

        

    
    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when LLM errors."""
        self._on_error(error, kwargs)

    
    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        """Run when chain starts running."""
        
        if serialized.get("name").startswith("LLM") :
            self.current_llm_chain = _find_the_caller_in_the_stack(serialized["name"])

            if (self.current_llm_chain.prompt.template.startswith("Given an input question, first create a syntactically correct")):
                self.current_llm_chain.prompt=PromptTemplate(
                    input_variables=self.current_llm_chain.prompt.input_variables,
                    template=
"""Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer. Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most {top_k} results. You can order the results by a relevant column to return the most interesting examples in the database.

Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.

Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the tables listed below.

{table_info}

Context:
Today is 31.3.2016

Example:
Question: What data are in table table_1 for last 2 months:
SQLQuery: select sum(column_1), avg(column_1) , sum(column_2), avg(column_2) form table_1 where date > date('now', '-2 month')

Question: {input}"""
                )
        if serialized.get("name")=="RetrievalQA":
            retrieval_qa_chain = _find_the_caller_in_the_stack(serialized["name"])
            
            retriever:BaseRetriever = retrieval_qa_chain.retriever
            if hasattr(retriever.get_relevant_documents,"__original_implementation"):
                wrapped_func=retriever.get_relevant_documents
            else:
                tracing_key= "handle_retriever"
                wrapped_func = _build_wrapped_function(self,  retriever, tracing_key, retriever.get_relevant_documents)
                
                self.monkey_patched_functions.append(wrapped_func)
                #monkey patching the retriever with our wrapped implementation of get_relevant_documents to get track the retrieval
                self.tracing_handlers[tracing_key] = self.handle_get_relevant_documents
                retriever.__dict__[retriever.get_relevant_documents.__name__] = wrapped_func

            


        

        # input is "agent" question key
        # question is for qa_chain
        # query is for RetrievalAQ chain
        question = inputs.get("question") or inputs.get("query")  or inputs.get("input") 
        if  question and self.current_session.steps_count==0:
            self._add_activity(Question(self.current_session,text=question))
        if not self.current_session.session_name:
            self.current_session.session_name=question
            if not self.current_session.start_time:
                self.current_session.start_time=datetime.datetime.now(tz=datetime.timezone.utc)
            self.session_repository.save_session(self.current_session)

        current_chain=ChainSequence(
                self.current_session,
                inputs=inputs,
                metadata={},
                sequence_type=serialized.get("name") or "others"
            )
                                     
        if kwargs:
            current_chain.metadata["input_kwargs"]=kwargs
        self._open_activity(current_chain)
        

    def _trace_function_call(self, handler_key:str, function_name:str, args, kwargs, result):
        handler = self.tracing_handlers.get(handler_key)
        if handler:
            handler(function_name, args, kwargs, result)
        
    def handle_get_relevant_documents(self,function_name:str, args, kwargs, result:List[Document]):
        docs=[]
        for doc in result:
            metadata = {key:val for key,val in doc.metadata.items() if key!="source"}  if doc.metadata else None
            source = doc.metadata.get("source") if doc.metadata else None
            docs.append(DocumentSnippet(
                text=doc.page_content, 
                source=source,
                metadata=metadata if metadata else None # to not pass empty objects
                ))
        
        self._add_activity(RetrievedDocuments(self.current_session,
                                              documents=docs
                                              ))
        
        

    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running."""
        
        if self.current_llm_chain:
            self.current_llm_chain =None
            
        self.current_activity.outputs=outputs
        if kwargs:
            self.current_activity.metadata["output_kwargs"]=kwargs
        
        if "total_tokens" in self.current_activity.metadata and len(self.chain_hierarchy)>1:
            parent_activity = self.chain_hierarchy[-2]
            if not parent_activity.metadata:
                parent_activity.metadata={"total_tokens":self.current_activity.metadata["total_tokens"]}
            else:
                parent_activity.metadata["total_tokens"] = parent_activity.metadata.get("total_tokens",0)+ self.current_activity.metadata["total_tokens"]
        
        self._close_current_activity()

    
    def on_chain_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when chain errors."""
        self._on_error(error, kwargs)

    
    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Run when tool starts running."""
        self._open_activity(
                Action(self.current_session, tool_type=serialized.get("name") or "undefined", input=input_str, input_data=kwargs)
            )

    
    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        """Run when tool ends running."""
        self.current_activity.output=output
        self.current_activity.output_data=kwargs
        self._close_current_activity()


        
    

    
    def on_tool_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when tool errors."""
        self._on_error(error, kwargs)

    
    def on_text(self, text: str, **kwargs: Any) -> Any:
        """Run on arbitrary text."""
        pass

    
    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""
        
        pass
        



    
    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        """Run on agent end."""
        answer_text = finish[0].get("output")
        answer_activity = Answer(self.current_session, text=answer_text)
        self._add_activity(answer_activity)
        answer_activity.parent_activity_id=None #the answer
        if finish.return_values:
            answer_activity.metadata["outputs"]:finish.return_values
        
        



def _build_wrapped_function(tracer:BlipTracer, instance,  handler_key:str, original_function):
    import types
    def wrapped(*args,**kwargs):
        try:
            #we skip the first param, since it is bounded... 
            result = original_function(*args[1:],**kwargs)
        except Exception as ex:
            tracer._trace_function_call(handler_key, original_function.__name__, args=args, kwargs=kwargs, result=ex)
            raise ex
        tracer._trace_function_call(handler_key, original_function.__name__, args=args, kwargs=kwargs, result=result)
        return result
    wrapped.__original_implementation=original_function
    wrapped = types.MethodType(wrapped, instance)
    return wrapped