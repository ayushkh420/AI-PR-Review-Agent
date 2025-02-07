from typing import Dict, List, Optional
from langchain.prompts import ChatPromptTemplate
from langchain.llms.base import BaseLLM

class CodeReviewAgent:
    """
    Agent responsible for code review analysis using LLM.
    """
    
    def __init__(self, llm: BaseLLM):
        """
        Initialize the code review agent.
        
        Args:
            llm (BaseLLM): Language model instance
        """
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code reviewer. Analyze the following code diff and provide detailed feedback on:
            1. Code quality and maintainability
            2. Potential bugs and errors
            3. Performance considerations
            4. Best practices compliance
            
            Focus on providing actionable, specific feedback."""),
            ("human", "{diff}")
        ])

    async def analyze(self, diff: str) -> Dict:
        """
        Analyze code diff and return structured feedback.
        
        Args:
            diff (str): Code diff to analyze
            
        Returns:
            Dict: Analysis results containing issues and suggestions
        """
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"diff": diff})
        
        return self._parse_response(response)

    def _parse_response(self, response) -> Dict:
        """
        Parse LLM response into structured format.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Dict: Structured analysis results
        """
        return {
            "issues": self._extract_issues(response),
            "suggestions": self._extract_suggestions(response),
            "complexity_score": self._calculate_complexity(response)
        }

    def _extract_issues(self, response) -> List[Dict]:
        """Extract code issues from LLM response"""
        try:
            # Basic parsing of LLM response
            issues = []
            lines = response.split('\n')
            current_issue = None
            
            for line in lines:
                if line.startswith('Issue:'):
                    if current_issue:
                        issues.append(current_issue)
                    current_issue = {'description': line[6:].strip()}
                elif line.startswith('Line:') and current_issue:
                    try:
                        current_issue['line'] = int(line[5:].strip())
                    except ValueError:
                        current_issue['line'] = 0
                elif line.startswith('Suggestion:') and current_issue:
                    current_issue['suggestion'] = line[11:].strip()
                    
            if current_issue:
                issues.append(current_issue)
                
            return issues
        except Exception as e:
            print(f"Error parsing issues: {str(e)}")
            return []

    def _extract_suggestions(self, response) -> List[Dict]:
        """
        Extract improvement suggestions from LLM response.
        
        Args:
            response: Raw LLM response
            
        Returns:
            List[Dict]: List of suggestions
        """
        return []

    def _calculate_complexity(self, response) -> int:
        """
        Calculate code complexity score.
        
        Args:
            response: Raw LLM response
            
        Returns:
            int: Complexity score (0-10)
        """
        return 0
