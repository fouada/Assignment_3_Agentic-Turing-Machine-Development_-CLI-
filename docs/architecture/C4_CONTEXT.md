# C4 Model - Context Diagram
## Agentic Turing Machine System

**Level:** 1 - System Context  
**Audience:** Technical and non-technical stakeholders  
**Purpose:** Show how the Agentic Turing Machine fits into the wider ecosystem

---

## Context Diagram

```mermaid
C4Context
    title System Context Diagram - Agentic Turing Machine

    Person(researcher, "Researcher", "Studies semantic drift and translation quality")
    Person(developer, "Developer", "Extends system with new skills and features")
    
    System(atm, "Agentic Turing Machine", "Multi-agent translation system that performs sequential translations and analyzes semantic drift")
    
    System_Ext(claude_api, "Anthropic Claude API", "Provides AI agents for translation tasks")
    System_Ext(file_system, "File System", "Stores configurations, skills, results, and logs")
    
    Rel(researcher, atm, "Runs experiments, analyzes results", "CLI")
    Rel(developer, atm, "Adds skills, configures", "File editing")
    
    Rel(atm, claude_api, "Invokes agents for translation", "HTTPS/REST API")
    Rel(atm, file_system, "Reads skills, writes results", "File I/O")
    
    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

---

## System Description

### Agentic Turing Machine
A Python-based multi-agent translation system that:
- Performs sequential translations through multiple language pairs
- Injects controlled noise to simulate real-world text imperfections
- Analyzes semantic drift using multiple similarity metrics
- Tracks API costs and provides comprehensive logging
- Supports extensible skill-based agent architecture

### Key Characteristics
- **Type:** Command-line application
- **Language:** Python 3.8+
- **Deployment:** Local execution
- **Scale:** Single-user, research-oriented

---

## External Systems

### 1. Anthropic Claude API
**Purpose:** Provides large language model capabilities for translation tasks

**Interaction:**
- System sends translation requests with context from skills
- Claude processes text and returns translations
- API tracks token usage for cost calculation

**Key Points:**
- Requires API key authentication
- Subject to rate limits based on tier
- Costs vary by model (Sonnet, Opus, Haiku)
- Typical latency: 2-10 seconds per request

---

### 2. File System
**Purpose:** Persistent storage for all system data

**Interaction:**
- **Read:** Skills, configuration, input data
- **Write:** Translation outputs, analysis results, logs, cost reports

**Key Points:**
- No database required
- Directory-based organization
- JSON and text file formats
- Local storage only

---

## User Personas

### Researcher
**Goals:**
- Conduct systematic experiments on translation quality
- Measure semantic drift across different noise levels
- Analyze cost-performance tradeoffs
- Generate academic-quality results

**Interactions:**
- Runs pipeline with various configurations
- Analyzes results using provided tools
- Reviews Jupyter notebooks with statistical analysis
- Exports data for further research

**Technical Level:** Intermediate - comfortable with CLI and Python

---

### Developer
**Goals:**
- Extend system with new translation skills
- Add new analysis metrics
- Integrate additional language pairs
- Customize pipeline behavior

**Interactions:**
- Creates new skill markdown files
- Modifies configuration files
- Extends core modules
- Writes additional tests

**Technical Level:** Advanced - proficient in Python development

---

## Key Scenarios

### Scenario 1: Run Translation Experiment
```
Researcher → CLI Command → ATM → Claude API → Translation
         ↓
    Analysis → Results JSON + Visualizations
```

### Scenario 2: Analyze Existing Results
```
Researcher → Analysis Script → ATM → File System → Results
         ↓
    Statistical Analysis + Graphs
```

### Scenario 3: Add New Translation Skill
```
Developer → Create SKILL.md → File System
         ↓
    ATM loads skill → Tests with test_agent.py
```

---

## System Boundaries

### Inside the System
✅ Translation pipeline orchestration  
✅ Noise injection logic  
✅ Semantic drift analysis  
✅ Cost tracking and reporting  
✅ Logging and error handling  
✅ Configuration management  

### Outside the System
❌ Actual AI translation (delegated to Claude)  
❌ Cloud infrastructure  
❌ User authentication  
❌ Web interface  
❌ Database management  
❌ Real-time collaboration  

---

## Technology Context

```mermaid
graph TB
    subgraph "Development Environment"
        A[Python 3.8+]
        B[pytest]
        C[WSL/Linux]
    end
    
    subgraph "Runtime Dependencies"
        D[Anthropic SDK]
        E[NumPy/scikit-learn]
        F[Matplotlib]
        G[PyYAML]
    end
    
    subgraph "External Services"
        H[Claude API]
        I[Local File System]
    end
    
    A --> D
    A --> E
    A --> F
    A --> G
    
    D --> H
    A --> I
```

---

## Data Flow Overview

```mermaid
flowchart LR
    A[Input Text] --> B[Noise Injection]
    B --> C[Translation Chain]
    C --> D[Claude API]
    D --> E[Results Storage]
    E --> F[Analysis Engine]
    F --> G[Metrics & Visualizations]
    
    H[Skills] --> C
    I[Config] --> C
    
    style D fill:#f9f,stroke:#333,stroke-width:2px
    style G fill:#9f9,stroke:#333,stroke-width:2px
```

---

## Quality Attributes

| Attribute | Requirement | Achieved Through |
|-----------|-------------|------------------|
| **Reliability** | 95%+ error coverage | Custom exception hierarchy, comprehensive tests |
| **Performance** | <30s per experiment | Efficient API calls, local embeddings |
| **Maintainability** | A+ code quality | Modular design, comprehensive docs |
| **Usability** | Clear CLI | argparse, help messages, examples |
| **Security** | No secret exposure | Environment variables, .env files |
| **Extensibility** | Easy skill addition | Plugin architecture, skill templates |

---

## Deployment Context

```mermaid
C4Deployment
    title Deployment Diagram
    
    Deployment_Node(dev_machine, "Developer Machine", "Windows/Linux/Mac") {
        Deployment_Node(wsl, "WSL/Linux Environment", "Ubuntu/Debian") {
            Deployment_Node(python, "Python Runtime", "3.8+") {
                Container(app, "ATM Application", "Python CLI", "Main system")
            }
        }
    }
    
    Deployment_Node(cloud, "Anthropic Cloud", "AWS") {
        Container(api, "Claude API", "REST API", "Translation service")
    }
    
    Deployment_Node(storage, "Local Storage", "File System") {
        ContainerDb(files, "Data Files", "JSON/TXT", "Skills, results, logs")
    }
    
    Rel(app, api, "HTTPS", "Translation requests")
    Rel(app, files, "File I/O", "Read/Write")
```

---

## Future Context (Potential Extensions)

```mermaid
graph TB
    subgraph "Current System"
        A[CLI Application]
    end
    
    subgraph "Future Enhancements"
        B[Web UI]
        C[REST API]
        D[Cloud Deployment]
        E[Database Storage]
        F[Multi-user Support]
    end
    
    A -.->|v2.0| B
    A -.->|v2.0| C
    B -.->|v3.0| D
    C -.->|v3.0| E
    D -.->|v3.0| F
    
    style A fill:#9f9,stroke:#333,stroke-width:2px
    style B fill:#ff9,stroke:#333,stroke-width:1px,stroke-dasharray: 5 5
    style C fill:#ff9,stroke:#333,stroke-width:1px,stroke-dasharray: 5 5
```

---

## Compliance & Standards

- **ISO/IEC 25010:** Software quality model compliance
- **Python PEP 8:** Code style guidelines
- **C4 Model:** Architecture documentation standard
- **Semantic Versioning:** Version numbering

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-26  
**Status:** Current

---

*This context diagram provides the highest-level view of the Agentic Turing Machine system and its ecosystem. For more detailed views, see Container and Component diagrams.*
