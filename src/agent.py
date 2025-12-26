import os
import aisuite as ai
from aisuite.mcp import MCPClient
from pathlib import Path

from .config import AVAILABLE_MODELS, DEFAULT_MODEL, MAX_TURNS
from .prompts import get_analysis_prompt


class CodeScopeAgent:
    def __init__(self, model_key: str = DEFAULT_MODEL, verbose: bool = True):
        """
        Initialize the CodeScope agent.
        
        Args:
            model_key: Which model to use (claude, gpt4, gpt4-mini, gemini)
            verbose: Whether to print progress messages
        """
        self.model = AVAILABLE_MODELS.get(model_key, AVAILABLE_MODELS[DEFAULT_MODEL])
        self.verbose = verbose
        self.client = ai.Client()
        self.mcp_client = None
        
        if self.verbose:
            print(f"CodeScope initialized with model: {self.model}")
    
    def _log(self, message: str):
        # print message if verbose mode is on
        if self.verbose:
            print(message)
    
    def analyze( self, codebase_path: str, focus_areas: list[str] = None,) -> dict:
        # resolve to absolute path
        codebase_path = str(Path(codebase_path).resolve())
        
        self._log(f"\n{'='*60}")
        self._log(f"Analyzing: {codebase_path}")
        self._log(f"{'='*60}\n")
        
        # initialize MCP filesystem client: gives agent read/write access to target dir
        self._log("Initializing filesystem tools...")
        self.mcp_client = MCPClient(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", codebase_path]
        )
        
        # get available tools from MCP
        tools = self.mcp_client.get_callable_tools()
        self._log(f"✓ {len(tools)} filesystem tools available")
        
        # generate the analysis prompt
        prompt = get_analysis_prompt(codebase_path, focus_areas)
        
        # run the agent
        self._log(f"\n Starting analysis (max {MAX_TURNS} turns)...\n")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                tools=tools,
                max_turns=MAX_TURNS,
            )
            
            # extract the final response
            final_message = response.choices[0].message.content
            
            self._log("\n Analysis complete!")
            
            # check if report was created
            report_path = Path(codebase_path) / "codescope_report.md"
            report_exists = report_path.exists()
            
            if report_exists:
                self._log(f" Report saved: {report_path}")
            
            return {
                "success": True,
                "codebase": codebase_path,
                "model": self.model,
                "report_path": str(report_path) if report_exists else None,
                "summary": final_message,
            }
            
        except Exception as e:
            self._log(f"\n Error during analysis: {e}")
            return {
                "success": False,
                "error": str(e),
                "codebase": codebase_path,
            }
        
        finally:
            # clean up MCP client
            if self.mcp_client:
                self.mcp_client.close()
                self._log("Cleanup complete")
    
# convenience function to analyze a codebase
def analyze_codebase(path: str, model: str = DEFAULT_MODEL, focus_areas: list[str] = None, verbose: bool = True,) -> dict:
    agent = CodeScopeAgent(model_key=model, verbose=verbose)
    return agent.analyze(path, focus_areas=focus_areas)