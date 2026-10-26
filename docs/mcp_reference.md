# MCP Protocol Reference

This document provides a reference for the MCP (Model Context Protocol) definitions, schemas, resources, and configuration for the MCP Memory Server.

## Tools

The server provides the following tools. For all tools, the output schema is a simple string containing the result or error message.

### memory_store
**Description:** Store a memory. Type: 'decision', 'resolved', 'question', 'knowledge', or 'auto' (auto-detect).
For decisions: content = 'what | why | how'. For questions: priority 1=high, 2=medium, 3=low.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "content": {
      "type": "string"
    },
    "type": {
      "default": "auto",
      "type": "string"
    },
    "tags": {
      "default": "",
      "type": "string"
    },
    "priority": {
      "default": 2,
      "type": "integer"
    }
  },
  "required": [
    "content"
  ],
  "type": "object"
}
```

### memory_record_decision
**Description:** Record a decision made in this workspace.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "what": {
      "type": "string"
    },
    "why": {
      "default": "",
      "type": "string"
    },
    "how": {
      "default": "",
      "type": "string"
    },
    "tags": {
      "default": "",
      "type": "string"
    }
  },
  "required": [
    "what"
  ],
  "type": "object"
}
```

### memory_record_resolved
**Description:** Record a resolved issue or problem.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "what": {
      "type": "string"
    },
    "how": {
      "default": "",
      "type": "string"
    },
    "tags": {
      "default": "",
      "type": "string"
    }
  },
  "required": [
    "what"
  ],
  "type": "object"
}
```

### memory_record_question
**Description:** Record an open question. Priority: 1=high, 2=medium, 3=low.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "question": {
      "type": "string"
    },
    "context": {
      "default": "",
      "type": "string"
    },
    "tags": {
      "default": "",
      "type": "string"
    },
    "priority": {
      "default": 2,
      "type": "integer"
    }
  },
  "required": [
    "question"
  ],
  "type": "object"
}
```

### memory_record_knowledge
**Description:** Record a knowledge item. Will sync to Obsidian and Oracle.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "title": {
      "type": "string"
    },
    "content": {
      "default": "",
      "type": "string"
    },
    "tags": {
      "default": "",
      "type": "string"
    }
  },
  "required": [
    "title"
  ],
  "type": "object"
}
```

### memory_list
**Description:** List recent memories. Type: 'all', 'decisions', 'resolved', 'questions', 'knowledge'.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "type": {
      "default": "all",
      "type": "string"
    },
    "workspace": {
      "default": "current",
      "type": "string"
    },
    "limit": {
      "default": 20,
      "type": "integer"
    }
  },
  "type": "object"
}
```

### memory_get
**Description:** Get a specific memory by ID. Searches all tables. Auto-tracks access.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "id": {
      "type": "string"
    },
    "workspace": {
      "default": "current",
      "type": "string"
    }
  },
  "required": [
    "id"
  ],
  "type": "object"
}
```

### memory_get_summary
**Description:** Get memory summary (counts) for a workspace.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "workspace": {
      "default": "current",
      "type": "string"
    }
  },
  "type": "object"
}
```

### memory_delete
**Description:** Delete a memory by ID. Searches all tables.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "id": {
      "type": "string"
    },
    "workspace": {
      "default": "current",
      "type": "string"
    }
  },
  "required": [
    "id"
  ],
  "type": "object"
}
```

### memory_reinforce
**Description:** Manually boost a memory's salience. Use when a memory proves especially valuable.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "id": {
      "type": "string"
    },
    "workspace": {
      "default": "current",
      "type": "string"
    }
  },
  "required": [
    "id"
  ],
  "type": "object"
}
```

### memory_search
**Description:** Semantic search across ALL workspaces via Oracle.
domain: 'all', 'work', or 'personal'. Falls back to text search if vector not available.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "query": {
      "type": "string"
    },
    "domain": {
      "default": "all",
      "type": "string"
    },
    "limit": {
      "default": 10,
      "type": "integer"
    }
  },
  "required": [
    "query"
  ],
  "type": "object"
}
```

### memory_audit_search
**Description:** Search the audit trail log. Filter by keyword, date (YYYY-MM-DD), sender, importance (H/M/L).
Searches across subject, from_name, category, what, keywords fields.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "query": {
      "default": "",
      "type": "string"
    },
    "date": {
      "default": "",
      "type": "string"
    },
    "sender": {
      "default": "",
      "type": "string"
    },
    "importance": {
      "default": "",
      "type": "string"
    },
    "workspace": {
      "default": "all",
      "type": "string"
    },
    "limit": {
      "default": 20,
      "type": "integer"
    }
  },
  "type": "object"
}
```

### memory_audit_stats
**Description:** Get audit trail statistics. Optionally filter by date (YYYY-MM-DD or YYYY-MM) and workspace.
Shows counts by importance, direction, category, and suspicious flags.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "date": {
      "default": "",
      "type": "string"
    },
    "workspace": {
      "default": "all",
      "type": "string"
    }
  },
  "type": "object"
}
```

### memory_daily_report
**Description:** Get daily reports. Filter by date (YYYY-MM-DD) or get recent N days.
Shows email counts, calendar events, high-priority items, and narrative summary.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "date": {
      "default": "",
      "type": "string"
    },
    "workspace": {
      "default": "all",
      "type": "string"
    },
    "limit": {
      "default": 7,
      "type": "integer"
    }
  },
  "type": "object"
}
```

### memory_activity_log
**Description:** View agent activity log. Filter by agent name, action type, or workspace.
Shows what agents (schedulers, dispatchers, etc.) have been doing.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "agent": {
      "default": "",
      "type": "string"
    },
    "action": {
      "default": "",
      "type": "string"
    },
    "workspace": {
      "default": "all",
      "type": "string"
    },
    "limit": {
      "default": 20,
      "type": "integer"
    }
  },
  "type": "object"
}
```

### memory_status
**Description:** Get system status: local counts + Oracle sync status.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {},
  "type": "object"
}
```

### memory_compact
**Description:** Compact: summarize session.md, extract key items to SQLite, trim session.
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {
    "workspace": {
      "default": "current",
      "type": "string"
    }
  },
  "type": "object"
}
```

### memory_oracle_summary
**Description:** Cross-workspace summary from Oracle (all workspaces, all domains).
**Input Schema:**
```json
{
  "additionalProperties": false,
  "properties": {},
  "type": "object"
}
```


## Resources

The MCP Memory Server does not expose any resource endpoints or resource templates. Memory interactions are exclusively handled via the tools documented above.

## Server Configuration

The MCP Memory Server stores its configuration in `~/.mcp-memory/config.json`. The configuration is initialized by running `setup_config.py`.

### Default Configuration

```json
{
  "workspace_root": "~/Documents/Workspace",
  "claude_setup_dir": "~/Documents/claude-setup",
  "workspace_map": "~/Documents/claude-setup/workspace-map.json",
  "knowledge_dir": "~/Documents/knowledge",
  "oracle": {
    "enabled": false,
    "wallet_dir": "",
    "wallet_password": "",
    "dsn": "",
    "user": "CLAUDE_MEMORY",
    "password": ""
  },
  "embedding": {
    "provider": "none",
    "model": "text-embedding-3-small",
    "api_key": ""
  }
}
```

### Configuration Details

- **`workspace_map`**: Points to a JSON file mapping workspace IDs to folders under `workspace_root`.
- **`embedding.provider`**: Can be set to `none` or `openai`.
- **Oracle Settings**: Configure the oracle section if you plan to use Oracle cloud DB for vector searches and audit logs.
- **Environment Variables**:
  - `MEMORY_WORKSPACE`: Overrides the current workspace.
  - `MCP_MEMORY_WORKSPACE_ROOT`: Overrides the workspace root path.
  - `MCP_MEMORY_ORACLE_PASSWORD`: Oracle DB password override.
  - `OPENAI_API_KEY`: API key for OpenAI embeddings.
