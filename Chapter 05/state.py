from pydantic import BaseModel, Field


class ResearchState(BaseModel):
    """State definition for the research agent workflow.
    
    This state serves as the single source of truth, carrying all data
    through the workflow. Every node reads from this state and returns
    updates to it.
    """
    query: str = Field(description="The user's research question or search query")
    candidate_urls: list[str] = Field(description="List of URLs identified as potentially relevant sources")
    page_texts: list[str] = Field(description="List of fetched page content from the candidate URLs")
    draft_summary: str = Field(description="Preliminary summary created from the gathered page texts")
    final_report: str = Field(description="The finalized research report compiled from all gathered information")
    errors: list[str] = Field(description="List of error messages encountered during the research workflow")
