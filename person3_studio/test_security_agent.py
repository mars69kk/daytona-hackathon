import os
import sys
import pytest
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from person3_studio.security_agent import SecurityAgent, run_security_and_test_feedback, SecurityFuzzSuite, NosanaAuditEngine


def test_security_fuzz_suite_secret_leaks():
    leaks = SecurityFuzzSuite.audit_logs_for_leaks("Debug log: sk-proj-1234567890abcdef1234567890 and dtn_d38bd713065be40c784172c2650291361e6c1a0705ca069ae86ad0f4da56cb56")
    assert len(leaks) >= 2


def test_nosana_patch_suggestions():
    suggestion = NosanaAuditEngine.generate_patch_suggestions("secret_leakage", "leak logs")
    assert "Mask and sanitize" in suggestion

    suggestion_syntax = NosanaAuditEngine.generate_patch_suggestions("syntax_error", "SyntaxError")
    assert "syntax error" in suggestion_syntax


def test_security_agent_success_flow():
    agent = SecurityAgent(api_key="mock_key")
    # Mock execute_in_sandbox to return success (exit_code 0)
    agent.execute_in_sandbox = MagicMock(side_effect=[
        (0, "compilation successful", ""), # syntax check
        (0, "2 passed in 0.12s", "")       # pytest / run_tests
    ])

    state_payload = {
        "service_name": "GitHubMini",
        "coding_agent_output": {"target_filename": "server.py"},
        "deployment_agent_output": {"daytona_workspace_id": "sb-live-123"},
        "pipeline_routing": {"current_agent": "SecurityAgent", "iteration_count": 0}
    }

    updated = agent.run_security_audit(state_payload)
    assert updated["security_agent_output"]["is_secure"] is True
    assert updated["pipeline_routing"]["current_agent"] == "DeploymentAgent"
    assert updated["feedback_report"]["status"] == "PASS"


def test_security_agent_leak_detection_flow():
    agent = SecurityAgent(api_key="mock_key")
    # Mock execute_in_sandbox: syntax passes, but tests leak an OpenAI token
    agent.execute_in_sandbox = MagicMock(side_effect=[
        (0, "compilation successful", ""),
        (0, "Tool executed. Leaked: sk-proj-abc1234567890123456789012345", "")
    ])

    state_payload = {
        "service_name": "GitHubMini",
        "coding_agent_output": {"target_filename": "server.py"},
        "deployment_agent_output": {"daytona_workspace_id": "sb-live-123"},
        "pipeline_routing": {"current_agent": "SecurityAgent", "iteration_count": 0}
    }

    updated = agent.run_security_audit(state_payload)
    assert updated["security_agent_output"]["is_secure"] is False
    assert updated["pipeline_routing"]["current_agent"] == "CodingAgent"
    assert updated["pipeline_routing"]["iteration_count"] == 1
    assert updated["feedback_report"]["error_category"] == "secret_leakage"
