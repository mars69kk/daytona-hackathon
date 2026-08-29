# ⚡ MCP-X
### The Autonomous, Daytona-Powered MCP & Agent Tooling Compiler

> **Built for Daytona HackSprint Singapore (August 2026)**  
> *Transforming the world's REST APIs into verified, enterprise-hardened Model Context Protocol (FastMCP) servers with zero human intervention.*

---

## 🧭 Executive Pitch Overview

```mermaid
flowchart LR
    A["Raw API Specs<br/>(OpenAPI / Swagger / cURL)"] --> B["⚡ MCP-X<br/>(5-Agent Swarm)"]
    B <--> C["⚡ Daytona Cloud<br/>(Isolated Sandboxes)"]
    B --> D["Verified FastMCP Bundle<br/>(server.py + Claude Config)"]
```

---

# 🔴 Part 1: THE "WHY"
### *The Bottleneck in the AI Agent Revolution*

### 1. The MCP Era Has Arrived
The **Model Context Protocol (MCP)** pioneered by Anthropic has become the universal standard connecting LLMs and AI Agents (Claude Desktop, Cursor, Antigravity) to real-world software and enterprise data.

### 2. The Multi-Billion Dollar Friction Point
There are millions of production REST APIs across global enterprise systems. However, bridging a REST API to an enterprise-grade MCP server currently requires:
- **Painstaking Manual Engineering:** Days spent crafting parameter definitions, Pydantic type schemas, and async client plumbing.
- **Critical Security & Secret Exposure:** Hand-rolled MCP servers frequently leak API keys, authorization headers, and sensitive environment tokens directly into LLM context prompts.
- **The Execution Danger Zone:** Testing newly synthesized server code locally risks system pollution, dependency conflicts, or accidental credential exfiltration.

### 3. The Vision
**What if you could drop in any raw API specification or cURL snippet, and within seconds receive a verified, security-hardened FastMCP server that has already been deployed, tested, and self-healed inside an isolated cloud sandbox?**

---

# 🟢 Part 2: THE "WHAT"
### *Meet MCP-X: The Autonomous MCP Compiler*

**MCP-X** is an autonomous multi-agent compilation and verification platform. It automates the entire lifecycle of Model Context Protocol generation with zero human code writing required.

### 🎯 Key Product Capabilities

| Pillar | Capability | Impact |
| :--- | :--- | :--- |
| 📥 **Universal Ingestion** | Ingests OpenAPI 3.0 (JSON/YAML), Swagger 2.0, and raw cURL snippets. | Instant compatibility with 99% of web APIs out of the box. |
| 🛡️ **Enterprise Hardening** | Auto-injects token sanitization (`_sanitize_output`) and Pydantic validation. | Complete prevention of credential leaks into LLM context windows. |
| ⚡ **Daytona-Native Sandboxing** | Ephemeral, isolated Daytona Sandbox provisioning for test runs. | 100% safe code execution without polluting local environments. |
| 🔄 **Autonomous Self-Healing** | Real-time diagnostic parsing and feedback loop that auto-patches code. | Zero-touch recovery from runtime errors and signature mismatches. |
| 📦 **1-Click Client Integration** | Generates `claude_desktop_config.json` alongside `server.py`. | Ready to drop into Claude Desktop, Cursor, or Antigravity instantly. |

### 📦 The Output Artifacts (Enterprise MCP Bundle)
1. **`server.py`**: Production-ready FastMCP server implementing all endpoints as callable tools.
2. **`claude_desktop_config.json`**: Pre-configured desktop agent connection file.
3. **`test_protocol.json`**: Synthesized matrix of functional test cases.
4. **`run_tests.py`**: Autonomous test runner executed inside the Daytona sandbox.
5. **`test_report.json`**: Verified sandbox test execution scorecard with latency and status metrics.

---

# 🔵 Part 3: THE "HOW"
### *Multi-Agent Swarm Architecture & Daytona Engine*

MCP-X operates via an orchestrated 5-agent pipeline communicating across strict data contracts, with **Daytona Cloud Sandboxes** serving as the core execution and verification engine.

### 🏗️ End-to-End System Architecture

```mermaid
flowchart TD
    %% Styling
    classDef p1 fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:#ffffff;
    classDef p2 fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#ffffff;
    classDef p3 fill:#701a75,stroke:#d946ef,stroke-width:2px,color:#ffffff;
    classDef orch fill:#111827,stroke:#6366f1,stroke-width:2px,color:#ffffff;
    classDef sand fill:#064e3b,stroke:#10b981,stroke-width:2px,stroke-dasharray: 5 5,color:#ffffff;

    subgraph UI ["🖥️ Web Studio (person3_studio/app.py)"]
        SpecInput["1. Raw API Spec Ingestion (OpenAPI / Swagger / cURL)"]
        LiveDashboard["6. Live Streamlit Studio & 1-Click Artifact Downloads"]
    end

    subgraph Orchestrator ["⚡ Master Orchestrator (orchestrator.py)"]
        Loop["Autonomous Multi-Agent Controller & Healing Router"]
    end

    subgraph Compiler ["⚙️ Ingestion & Planner Engine (person1_compiler/)"]
        Agent1["🧠 Agent 1: Planner Agent (Schema Planning & Fallback)"]
        Agent2["💻 Agent 2: Coder Agent (FastMCP & Test Suite Synthesis)"]
        Healer["🔄 Self-Healing Patch Engine"]
        Bench["📊 Benchmark & Quality Evaluator"]
    end

    subgraph DaytonaEngine ["🚀 Daytona Deployment Engine (deployment_stage/)"]
        Agent3["🚀 Agent 3: Deployer Agent (Daytona SDK Provisioning)"]
        Agent4["🧪 Agent 4: Tester Agent (Functional Sandbox Driver)"]
    end

    subgraph Sandbox ["⚡ Isolated Daytona Sandbox Workspace"]
        ServerRun["⚙️ Running FastMCP Server (server.py)"]
        TestRun["🧪 Test Suite Execution (run_tests.py)"]
    end

    SpecInput --> Loop
    Loop --> Agent1 --> Agent2
    Agent2 -->|"MCPBundle (server.py, run_tests.py)"| Agent3
    Agent3 -->|"Mount Workspace & Inject Env Vars"| Sandbox
    Sandbox --> ServerRun & TestRun
    TestRun --> Agent4
    Agent4 -->|"❌ Runtime Failure"| Healer --> Agent2
    Agent4 -->|"✅ All Tests Passed"| Bench
    Bench --> LiveDashboard

    class SpecInput,LiveDashboard p3;
    class Loop orch;
    class Agent1,Agent2,Healer,Bench p1;
    class Agent3,Agent4 p2;
    class ServerRun,TestRun sand;
```

---

### ⚡ Why Daytona is the Secret Weapon

Daytona makes autonomous multi-agent code generation viable for production:
1. **Isolated Execution Guarantee:** AI-generated server scripts run in sandboxed Daytona micro-environments, eliminating risk to host machines.
2. **Ephemeral Lifecycle:** Sandboxes are spun up on-demand, mounted with code bundles and test suites, validated, and safely torn down.
3. **Environment Parity:** Daytona ensures that dependency resolution (`requirements.txt`), Python runtime versions, and environment variables are tested under real cloud conditions.

---

### 🔄 The Self-Healing Feedback Loop in Action

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Web Studio
    participant Orch as Master Orchestrator
    participant Coder as Agent 2 (Coder)
    participant Daytona as Daytona Sandbox
    participant Tester as Agent 4 (Tester)
    participant Healer as Self-Healing Engine

    User->>Orch: Submit Raw API Spec
    Orch->>Coder: Generate Initial MCP Server & Test Harness
    Coder->>Daytona: Provision Sandbox & Mount Files
    Daytona->>Tester: Execute run_tests.py
    alt Tests Encounter Error / Crash
        Tester->>Healer: Emit Diagnostic FeedbackReport (Stderr, Traceback)
        Healer->>Coder: Formulate Remediation Patch
        Coder->>Daytona: Re-deploy Patched server.py
        Daytona->>Tester: Re-verify Tool Execution
    end
    Tester->>Orch: ✅ Verification Passed (0 Errors)
    Orch->>User: Deliver Verified FastMCP Bundle & Claude Config
```

---

# 🚀 Live Demo & Quickstart

### 1. Quick Setup
```bash
git clone https://github.com/Nischit290402/daytona-hackathon.git
cd daytona-hackathon

# Create & activate environment
python -m venv daytona
.\daytona\Scripts\activate      # Windows
source daytona/bin/activate     # Linux / macOS

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch the Web Studio
```bash
streamlit run person3_studio/app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser:
1. Select the **GitHub Issues & Repositories API (Showcase)** preset.
2. Click **🚀 Compile, Deploy & Verify in Daytona**.
3. Watch the live multi-agent pipeline stream in real time.
4. Download the verified **`server.py`** and **`claude_desktop_config.json`**.

### 3. Run via CLI Orchestrator
```bash
python orchestrator.py
```

---

## 👥 Team & Architecture Separation

- **👤 Person 1 (Compiler & Self-Healing Core):** Multi-Spec Ingestion, Planner Agent (Agent 1), Coder Agent (Agent 2), Self-Healing Patch Loop, Benchmark Evaluator (`person1_compiler/`).
- **👤 Person 2 (Daytona Cloud Runtime):** Daytona Deployer Agent (Agent 3), Daytona Tester Agent (Agent 4), Sandbox Workspace Manager (`deployment_stage/`).
- **👤 Person 3 (Web Studio UI):** Streamlit Web Studio, Showcase Presets, Live Multi-Agent Event Streamer (`person3_studio/`).
- **🔄 Master Orchestrator:** End-to-end pipeline coordination and feedback routing (`orchestrator.py`).
