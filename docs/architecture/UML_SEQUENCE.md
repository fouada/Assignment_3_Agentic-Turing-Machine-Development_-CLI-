# UML Sequence Diagram
## Agentic Turing Machine - Translation Flow

**Purpose:** Show the detailed sequence of interactions during a complete translation chain execution  
**Scope:** From user command to final output storage

---

## Complete Translation Chain Sequence

```mermaid
sequenceDiagram
    actor User
    participant CLI as run_with_skills.py
    participant Main as main()
    participant Chain as run_translation_chain()
    participant Loader as load_skill()
    participant Noise as create_noisy_input()
    participant Trans as run_translation_with_skill()
    participant Config as Configuration
    participant Logger as Logging System
    participant Tracker as Cost Tracker
    participant API as Claude API
    participant FS as File System
    
    User->>CLI: python run_with_skills.py --noise 25
    activate CLI
    
    CLI->>Main: parse arguments
    activate Main
    
    Main->>Config: load configuration
    Config-->>Main: config object
    
    Main->>Logger: initialize logging
    Logger-->>Main: logger ready
    
    Main->>Main: validate API key
    
    Main->>Chain: run_translation_chain(text, 25)
    activate Chain
    
    Note over Chain: Initialize client
    Chain->>API: Anthropic(api_key)
    API-->>Chain: client instance
    
    Note over Chain: Stage 0: Prepare input
    Chain->>Noise: create_noisy_input(text, 25)
    activate Noise
    Noise->>Noise: apply 25% character noise
    Noise-->>Chain: noisy_text
    deactivate Noise
    
    Chain->>Logger: info("Starting translation chain")
    
    Note over Chain,API: Stage 1: English → French
    Chain->>Loader: load_skill("english-to-french-translator")
    activate Loader
    Loader->>FS: read skills/.../SKILL.md
    FS-->>Loader: skill content
    Loader-->>Chain: skill_dict
    deactivate Loader
    
    Chain->>Trans: run_translation_with_skill(client, "en-to-fr", noisy_text, 1)
    activate Trans
    
    Trans->>Logger: info("Stage 1: EN→FR")
    Trans->>Config: get model_name, max_tokens, temperature
    Config-->>Trans: parameters
    
    Trans->>API: messages.create(model, messages)
    activate API
    Note over API: Claude processes<br/>English→French
    API-->>Trans: response (French text + usage)
    deactivate API
    
    Trans->>Tracker: record_request(usage)
    activate Tracker
    Tracker->>Tracker: calculate_cost(input_tokens, output_tokens)
    Tracker-->>Trans: cost recorded
    deactivate Tracker
    
    Trans->>Logger: debug(f"Translation: {french_text}")
    Trans-->>Chain: french_text
    deactivate Trans
    
    Note over Chain,API: Stage 2: French → Hebrew
    Chain->>Loader: load_skill("french-to-hebrew-translator")
    activate Loader
    Loader->>FS: read skills/.../SKILL.md
    FS-->>Loader: skill content
    Loader-->>Chain: skill_dict
    deactivate Loader
    
    Chain->>Trans: run_translation_with_skill(client, "fr-to-he", french_text, 2)
    activate Trans
    
    Trans->>Logger: info("Stage 2: FR→HE")
    Trans->>API: messages.create(model, messages)
    activate API
    Note over API: Claude processes<br/>French→Hebrew
    API-->>Trans: response (Hebrew text + usage)
    deactivate API
    
    Trans->>Tracker: record_request(usage)
    Trans->>Logger: debug(f"Translation: {hebrew_text}")
    Trans-->>Chain: hebrew_text
    deactivate Trans
    
    Note over Chain,API: Stage 3: Hebrew → English
    Chain->>Loader: load_skill("hebrew-to-english-translator")
    activate Loader
    Loader->>FS: read skills/.../SKILL.md
    FS-->>Loader: skill content
    Loader-->>Chain: skill_dict
    deactivate Loader
    
    Chain->>Trans: run_translation_with_skill(client, "he-to-en", hebrew_text, 3)
    activate Trans
    
    Trans->>Logger: info("Stage 3: HE→EN")
    Trans->>API: messages.create(model, messages)
    activate API
    Note over API: Claude processes<br/>Hebrew→English
    API-->>Trans: response (English text + usage)
    deactivate API
    
    Trans->>Tracker: record_request(usage)
    Trans->>Logger: debug(f"Translation: {final_english}")
    Trans-->>Chain: final_english
    deactivate Trans
    
    Note over Chain,FS: Save all outputs
    Chain->>FS: create outputs/noise_25/
    Chain->>FS: write agent1_french.txt
    Chain->>FS: write agent2_hebrew.txt
    Chain->>FS: write agent3_english.txt
    FS-->>Chain: files saved
    
    Chain->>Logger: info("Translation chain complete")
    Chain->>Tracker: export_cost_report()
    activate Tracker
    Tracker->>FS: write results/cost_analysis.json
    Tracker-->>Chain: report saved
    deactivate Tracker
    
    Chain-->>Main: success
    deactivate Chain
    
    Main->>Logger: info("Pipeline execution complete")
    Main-->>CLI: exit(0)
    deactivate Main
    
    CLI-->>User: "Translation complete. Check outputs/"
    deactivate CLI
```

---

## Error Handling Sequence

```mermaid
sequenceDiagram
    participant Chain as run_translation_chain()
    participant Loader as load_skill()
    participant Trans as run_translation_with_skill()
    participant API as Claude API
    participant Error as Error Handler
    participant Logger as Logger
    participant User
    
    Chain->>Loader: load_skill("invalid-skill")
    activate Loader
    
    Loader->>Loader: check if file exists
    Loader->>Error: raise SkillNotFoundError
    activate Error
    
    Error->>Logger: error("Skill not found: invalid-skill")
    Error-->>Chain: SkillNotFoundError
    deactivate Error
    deactivate Loader
    
    Chain->>Logger: error("Pipeline failed")
    Chain->>User: sys.exit(1) with error message
    
    Note over User: Alternative: API Error
    
    Chain->>Trans: run_translation_with_skill(...)
    activate Trans
    
    Trans->>API: messages.create(...)
    API-->>Trans: APIError (rate limit)
    
    Trans->>Error: raise APIError
    activate Error
    Error->>Logger: error("API call failed: rate limit")
    Error-->>Trans: APIError
    deactivate Error
    
    Trans-->>Chain: APIError
    deactivate Trans
    
    Chain->>Logger: error("Translation failed")
    Chain->>User: sys.exit(1) with retry advice
```

---

## Analysis Flow Sequence

```mermaid
sequenceDiagram
    actor User
    participant CLI as analyze_results_local.py
    participant Main as main()
    participant Analyzer as analyze_semantic_drift()
    participant Loader as load_final_outputs()
    participant Embed as get_local_embedding()
    participant Sim as calculate_cosine_distance()
    participant Overlap as calculate_word_overlap()
    participant Stats as print_summary_statistics()
    participant Graph as generate_graph()
    participant FS as File System
    
    User->>CLI: python analyze_results_local.py
    activate CLI
    
    CLI->>Main: execute
    activate Main
    
    Main->>Analyzer: analyze_semantic_drift()
    activate Analyzer
    
    Note over Analyzer: Initialize results dict
    Analyzer->>Analyzer: results = {}
    
    loop For each noise level [0, 25, 50, 75, 100]
        Analyzer->>Loader: load_final_outputs(noise_level)
        activate Loader
        
        Loader->>FS: read data/input_data.txt
        FS-->>Loader: original_text
        
        Loader->>FS: read outputs/noise_X/agent3_english.txt
        alt File exists
            FS-->>Loader: final_text
            Loader-->>Analyzer: (original, final)
        else File missing
            FS-->>Loader: FileNotFoundError
            Loader-->>Analyzer: (None, None)
        end
        deactivate Loader
        
        alt Both texts available
            Analyzer->>Embed: get_local_embedding([original, final])
            activate Embed
            Embed->>Embed: TfidfVectorizer.fit_transform()
            Embed-->>Analyzer: [vec_original, vec_final]
            deactivate Embed
            
            Analyzer->>Sim: calculate_cosine_distance(vec1, vec2)
            activate Sim
            Sim->>Sim: cosine_similarity → distance
            Sim-->>Analyzer: distance_value
            deactivate Sim
            
            Analyzer->>Overlap: calculate_word_overlap(text1, text2)
            activate Overlap
            Overlap->>Overlap: tokenize & compute intersection
            Overlap-->>Analyzer: overlap_percentage
            deactivate Overlap
            
            Analyzer->>Analyzer: results[noise_level] = {metrics}
        end
    end
    
    Note over Analyzer: Generate outputs
    
    Analyzer->>Stats: print_summary_statistics(results)
    activate Stats
    Stats->>Stats: calculate mean, std, trends
    Stats->>User: print statistics to console
    deactivate Stats
    
    Analyzer->>Graph: generate_graph(results)
    activate Graph
    Graph->>Graph: create matplotlib figure
    Graph->>FS: save results/semantic_drift.png
    Graph-->>Analyzer: graph saved
    deactivate Graph
    
    Analyzer->>FS: write results/analysis_results_local.json
    FS-->>Analyzer: file saved
    
    Analyzer-->>Main: results_dict
    deactivate Analyzer
    
    Main->>User: print("Analysis complete")
    Main-->>CLI: exit(0)
    deactivate Main
    
    CLI-->>User: "Results saved to results/"
    deactivate CLI
```

---

## Agent Testing Sequence

```mermaid
sequenceDiagram
    actor User
    participant CLI as test_agent.py
    participant Main as main()
    participant List as list_agents()
    participant Invoke as invoke_agent()
    participant API as Claude API
    participant FS as File System
    
    alt List agents mode
        User->>CLI: python test_agent.py --list
        CLI->>Main: parse args
        Main->>List: list_agents()
        activate List
        List->>FS: read skills/ directory
        FS-->>List: [skill1, skill2, skill3]
        List-->>Main: agent_list
        deactivate List
        Main->>User: print agent names
    else Test specific agent
        User->>CLI: python test_agent.py en-to-fr "Hello"
        CLI->>Main: parse args
        Main->>Main: validate inputs
        Main->>Invoke: invoke_agent("en-to-fr", "Hello")
        activate Invoke
        
        Invoke->>FS: load_skill("en-to-fr")
        FS-->>Invoke: skill_content
        
        Invoke->>API: messages.create(...)
        activate API
        API-->>Invoke: response
        deactivate API
        
        Invoke->>User: print(f"Result: {translation}")
        Invoke->>User: print(f"Tokens: {usage}")
        
        Invoke-->>Main: translation
        deactivate Invoke
        Main-->>User: exit(0)
    end
```

---

## Configuration Loading Sequence

```mermaid
sequenceDiagram
    participant App as Application
    participant Config as Config.__init__()
    participant FS as File System
    participant Env as Environment
    participant Validator as validate()
    
    App->>Config: Config() [singleton]
    activate Config
    
    Config->>FS: read config/config.yaml
    alt File exists
        FS-->>Config: yaml_content
        Config->>Config: yaml.safe_load()
    else File missing
        FS-->>Config: FileNotFoundError
        Config->>Config: use default values
    end
    
    Config->>Env: os.getenv("ANTHROPIC_API_KEY")
    Env-->>Config: api_key or None
    
    Config->>Env: os.getenv("MODEL_NAME")
    alt Env var set
        Env-->>Config: override_value
        Config->>Config: override config value
    else Not set
        Env-->>Config: None
        Config->>Config: use yaml/default value
    end
    
    Config->>Validator: validate()
    activate Validator
    Validator->>Validator: check required fields
    alt Valid
        Validator-->>Config: validation passed
    else Invalid
        Validator->>Config: raise ConfigurationError
    end
    deactivate Validator
    
    Config-->>App: config instance
    deactivate Config
    
    Note over App: Config is now available globally
    App->>Config: config.model_name
    Config-->>App: "claude-3-5-sonnet-20241022"
```

---

## Logging Initialization Sequence

```mermaid
sequenceDiagram
    participant App as Application
    participant Setup as setup_logging()
    participant Logger as Python logging
    participant FS as File System
    
    App->>Setup: setup_logging()
    activate Setup
    
    Setup->>FS: create logs/ directory
    FS-->>Setup: directory ready
    
    Setup->>Setup: generate log filename with timestamp
    Note over Setup: logs/atm_20251126_101523.log
    
    Setup->>Logger: create file handler
    Setup->>Logger: create console handler
    
    Setup->>Logger: set log level (INFO/DEBUG)
    Setup->>Logger: set formatter
    Note over Logger: %(asctime)s - %(name)s - %(levelname)s - %(message)s
    
    Setup->>Logger: add handlers to root logger
    
    Setup-->>App: logger configured
    deactivate Setup
    
    App->>Logger: logger.info("Application started")
    Logger->>FS: write to log file
    Logger->>User: print to console
```

---

## Cost Tracking Sequence

```mermaid
sequenceDiagram
    participant Trans as Translation Executor
    participant API as Claude API
    participant Tracker as CostTracker
    participant FS as File System
    
    Trans->>API: messages.create(...)
    API-->>Trans: response with usage
    
    Note over Trans: Extract usage info
    Trans->>Trans: usage = response.usage
    
    Trans->>Tracker: record_request(usage)
    activate Tracker
    
    Tracker->>Tracker: extract input_tokens
    Tracker->>Tracker: extract output_tokens
    
    Note over Tracker: Calculate costs
    Tracker->>Tracker: input_cost = tokens * $3/1M
    Tracker->>Tracker: output_cost = tokens * $15/1M
    Tracker->>Tracker: total_cost = input + output
    
    Tracker->>Tracker: add to running total
    Tracker->>Tracker: store request details
    
    Tracker-->>Trans: cost recorded
    deactivate Tracker
    
    Note over Trans: Later, after all translations
    
    Trans->>Tracker: export_cost_report()
    activate Tracker
    
    Tracker->>Tracker: aggregate all requests
    Tracker->>Tracker: format JSON report
    
    Tracker->>FS: write results/cost_analysis.json
    FS-->>Tracker: file saved
    
    Tracker-->>Trans: report exported
    deactivate Tracker
```

---

## Key Timing Information

| Operation | Typical Duration | Bottleneck |
|-----------|------------------|------------|
| Load skill | 1-5 ms | File I/O |
| Create noisy input | 1-10 ms | String operations |
| API call (translation) | 2-10 seconds | Network + AI processing |
| Cost tracking | <1 ms | In-memory calculation |
| Save output file | 1-5 ms | File I/O |
| Generate embeddings | 10-50 ms | TF-IDF vectorization |
| Calculate cosine distance | <1 ms | NumPy operations |
| Generate graph | 100-500 ms | Matplotlib rendering |
| **Full pipeline (1 noise level)** | **~10-30 seconds** | **3x API calls** |
| **Full experiment (5 noise levels)** | **~50-150 seconds** | **15x API calls** |

---

## State Transitions

```mermaid
stateDiagram-v2
    [*] --> Initialized: User starts CLI
    Initialized --> ConfigLoaded: Load config
    ConfigLoaded --> SkillsLoaded: Load skills
    SkillsLoaded --> NoiseApplied: Apply noise
    NoiseApplied --> Stage1: Translate EN→FR
    Stage1 --> Stage2: Translate FR→HE
    Stage2 --> Stage3: Translate HE→EN
    Stage3 --> OutputsSaved: Save results
    OutputsSaved --> CostsTracked: Export costs
    CostsTracked --> [*]: Complete
    
    ConfigLoaded --> Error: Invalid config
    SkillsLoaded --> Error: Skill not found
    Stage1 --> Error: API error
    Stage2 --> Error: API error
    Stage3 --> Error: API error
    Error --> [*]: Exit with error
```

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-26  
**Status:** Current

---

*These sequence diagrams detail the dynamic behavior of the Agentic Turing Machine system. For static structure, see C4 Component diagrams.*
