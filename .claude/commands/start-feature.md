# Start Feature Development

You are starting a new feature development session. Your task is to:

1. **Generate a branch name** based on the feature description provided by the user
   - Format: `feat/feature-name-kebab-case`
   - Example: For "add async database queries", generate `feat/add-async-db-queries`

2. **Create and checkout the branch** using git commands
   - Check current branch first
   - Create new branch from main
   - Checkout the new branch

3. **Create an initial commit** with a clear message
   - Message format: "feat: {feature description}"
   - Include the feature scope in the commit

4. **Show the setup confirmation** with:
   - Branch name created
   - Current status
   - Ready to start development

## Instructions for Claude Code

When the user invokes `/start-feature [feature-description]`:

1. Parse the feature description
2. Generate a proper kebab-case branch name (e.g., "Parser AST with metrics" → `feat/parser-ast-with-metrics`)
3. Execute these bash commands in sequence:
   - `git status` (verify clean state)
   - `git checkout -b feat/your-generated-name` (create and switch branch)
   - `git commit --allow-empty -m "feat: your feature description"` (initial commit to create branch)
   - `git log -1 --oneline` (show confirmation)
4. Output a summary showing:
   - ✅ Branch name: `feat/your-generated-name`
   - ✅ Ready to start development
   - Next step: "Run `/sync` when you've completed the feature"

## Examples

**Input:**
```
/start-feature Parser with AST and complexity metrics
```

**Output:**
```
✅ Branch created: feat/parser-ast-complexity-metrics
✅ Initial commit: feat: Parser with AST and complexity metrics
✅ Ready to develop!

Next: When done, run `/sync` to update CLAUDE.md
```

**Input:**
```
/start-feature Implement clean code agent for LLM analysis
```

**Output:**
```
✅ Branch created: feat/clean-code-agent-llm-analysis
✅ Initial commit: feat: Implement clean code agent for LLM analysis
✅ Ready to develop!

Next: When done, run `/sync` to update CLAUDE.md
```
