```mermaid
sequenceDiagram
    autonumber
    participant C as Client (Browser)
    participant R as chat_router
    participant U as chat_utils
    participant M as In-memory conversations
    participant DB as Postgres (conversations)
    participant G as Gemini API
    participant T as Tools (db_functions)
    participant TA as Todo API (/todos)

    C->>R: GET /chats/?question&chat_id OR POST /chats/stream {question, chat_id}<br/>Authorization Bearer access_token
    R->>R: user_dependency (get_current_user)
    alt Invalid or expired token
        R-->>C: 401 Unauthorized
    end

    rect rgb(235, 245, 255)
    Note over R,DB: get_chat(chat_id, user_id, db)
    alt No chat_id
        U->>U: new uuid chat_id
        U->>G: client.chats.create(model, tool_config)
        U->>M: store {user_id, chat}
    else chat_id in memory
        M-->>U: existing chat
    else chat_id not in memory
        U->>DB: load_history(chat_id, user_id)
        DB-->>U: history JSON or None
        U->>U: Content.model_validate per item
        U->>G: client.chats.create(model, tool_config, history)
        U->>M: store {user_id, chat}
    end
    end

    rect rgb(240, 255, 240)
    Note over C,TA: Tool-calling loop
    opt Stream endpoint
        U-->>C: SSE meta {chat_id}
    end
    U->>G: send_message(question) / send_message_stream(question)
    loop While model returns function_calls
        G-->>U: function_calls (or streamed chunks)
        opt Stream endpoint
            U-->>C: SSE token / tool_call {name, args}
        end
        U->>U: create_tool_mapper(token)
        U->>T: tool_function(args)
        T->>TA: HTTP GET/POST/PUT/DELETE /todos with Bearer token
        TA-->>T: JSON result
        T-->>U: result
        opt Stream endpoint
            U-->>C: SSE tool_result {name, result}
        end
        U->>G: send_message(function_response)
    end
    G-->>U: final text (or streamed chunks)
    end

    rect rgb(255, 250, 230)
    Note over U,DB: Persist + respond
    U->>DB: save_history(chat_id, user_id, chat.get_history(curated=True))
    alt GET /chats/
        U-->>C: 200 {answer, chat_id}
    else POST /chats/stream
        U-->>C: SSE token chunks ... then SSE done {chat_id}
    end
    end

    opt Any exception during stream
        U-->>C: SSE error {text}
    end
```