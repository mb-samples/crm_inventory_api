---
inclusion: auto
---

# AWS Transform Custom - AI-Powered Code Modernization

## Overview

AWS Transform custom is an AI-powered CLI tool that performs large-scale modernization of software, code, libraries, and frameworks to reduce technical debt. It uses agentic AI with continual learning to deliver high-quality, repeatable transformations.

**Important:** This is NOT related to AWS CloudFormation transforms. It's a standalone code transformation tool.

## Key Capabilities

- **Natural language-driven transformation definition** - Create transformations using prompts, documentation, and code samples
- **Transformation execution** - Apply transformations consistently across multiple codebases
- **Continual learning** - Automatically improves from every execution and developer feedback
- **AWS-managed transformations** - Ready-to-use transformations for common scenarios

## Supported Transformation Patterns

| Pattern | Complexity | Examples |
|---------|-----------|----------|
| **API and Service Migrations** | Medium | AWS SDK v1→v2, Boto2→Boto3, JUnit 4→5, javax→jakarta |
| **Language Version Upgrades** | Low-Medium | Java 8→17, Python 3.9→3.13, Node.js 12→22 |
| **Framework Upgrades** | Medium | Spring Boot 2.x→3.x, React 17→18, Django upgrades |
| **Framework Migrations** | High | Angular→React, Redux→Zustand, Vue.js→React |
| **Library Upgrades** | Low-Medium | Pandas 1.x→2.x, NumPy, Hadoop/HBase/Hive |
| **Code Refactoring** | Low-Medium | Print→Logging, string concat→f-strings, type hints |
| **Script Translations** | Low-Medium | CDK→Terraform, Terraform→CloudFormation, Bash→PowerShell |
| **Architecture Migrations** | Medium-High | x86→Graviton (ARM), on-premises→Lambda, server→containers |
| **Language-to-Language** | Very High | Java→Python, JavaScript→TypeScript, C→Rust |
| **Organization-Specific** | Varies | Custom library migrations, coding standards |

## Core Concepts

### Transformation Definitions

A transformation definition is a package containing:
- `transformation_definition.md` (required) - Core transformation logic and instructions
- `summaries.md` (optional) - Summaries for reference documentation
- `document_references/` folder (optional) - User-provided docs and reference materials (text files only, max 10MB total)

### Transformation Registry

Your AWS account's centralized repository for storing and managing transformation definitions. Transformations are:
- Account-specific (not shared across AWS accounts)
- Version-controlled
- Discoverable via `atx custom def list`
- Executable across multiple codebases

### Draft vs Published Transformations

**Draft transformations:**
- In-progress or untested definitions
- Saved as specific versions
- Associated with specific conversations
- Useful for iterative development and testing

**Published transformations:**
- Available in your account's registry
- Discoverable by other users with IAM permissions
- Ready for team-wide use

**Typical workflow:**
1. Create transformation locally
2. Save as draft for testing (`atx custom def save-draft`)
3. Refine and validate
4. Publish to share with team (`atx custom def publish`)

### References vs Knowledge Items

**References:**
- User-provided documentation you explicitly add
- Text files only (max 10MB total)
- Contains documentation, API specs, migration guides, code samples
- Added when creating/updating transformation definitions

**Knowledge Items:**
- Automatically extracted learnings from executions
- Created by continual learning system
- Based on execution trajectories, developer feedback, code fixes
- Start in "not approved" state
- Must be explicitly approved before use in future executions
- Accumulate over time as transformation is executed

### Build and Validation Commands

Optional parameter specifying how to validate code during transformation. Examples:
- Java: `mvn clean install` or `gradle build`
- Python: `pytest` or `python -m py_compile`
- Node.js: `npm run build` or `npm test`
- Linters: `eslint .` or `pylint .`

**Important:** Providing validation commands significantly improves transformation quality through continual learning.

### Continual Learning

System that automatically captures feedback from every execution and improves quality over time:
- **Explicit feedback** - Comments and code fixes in interactive mode
- **Implicit observations** - Issues encountered while transforming/debugging

Creates knowledge items that improve future transformations. Occurs automatically after completion.

**Note:** Knowledge items are transformation-specific and not shared across transformations or accounts.

## Execution Modes

### 1. Interactive Conversational Mode
```bash
atx
```
- Full conversation with the agent
- Interrupt execution at any point
- Provide feedback during transformation
- Maximum control for complex scenarios

### 2. Direct Interactive Execution
```bash
atx custom def exec -n <transformation-name> -p <path>
```
- Review and interact at key decision points
- Agent pauses for input
- Ideal for testing and refining before autonomous execution

### 3. Non-Interactive/Headless Mode
```bash
atx custom def exec -n <transformation-name> -p <path> -x -t
```
- Full automation, no human intervention
- `-x` enables non-interactive mode
- `-t` automatically trusts all tools (use with caution)
- Designed for CI/CD pipelines and bulk execution

## Common Command Flags

| Flag | Description |
|------|-------------|
| `-n` or `--transformation-name` | Specifies transformation to execute |
| `-p` or `--code-repository-path` | Path to codebase (use "." for current) |
| `-c` or `--build-command` | Build or validation command |
| `-x` or `--non-interactive` | Enables non-interactive mode |
| `-t` or `--trust-all-tools` | Auto-trusts all tools (bypasses security guardrails) |
| `-d` or `--do-not-learn` | Prevents knowledge item extraction |
| `--tv` or `--transformation-version` | Specifies specific version |
| `-g` or `--configuration` | Provides configuration file or inline config |

**Warning:** `-t` flag bypasses all security guardrails. Use with caution in production.

## Essential Commands

### Basic Commands
```bash
# Interactive mode (default)
atx

# Show help
atx custom --help
atx custom -h

# Show version
atx --version
atx -v

# List available transformations
atx custom def list

# Execute transformation
atx custom def exec

# Manage MCP server configurations
atx mcp
```

### Transformation Management
```bash
# Save as draft
atx custom def save-draft -n my-transformation --description "Description" --sd ./transformation-directory

# Publish transformation
atx custom def publish -n my-transformation --description "Description" --sd ./transformation-directory

# Download transformation definition
atx custom def get -n my-transformation

# Download specific version
atx custom def get -n my-transformation --tv v1

# Delete transformation
atx custom def delete -n my-transformation

# Execute specific version
atx custom def exec -n my-transformation --tv v1 -p ./my-project
```

### Knowledge Item Management
```bash
# List knowledge items
atx custom def list-ki -n my-transformation

# View knowledge item details
atx custom def get-ki -n my-transformation --id <knowledge-item-id>

# Enable knowledge item
atx custom def update-ki-status -n my-transformation --id <knowledge-item-id> --status ENABLED

# Disable knowledge item
atx custom def update-ki-status -n my-transformation --id <knowledge-item-id> --status DISABLED

# Configure auto-approval
atx custom def update-ki-config -n my-transformation --auto-enabled TRUE

# Delete knowledge item
atx custom def delete-ki -n my-transformation --id <knowledge-item-id>

# Export knowledge items to markdown
atx custom def export-ki-markdown -n my-transformation
```

### Conversation Management
```bash
# Resume most recent conversation
atx --resume

# Resume specific conversation
atx --conversation-id <conversation-id>
```

**Note:** Conversations can only be resumed within 30 days of creation.

## Configuration Files

AWS Transform custom supports optional YAML or JSON configuration files:

```bash
# Using configuration file
atx custom def exec --configuration file://config.yaml

# Inline configuration
atx custom def exec --configuration "key=value,key2=value2"
```

**Example config.yaml:**
```yaml
codeRepositoryPath: ./my-project
transformationName: my-transformation
buildCommand: mvn clean install
additionalPlanContext: |
  The target Java version to upgrade to is Java 17.
  Ensure compatibility with our internal logging framework version 2.3.
validationCommands: |
  mvn test
  mvn verify
```

The `additionalPlanContext` parameter provides extra context for the agent's execution plan, especially useful with AWS-managed transformations.

## Typical Workflow (4 Phases)

### Phase 1: Define Transformation
- Provide natural language prompts, documentation, and code samples
- Agent generates initial transformation definition
- Iteratively refine through chat or direct edits
- Skip this phase when using AWS-managed transformations

### Phase 2: Pilot or Proof-of-Concept
- Test transformation on sample codebases
- Refine based on results
- Estimate cost and effort for full transformation
- Continual learning improves quality during this phase

### Phase 3: Scaled Execution
- Set up automated bulk execution using CLI
- Developers review and validate results
- Monitor progress using web application
- Track transformations across multiple repositories

### Phase 4: Monitor and Review
- Continual learning automatically improves quality
- Review and approve extracted knowledge items
- Ensure knowledge items meet quality standards

## Best Practices

### Creating Transformations
- Start with simple, well-defined transformations before complex ones
- Provide comprehensive reference materials (migration guides, code samples)
- Test on multiple sample codebases before publishing
- Use deterministic build/validation commands to enable continual learning
- Break complex transformations into smaller steps
- Mark crucial information with "CRITICAL:" or "IMPORTANT:" in definitions
- Explicitly specify exact requirements (commands, string values) using bash quotes for literal strings

### Providing Reference Materials
Recommended types:
- Before/after example code
- Documentation for APIs, libraries, or features
- Human-readable migration guides

**Supported formats:** Text-based files only (.md, .html, .txt, code files)
**Not supported:** Binary files, images, rich text (.pdf, .png, .docx)
**Limit:** 10MB total for all files

**Tip:** If you have many small text files, consider concatenating them into fewer descriptively-named files.

### Controlling Learning
```bash
# Prevent learning from specific execution
atx custom def exec -n my-transformation -p ./my-project -d
```

Use `-d` flag to opt out of knowledge item extraction for specific executions.

## Advanced Configuration

### Environment Variables
```bash
# Override shell command timeout (default: 900 seconds/15 minutes)
export ATX_SHELL_TIMEOUT=1800  # 30 minutes

# Disable automatic version checks
export ATX_DISABLE_UPDATE_CHECK=true
```

### Trust Settings
Configure in `~/.aws/atx/trust-settings.yaml`:
- `trustedTools` - Tools that execute without prompting
- `trustedShellCommands` - Shell commands that execute without prompting (supports wildcards)

**Default trusted tools:**
- `file_read`
- `get_transformation_from_registry`
- `list_available_transformations_from_registry`

**Session-level trust options during prompts:**
- `(y)es` - Execute once
- `(n)o` - Deny
- `(t)rust` - Trust for current session only (temporary, resets on CLI restart)

### Model Context Protocol (MCP) Servers
Configure in `~/.aws/atx/mcp.json` to extend CLI functionality.

```bash
# View configured MCP servers
atx mcp tools

# List tools from specific server
atx mcp tools --server <server-name>
```

### Tags and Organization
```bash
# List tags
atx custom def list-tags --arn <transformation-arn>

# Add tags
atx custom def tag --arn <transformation-arn> --tags '{"env":"prod","team":"backend"}'

# Remove tags
atx custom def untag --arn <transformation-arn> --tag-keys "env,team"
```

**ARN structure:** `arn:aws:transform-custom:<region>:<account-id>:package/<td-name>`

Tags enable grouped access control in IAM policies.

### Logs
**Conversation logs:**
- Location: `~/.aws/atx/custom/<conversation_id>/logs/<timestamp>-conversation.log`
- Contains full conversation history

**Developer debug logs:**
- Location: `~/.aws/atx/logs/debug*.log` and `~/.aws/atx/logs/error.log`
- Advanced troubleshooting information

**Tip:** Provide all relevant logs (`~/.aws/atx/custom/<conversation-id>/*` and `~/.aws/atx/logs/*`) when opening support tickets.

### CLI Updates
```bash
# Check for updates
atx update --check

# Update to latest version
atx update

# Update to specific version
atx update --target-version <version>
```

## Related AWS Transform Services

- **AWS Transform for Mainframe** - For COBOL/mainframe languages
- **AWS Transform for Windows** - For .NET Framework upgrades to .NET Core
- **AWS Transform for VMware** - For VMware migrations to AWS

## Quick Reference

**Start interactive mode:**
```bash
atx
```

**Execute transformation (interactive):**
```bash
atx custom def exec -n my-transformation -p ./my-project
```

**Execute transformation (headless):**
```bash
atx custom def exec -n my-transformation -p ./my-project -x -t
```

**List transformations:**
```bash
atx custom def list
```

**Publish transformation:**
```bash
atx custom def publish -n my-transformation --description "Description" --sd ./transformation-directory
```

**Resume conversation:**
```bash
atx --resume
```

---

**Document Purpose:** This steering document provides comprehensive guidance for working with AWS Transform custom in future conversations and implementations.
