import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.config import AVAILABLE_MODELS, DEFAULT_MODEL, REPORTS_DIR
from src.agent import CodeScopeAgent
from src.report import save_report


def print_banner():
    print("\n" + "=" * 60)
    print("\n CodeScope v0.1.0\n")
    print("= " * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="CodeScope - AI-powered code analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py ./my-project
  python main.py ./my-project --model gpt4-mini
  python main.py ./my-project --focus "unused imports" "dead code"
  python main.py --list-models
        """
    )
    
    parser.add_argument(
        "path",
        nargs="?",
        help="Path to the codebase to analyze"
    )
    
    parser.add_argument(
        "--model", "-m",
        choices=list(AVAILABLE_MODELS.keys()),
        default=DEFAULT_MODEL,
        help=f"LLM model to use (default: {DEFAULT_MODEL})"
    )
    
    parser.add_argument(
        "--focus", "-f",
        nargs="+",
        help="Specific areas to focus on"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress banner and progress output"
    )
    
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models and exit"
    )
    
    args = parser.parse_args()
    
    # handle --list-models
    if args.list_models:
        print("Available models:")
        for key, model in AVAILABLE_MODELS.items():
            default = " (default)" if key == DEFAULT_MODEL else ""
            print(f"  {key}: {model}{default}")
        return 0
    
    # require path
    if not args.path:
        parser.error("Please provide a path to analyze")
    
    # validate path
    codebase_path = Path(args.path)
    if not codebase_path.exists():
        print(f"Error: Path does not exist: {codebase_path}")
        return 1
    
    if not codebase_path.is_dir():
        print(f"Error: Path is not a directory: {codebase_path}")
        return 1
    
    # print banner
    if not args.quiet:
        print_banner()
        print(f" Target:  {codebase_path.absolute()}")
        print(f" Model:   {args.model}")
        if args.focus:
            print(f" Focus:   {', '.join(args.focus)}")
        print()
    
    # run analysis
    agent = CodeScopeAgent(model_key=args.model, verbose=not args.quiet)
    results = agent.analyze(str(codebase_path), focus_areas=args.focus)
    
    if not results.get("success"):
        print(f"\n Analysis failed: {results.get('error')}")
        return 1
    
    # save reports to reports dir
    if results.get("report_path"):
        saved = save_report(results["report_path"], codebase_path.name)
        
        print("\n" + "=" * 60)
        print("REPORTS GENERATED")
        print("=" * 60)
        print(f"\n Markdown: {saved.get('markdown')}")
        print(f" HTML:     {saved.get('html')}")
    
    # print summary
    if results.get("summary"):
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"\n{results['summary']}")
    
    print("\n" + "=" * 60)
    print("Remember: Review all findings before making changes!")
    print("=" * 60 + "\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())