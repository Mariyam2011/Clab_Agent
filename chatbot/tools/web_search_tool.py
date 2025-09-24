# from typing import Any, Dict, List, Optional
# import os
# import re
# import requests
# from langchain_core.tools import tool
# from langchain_core.prompts import ChatPromptTemplate
# from pydantic import BaseModel, Field

# from langchain_openai import AzureChatOpenAI
# from langchain_core.runnables import Runnable
# from langchain_core.output_parsers import StrOutputParser


# llm = AzureChatOpenAI(deployment_name="gpt-4o")


# class QueryRewriteInput(BaseModel):
#     raw_query: str = Field(..., description="The raw query to rewrite")
#     context: Optional[str] = Field(None, description="The context to use for the rewrite")


# class WebSearchInput(BaseModel):
#     query: str = Field(..., description="The search query to perform")
#     num_results: int = Field(..., description="The number of results to return")
#     time_window: Optional[str] = Field(None, description="The time window to search within")
#     rewrite: bool = Field(..., description="Whether to rewrite the search query")
#     context: Optional[str] = Field(None, description="The context to use for the search")


# @tool("rewrite_search_query", args_schema=QueryRewriteInput, return_direct=False)
# def rewrite_search_query(raw_query: str, context: Optional[str] = None) -> str:
#     """Rewrite a user search query to be clearer and more specific for web search."""
#     system_instructions = (
#         "You are a query rewriting expert. Improve the user's search query for web search. "
#         "Keep it concise (<= 20 words), unambiguous, and include key entities, constraints, and intent. "
#         "Prefer neutral phrasing, avoid stopwords, avoid quotes unless necessary, and do not add hallucinated facts. "
#         "Return ONLY the rewritten query, no extra text."
#     )

#     prompt = ChatPromptTemplate.from_messages(
#         [
#             ("system", system_instructions),
#             ("human", "Context (optional): {ctx}\n\nOriginal query: {q}\n\nRewritten query:"),
#         ]
#     )
#     chain: Runnable = prompt | llm | StrOutputParser()
#     rewritten = chain.invoke({"ctx": context or "", "q": raw_query})
#     return rewritten.strip()


# def _use_tavily(query: str, num_results: int, time_window: Optional[str]) -> List[Dict[str, Any]]:
#     api_key = os.getenv("TAVILY_API_KEY")
#     if not api_key:
#         return []
#     try:
#         headers = {
#             "Authorization": f"Bearer {api_key}",
#             "Content-Type": "application/json",
#         }
#         payload = {
#             "query": query,
#             "search_depth": "advanced",
#             "max_results": max(1, min(num_results, 10)),
#         }
#         if time_window:
#             payload["time_window"] = time_window
#         resp = requests.post("https://api.tavily.com/search", headers=headers, json=payload, timeout=30)
#         data = resp.json()
#         results = []
#         for item in (data.get("results") or [])[:num_results]:
#             results.append(
#                 {
#                     "title": item.get("title"),
#                     "url": item.get("url"),
#                     "snippet": item.get("content") or item.get("snippet"),
#                     "source": "tavily",
#                 }
#             )
#         return results
#     except Exception:
#         return []


# def perform_web_search(
#     query: str,
#     num_results: int = 5,
#     time_window: Optional[str] = None,
#     rewrite: bool = False,
#     context: Optional[str] = None,
# ) -> Dict[str, Any]:
#     """Search using Tavily with optional LLM rewriting and return metadata + results."""
#     original_query = query
#     final_query = query
#     if rewrite:
#         try:
#             final_query = rewrite_search_query.invoke({"raw_query": query, "context": context})  # type: ignore

#             if isinstance(final_query, dict) and "error" in final_query:
#                 final_query = original_query
#             elif isinstance(final_query, dict) and "rewritten" in final_query:
#                 final_query = final_query.get("rewritten") or original_query
#             elif not isinstance(final_query, str):
#                 final_query = original_query
#         except Exception:
#             final_query = original_query

#     results = _use_tavily(final_query, num_results, time_window)

#     return {
#         "original_query": original_query,
#         "final_query": final_query,
#         "results": results,
#         "count": len(results),
#         "time_window": time_window,
#         "rewrite_applied": bool(rewrite) and final_query != original_query,
#     }


# def _should_use_web(user_text: str) -> bool:
#     text = user_text.lower()

#     triggers = [
#         r"\b(current|latest|recent|today|now|this\s+year|202\d|202[0-9])\b",
#         r"\b(news|update|changes?|deadlines?|rankings?|requirements?)\b",
#         r"\bsearch\b|\bweb\b|\bonline\b",
#     ]

#     for pat in triggers:
#         if re.search(pat, text):
#             return True

#     return False


# @tool("web_search", args_schema=WebSearchInput, return_direct=False)
# def web_search(
#     query: str,
#     num_results: int = 5,
#     time_window: Optional[str] = None,
#     rewrite: bool = False,
#     context: Optional[str] = None,
# ) -> Dict[str, Any]:
#     """Search the web and return metadata + list of sources with title, url, snippet."""
#     payload = perform_web_search(
#         query=query,
#         num_results=num_results,
#         time_window=time_window,
#         rewrite=rewrite,
#         context=context,
#     )
#     return payload
