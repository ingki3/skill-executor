# Research: Skill Executor Agent

## Phase 0: Research Tasks

### Decision 1: FAISS Integration & Confidence Threshold
- **Decision**: Use `FAISS-cpu` with L2 distance. Implement a `MIN_CONFIDENCE_SCORE` threshold.
- **Rationale**: If the L2 distance of the top match exceeds a certain threshold (configurable), the system will treat it as "No Match Found" as per clarification.
- **Alternatives considered**: Cosine similarity (Rejected, L2 is default for many vector tasks).

### Decision 2: LLM-based Security Verification
- **Decision**: Use a "Security Agent" prompt with Gemini 1.5 Flash to evaluate skill code and prompts.
- **Rationale**: LLMs are better at understanding context and intent compared to static AST analysis for detecting subtle prompt injection or data exfiltration attempts.
- **Alternatives considered**: Static AST (Now a pre-filter step before the LLM scan).

### Decision 3: Skill Synchronization Flow
- **Decision**: Backend will use `git pull` or `git fetch/reset` to update local copies in `.skills/` when the "Sync" button is pressed.
- **Rationale**: Manual sync ensures stability. The system must re-run the security scan and re-index the skill in FAISS after every sync.
- **Alternatives considered**: Automatic sync (Rejected by user for transparency).

### Decision 4: Simple vs. Advanced Tier LLM Mapping
- **Decision**: 
    - **Simple**: Gemini 1.5 Flash.
    - **Advanced**: Gemini 1.5 Pro (ReACT).
- **Rationale**: Flash for speed, Pro for multi-step reasoning.