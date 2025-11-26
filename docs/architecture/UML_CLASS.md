# UML Class Diagram
## Agentic Turing Machine - System Architecture

**Purpose:** Show the static structure, classes, attributes, methods, and relationships  
**Scope:** Core modules and their interactions

---

## Complete Class Diagram

```mermaid
classDiagram
    %% Configuration Module
    class Config {
        -Dict~str,Any~ _config
        -Path _config_path
        -_instance: Config
        +__init__(config_path: Optional[Path])
        +get(key: str, default: Any) Any
        +_convert_type(value: str) Any
        +validate() None
        +model_name: str
        +temperature: float
        +max_tokens: int
        +noise_levels: List~int~
        +output_dir: Path
        +results_dir: Path
        +cost_tracking_enabled: bool
        +plugins_enabled: bool
    }
    
    %% Error Hierarchy
    class ATMError {
        <<exception>>
        +message: str
        +__init__(message: str)
    }
    
    class SkillNotFoundError {
        <<exception>>
    }
    
    class SkillLoadError {
        <<exception>>
    }
    
    class TranslationError {
        <<exception>>
    }
    
    class APIError {
        <<exception>>
    }
    
    class ValidationError {
        <<exception>>
    }
    
    class ConfigurationError {
        <<exception>>
    }
    
    class AnalysisError {
        <<exception>>
    }
    
    class FileOperationError {
        <<exception>>
    }
    
    %% Logger Module
    class LoggerSetup {
        <<static>>
        +setup_logging(log_level: str, log_file: Optional[Path]) Logger
        +get_logger(name: str) Logger
        -_create_file_handler(log_file: Path) FileHandler
        -_create_console_handler() StreamHandler
        -_get_formatter() Formatter
    }
    
    %% Cost Tracker Module
    class CostTracker {
        -str model_name
        -List~RequestRecord~ requests
        -float total_input_tokens
        -float total_output_tokens
        -float total_cost
        -Dict~str,float~ model_pricing
        +__init__(model_name: str)
        +record_request(usage: Usage) None
        +calculate_cost(input_tokens: int, output_tokens: int) float
        +get_total_cost() float
        +get_summary() Dict~str,Any~
        +export_report(output_path: Path) None
        +reset() None
    }
    
    class RequestRecord {
        +datetime timestamp
        +str model
        +int input_tokens
        +int output_tokens
        +float input_cost
        +float output_cost
        +float total_cost
        +Optional~str~ stage
    }
    
    %% Pipeline Module
    class Pipeline {
        <<static>>
        +load_skill(skill_name: str) Dict~str,str~
        +create_noisy_input(text: str, noise_level: int) str
        +run_translation_with_skill(client, skill_name, input_text, stage) str
        +run_translation_chain(input_text: str, noise_level: int) None
        +main() None
    }
    
    class SkillLoader {
        -Path skills_dir
        +__init__(skills_dir: Path)
        +load(skill_name: str) Skill
        +validate_skill(skill: Skill) bool
        +list_available() List~str~
    }
    
    class Skill {
        +str name
        +str content
        +Optional~Dict~ metadata
        +__init__(name: str, content: str)
        +to_dict() Dict~str,str~
    }
    
    class NoiseInjector {
        <<static>>
        +apply_noise(text: str, noise_level: int) str
        -_replace_char(char: str) str
        -_insert_random_char() str
        -_should_apply_noise(noise_level: int) bool
    }
    
    class TranslationExecutor {
        -Anthropic client
        -Config config
        -CostTracker cost_tracker
        -Logger logger
        +__init__(client, config, cost_tracker)
        +execute(skill_name: str, input_text: str, stage: int) str
        -_build_prompt(skill: Skill, text: str) str
        -_call_api(prompt: str) Response
        -_extract_translation(response: Response) str
    }
    
    class ChainOrchestrator {
        -TranslationExecutor executor
        -Config config
        -Logger logger
        +__init__(executor, config)
        +run_chain(input_text: str, noise_level: int) ChainResult
        -_save_outputs(noise_level: int, results: Dict) None
        -_create_output_directory(noise_level: int) Path
    }
    
    class ChainResult {
        +str original_input
        +str noisy_input
        +str french_output
        +str hebrew_output
        +str final_english_output
        +int noise_level
        +float total_cost
        +datetime timestamp
    }
    
    %% Analysis Module
    class AnalysisEngine {
        <<static>>
        +analyze_semantic_drift() Dict~str,Any~
        +load_final_outputs(noise_level: int) Tuple~str,str~
        +generate_graph(data: Dict) None
        +print_summary_statistics(data: Dict) None
    }
    
    class EmbeddingGenerator {
        -TfidfVectorizer vectorizer
        +__init__()
        +generate(texts: List~str~) ndarray
        +fit_transform(texts: List~str~) ndarray
    }
    
    class SimilarityCalculator {
        <<static>>
        +calculate_cosine_distance(vec1: ndarray, vec2: ndarray) float
        +calculate_text_similarity(text1: str, text2: str) float
        +calculate_word_overlap(text1: str, text2: str) float
        -_validate_vectors(vec1, vec2) None
    }
    
    class MetricsCollector {
        -Dict~str,Any~ metrics
        +__init__()
        +add_metric(name: str, value: float, noise_level: int) None
        +get_metrics() Dict~str,Any~
        +get_summary() Dict~str,Any~
        +export_json(path: Path) None
    }
    
    class GraphGenerator {
        -matplotlib Figure figure
        -matplotlib Axes axes
        +__init__()
        +create_line_plot(data: Dict, title: str) None
        +create_bar_chart(data: Dict, title: str) None
        +save(path: Path) None
        -_configure_style() None
    }
    
    %% Agent Tester Module
    class AgentTester {
        <<static>>
        +invoke_agent(skill_name: str, input_text: str) str
        +list_agents() List~str~
        +main() None
    }
    
    %% Relationships
    
    %% Error hierarchy
    ATMError <|-- SkillNotFoundError
    ATMError <|-- SkillLoadError
    ATMError <|-- TranslationError
    ATMError <|-- APIError
    ATMError <|-- ValidationError
    ATMError <|-- ConfigurationError
    ATMError <|-- AnalysisError
    ATMError <|-- FileOperationError
    
    %% Cost Tracker composition
    CostTracker "1" *-- "many" RequestRecord : contains
    
    %% Pipeline relationships
    Pipeline ..> Config : uses
    Pipeline ..> LoggerSetup : uses
    Pipeline ..> CostTracker : uses
    Pipeline ..> SkillLoader : uses
    Pipeline ..> NoiseInjector : uses
    Pipeline ..> TranslationExecutor : uses
    Pipeline ..> ChainOrchestrator : uses
    
    SkillLoader ..> Skill : creates
    SkillLoader ..> SkillNotFoundError : throws
    SkillLoader ..> SkillLoadError : throws
    
    TranslationExecutor --> Config : uses
    TranslationExecutor --> CostTracker : uses
    TranslationExecutor ..> Skill : uses
    TranslationExecutor ..> APIError : throws
    TranslationExecutor ..> TranslationError : throws
    
    ChainOrchestrator --> TranslationExecutor : uses
    ChainOrchestrator --> Config : uses
    ChainOrchestrator ..> ChainResult : creates
    ChainOrchestrator ..> FileOperationError : throws
    
    %% Analysis relationships
    AnalysisEngine ..> EmbeddingGenerator : uses
    AnalysisEngine ..> SimilarityCalculator : uses
    AnalysisEngine ..> MetricsCollector : uses
    AnalysisEngine ..> GraphGenerator : uses
    AnalysisEngine ..> AnalysisError : throws
    
    EmbeddingGenerator ..> AnalysisError : throws
    SimilarityCalculator ..> AnalysisError : throws
    
    %% Agent Tester relationships
    AgentTester ..> SkillLoader : uses
    AgentTester ..> Config : uses
    AgentTester ..> ValidationError : throws
    
    %% Global dependencies
    Config ..> ConfigurationError : throws
    LoggerSetup ..> FileOperationError : throws
```

---

## Module Details

### Configuration Module (`src/config.py`)

```mermaid
classDiagram
    class Config {
        <<singleton>>
        -Dict~str,Any~ _config
        -Path _config_path
        -Config _instance
        
        +__init__(config_path: Optional[Path])
        +get(key: str, default: Any) Any
        +_convert_type(value: str) Any
        +validate() None
        
        +model_name: str
        +temperature: float
        +max_tokens: int
        +noise_levels: List~int~
        +output_dir: Path
        +results_dir: Path
        +cost_tracking_enabled: bool
        +plugins_enabled: bool
    }
    
    note for Config "Singleton pattern ensures\nonly one config instance\nexists globally"
```

**Key Methods:**
- `get(key, default)`: Retrieve configuration value with fallback
- `_convert_type(value)`: Convert string values to appropriate types
- `validate()`: Ensure required configuration is present

**Properties:**
- Read-only access to configuration values
- Type-safe property accessors
- Environment variable overrides

---

### Error Hierarchy (`src/errors.py`)

```mermaid
classDiagram
    class ATMError {
        <<exception>>
        +str message
        +__init__(message: str)
    }
    
    class SkillNotFoundError {
        <<exception>>
        "Raised when skill file not found"
    }
    
    class SkillLoadError {
        <<exception>>
        "Raised when skill file cannot be loaded"
    }
    
    class TranslationError {
        <<exception>>
        "Raised when translation fails"
    }
    
    class APIError {
        <<exception>>
        "Raised when API call fails"
    }
    
    class ValidationError {
        <<exception>>
        "Raised when input validation fails"
    }
    
    class ConfigurationError {
        <<exception>>
        "Raised when configuration is invalid"
    }
    
    class AnalysisError {
        <<exception>>
        "Raised when analysis fails"
    }
    
    class FileOperationError {
        <<exception>>
        "Raised when file operation fails"
    }
    
    ATMError <|-- SkillNotFoundError
    ATMError <|-- SkillLoadError
    ATMError <|-- TranslationError
    ATMError <|-- APIError
    ATMError <|-- ValidationError
    ATMError <|-- ConfigurationError
    ATMError <|-- AnalysisError
    ATMError <|-- FileOperationError
```

**Design Pattern:** Exception Hierarchy  
**Purpose:** Precise error handling and recovery

---

### Cost Tracker Module (`src/cost_tracker.py`)

```mermaid
classDiagram
    class CostTracker {
        -str model_name
        -List~RequestRecord~ requests
        -float total_input_tokens
        -float total_output_tokens
        -float total_cost
        -Dict~str,float~ model_pricing
        
        +__init__(model_name: str)
        +record_request(usage: Usage) None
        +calculate_cost(input_tokens: int, output_tokens: int) float
        +get_total_cost() float
        +get_summary() Dict~str,Any~
        +export_report(output_path: Path) None
        +reset() None
    }
    
    class RequestRecord {
        +datetime timestamp
        +str model
        +int input_tokens
        +int output_tokens
        +float input_cost
        +float output_cost
        +float total_cost
        +Optional~str~ stage
    }
    
    CostTracker "1" *-- "many" RequestRecord : tracks
    
    note for CostTracker "Tracks API usage and costs\nSupports multiple Claude models\nExports detailed reports"
    
    note for RequestRecord "Immutable record of\nsingle API request"
```

**Model Pricing:**
```python
{
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},  # per MTok
    "claude-3-opus": {"input": 15.00, "output": 75.00},
    "claude-3-haiku": {"input": 0.25, "output": 1.25}
}
```

---

### Pipeline Module (`src/pipeline.py`)

```mermaid
classDiagram
    class SkillLoader {
        -Path skills_dir
        +__init__(skills_dir: Path)
        +load(skill_name: str) Skill
        +validate_skill(skill: Skill) bool
        +list_available() List~str~
    }
    
    class Skill {
        +str name
        +str content
        +Optional~Dict~ metadata
        +__init__(name: str, content: str)
        +to_dict() Dict~str,str~
    }
    
    class NoiseInjector {
        <<static>>
        +apply_noise(text: str, noise_level: int) str
        -_replace_char(char: str) str
        -_insert_random_char() str
        -_should_apply_noise(noise_level: int) bool
    }
    
    class TranslationExecutor {
        -Anthropic client
        -Config config
        -CostTracker cost_tracker
        -Logger logger
        
        +__init__(client, config, cost_tracker)
        +execute(skill_name: str, input_text: str, stage: int) str
        -_build_prompt(skill: Skill, text: str) str
        -_call_api(prompt: str) Response
        -_extract_translation(response: Response) str
    }
    
    class ChainOrchestrator {
        -TranslationExecutor executor
        -Config config
        -Logger logger
        
        +__init__(executor, config)
        +run_chain(input_text: str, noise_level: int) ChainResult
        -_save_outputs(noise_level: int, results: Dict) None
        -_create_output_directory(noise_level: int) Path
    }
    
    class ChainResult {
        +str original_input
        +str noisy_input
        +str french_output
        +str hebrew_output
        +str final_english_output
        +int noise_level
        +float total_cost
        +datetime timestamp
    }
    
    SkillLoader ..> Skill : creates
    TranslationExecutor ..> Skill : uses
    ChainOrchestrator --> TranslationExecutor : orchestrates
    ChainOrchestrator ..> ChainResult : produces
```

---

### Analysis Module (`src/analysis.py`)

```mermaid
classDiagram
    class EmbeddingGenerator {
        -TfidfVectorizer vectorizer
        
        +__init__()
        +generate(texts: List~str~) ndarray
        +fit_transform(texts: List~str~) ndarray
    }
    
    class SimilarityCalculator {
        <<static>>
        +calculate_cosine_distance(vec1: ndarray, vec2: ndarray) float
        +calculate_text_similarity(text1: str, text2: str) float
        +calculate_word_overlap(text1: str, text2: str) float
        -_validate_vectors(vec1, vec2) None
    }
    
    class MetricsCollector {
        -Dict~str,Any~ metrics
        
        +__init__()
        +add_metric(name: str, value: float, noise_level: int) None
        +get_metrics() Dict~str,Any~
        +get_summary() Dict~str,Any~
        +export_json(path: Path) None
    }
    
    class GraphGenerator {
        -matplotlib Figure figure
        -matplotlib Axes axes
        
        +__init__()
        +create_line_plot(data: Dict, title: str) None
        +create_bar_chart(data: Dict, title: str) None
        +save(path: Path) None
        -_configure_style() None
    }
    
    EmbeddingGenerator ..> SimilarityCalculator : provides vectors to
    SimilarityCalculator ..> MetricsCollector : sends metrics to
    MetricsCollector ..> GraphGenerator : provides data to
```

---

## Design Patterns Used

### 1. Singleton Pattern
**Class:** `Config`  
**Purpose:** Ensure single configuration instance  
**Implementation:**
```python
class Config:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

---

### 2. Factory Pattern
**Class:** `SkillLoader`  
**Purpose:** Create `Skill` objects from files  
**Implementation:**
```python
class SkillLoader:
    def load(self, skill_name: str) -> Skill:
        # Read file, parse, create Skill object
        return Skill(name=skill_name, content=content)
```

---

### 3. Strategy Pattern
**Class:** `NoiseInjector`  
**Purpose:** Different noise application strategies  
**Strategies:** Replace, Insert, Delete characters

---

### 4. Template Method Pattern
**Class:** `ChainOrchestrator`  
**Purpose:** Define translation chain skeleton  
**Steps:**
1. Load skills
2. Apply noise
3. Execute stage 1
4. Execute stage 2
5. Execute stage 3
6. Save outputs

---

### 5. Observer Pattern (Implicit)
**Class:** `CostTracker`  
**Purpose:** Observe API calls and record costs  
**Observers:** Logger, CostTracker, MetricsCollector

---

## Class Relationships Summary

| Relationship | Type | Description |
|--------------|------|-------------|
| Config → ConfigurationError | Dependency | Throws exception on invalid config |
| CostTracker ◆ RequestRecord | Composition | CostTracker contains RequestRecords |
| Pipeline → Config | Association | Pipeline uses Config |
| TranslationExecutor → CostTracker | Association | Executor uses CostTracker |
| ChainOrchestrator → TranslationExecutor | Association | Orchestrator uses Executor |
| SkillLoader ⇢ Skill | Dependency | Loader creates Skills |
| AnalysisEngine → EmbeddingGenerator | Dependency | Engine uses Generator |

---

## Dependency Graph

```mermaid
graph TD
    A[Pipeline] --> B[Config]
    A --> C[LoggerSetup]
    A --> D[CostTracker]
    A --> E[SkillLoader]
    
    F[AnalysisEngine] --> B
    F --> C
    F --> G[EmbeddingGenerator]
    F --> H[SimilarityCalculator]
    
    I[AgentTester] --> B
    I --> C
    I --> E
    
    E --> J[Skill]
    D --> K[RequestRecord]
    
    style A fill:#9f9
    style F fill:#9ff
    style I fill:#ff9
    style B fill:#f99
```

---

## Object Creation Sequence

```mermaid
sequenceDiagram
    participant Main
    participant Config
    participant Logger
    participant Tracker
    participant Executor
    participant Orchestrator
    
    Main->>Config: Config()
    Config-->>Main: config instance
    
    Main->>Logger: setup_logging()
    Logger-->>Main: logger
    
    Main->>Tracker: CostTracker(model_name)
    Tracker-->>Main: tracker instance
    
    Main->>Executor: TranslationExecutor(client, config, tracker)
    Executor-->>Main: executor instance
    
    Main->>Orchestrator: ChainOrchestrator(executor, config)
    Orchestrator-->>Main: orchestrator instance
```

---

## Attributes and Methods Summary

### Config Class
**Attributes:**
- `_config: Dict[str, Any]` - Configuration dictionary
- `_config_path: Path` - Path to config file
- `_instance: Config` - Singleton instance

**Methods:**
- `get(key, default)` - Get config value
- `validate()` - Validate configuration
- Properties for each config value

---

### CostTracker Class
**Attributes:**
- `model_name: str` - Model being tracked
- `requests: List[RequestRecord]` - All requests
- `total_cost: float` - Cumulative cost

**Methods:**
- `record_request(usage)` - Record API usage
- `calculate_cost(in, out)` - Calculate cost
- `export_report(path)` - Export to JSON

---

### TranslationExecutor Class
**Attributes:**
- `client: Anthropic` - API client
- `config: Config` - Configuration
- `cost_tracker: CostTracker` - Cost tracking
- `logger: Logger` - Logging

**Methods:**
- `execute(skill, text, stage)` - Run translation
- `_build_prompt(skill, text)` - Create prompt
- `_call_api(prompt)` - Invoke Claude
- `_extract_translation(response)` - Parse response

---

## Data Types

### Type Aliases
```python
SkillDict = Dict[str, str]  # {name, content}
MetricsDict = Dict[str, float]  # {metric_name: value}
ResultsDict = Dict[int, MetricsDict]  # {noise_level: metrics}
UsageDict = Dict[str, int]  # {input_tokens, output_tokens}
```

### Custom Types
```python
from typing import NamedTuple

class RequestRecord(NamedTuple):
    timestamp: datetime
    model: str
    input_tokens: int
    output_tokens: int
    input_cost: float
    output_cost: float
    total_cost: float
    stage: Optional[str] = None
```

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-26  
**Status:** Current

---

*This class diagram provides the static structure view of the Agentic Turing Machine system. For dynamic behavior, see UML Sequence diagrams.*
