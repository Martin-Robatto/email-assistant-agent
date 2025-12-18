#!/bin/bash
# Email Assistant Test Runner

set -e  # Exit on error

echo "=================================="
echo "Email Assistant Test Suite"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${YELLOW}Warning: pytest not found. Install with: pip install pytest${NC}"
    exit 1
fi

# Function to run tests
run_test_suite() {
    local name=$1
    local path=$2
    local suite_name=$3
    
    echo -e "${BLUE}Running: ${name}${NC}"
    echo "----------------------------------------"
    
    if [ -n "$suite_name" ]; then
        LANGSMITH_TEST_SUITE="$suite_name" pytest "$path" -v
    else
        pytest "$path" -v
    fi
    
    echo ""
}

# Parse command line arguments
case "${1:-all}" in
    "triage")
        echo "Running triage classification tests..."
        run_test_suite "Triage Tests" \
            "email_assistant/tests/test_triage.py" \
            "Email Assistant: Triage Tests"
        ;;
    
    "agent")
        echo "Running agent behavior tests..."
        run_test_suite "Agent Tests" \
            "email_assistant/tests/test_agent.py" \
            "Email Assistant: Agent Tests"
        ;;
    
    "quick")
        echo "Running quick tests (no LangSmith logging)..."
        pytest email_assistant/tests/ -v -m "not langsmith"
        ;;
    
    "all")
        echo "Running all tests with LangSmith logging..."
        echo ""
        
        run_test_suite "1. Triage Classification Tests" \
            "email_assistant/tests/test_triage.py" \
            "Email Assistant: Triage Tests"
        
        run_test_suite "2. Agent Behavior Tests" \
            "email_assistant/tests/test_agent.py" \
            "Email Assistant: Agent Tests"
        
        echo -e "${GREEN}✓ All test suites completed!${NC}"
        ;;
    
    "help"|"-h"|"--help")
        echo "Usage: ./scripts/run_tests.sh [OPTION]"
        echo ""
        echo "Options:"
        echo "  all      Run all test suites (default)"
        echo "  triage   Run only triage classification tests"
        echo "  agent    Run only agent behavior tests"
        echo "  quick    Run tests without LangSmith logging"
        echo "  help     Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./scripts/run_tests.sh          # Run all tests"
        echo "  ./scripts/run_tests.sh triage   # Run triage tests only"
        echo "  ./scripts/run_tests.sh quick    # Quick test run"
        echo ""
        echo "Environment Variables:"
        echo "  LANGSMITH_API_KEY    Your LangSmith API key for logging"
        echo ""
        exit 0
        ;;
    
    *)
        echo -e "${YELLOW}Unknown option: $1${NC}"
        echo "Run './scripts/run_tests.sh help' for usage information"
        exit 1
        ;;
esac

echo ""
echo "=================================="
echo -e "${GREEN}Tests Complete!${NC}"
echo "=================================="

if [ -n "$LANGSMITH_API_KEY" ]; then
    echo "View results in LangSmith UI: https://smith.langchain.com"
else
    echo -e "${YELLOW}Tip: Set LANGSMITH_API_KEY to log results to LangSmith${NC}"
fi