def print_input_messages(messages):
    try:
        # Prepare rows for table output
        headers = ["idx", "role", "tool_calls", "tool_call_id", "content"]
        rows = []
        for idx, m in enumerate(messages):
            role = str(m.get('role', ''))
            content = m.get('content')
            content_one_line = ' '.join((content or '').split()) if isinstance(content, str) else ''
            # Truncate long content for readability
            if len(content_one_line) > 200:
                content_one_line = content_one_line[:200]

            # Collect tool call names if any
            tool_calls = m.get('tool_calls')
            tool_call_names = ''
            if tool_calls:
                names = []
                for tc in tool_calls:
                    fn = tc.get('function', {}) if isinstance(tc, dict) else {}
                    names.append(fn.get('name', 'unknown'))
                tool_call_names = ','.join(names)

            tool_call_id = str(m.get('tool_call_id', ''))

            rows.append([
                str(idx),
                role,
                tool_call_names,
                tool_call_id,
                content_one_line,
            ])

        # Compute column widths with caps
        caps = [4, 10, 30, 24, 100]
        widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = min(max(widths[i], len(cell)), caps[i])

        def fmt_cell(text, width):
            if len(text) > width:
                return text[: max(0, width - 1)] + "…"
            return text.ljust(width)

        # Print table
        sep = "+" + "+".join(["-" * (w + 2) for w in widths]) + "+"
        print(f"[debug] input_messages count: {len(messages)}")
        print(sep)
        print("| " + " | ".join(fmt_cell(h, w) for h, w in zip(headers, widths)) + " |")
        print(sep)
        for row in rows:
            print("| " + " | ".join(fmt_cell(c, w) for c, w in zip(row, widths)) + " |")
        print(sep)
    except Exception as e:
        print(f"[debug] error printing input messages: {e}")

def print_output_message(response_message):

    print(f"[debug] Message received from OpenAI ")
    try:
        # Extract fields
        role = str(getattr(response_message, 'role', ''))
        content = getattr(response_message, 'content', '') or ''
        content_one_line = ' '.join(content.split())
        if len(content_one_line) > 200:
            content_one_line = content_one_line[:200]

        tool_names = []
        if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
            for tc in response_message.tool_calls:
                name = getattr(getattr(tc, 'function', object()), 'name', 'unknown')
                tool_names.append(name)
        tool_names_str = ','.join(tool_names)

        # Prepare table
        headers = ["role", "tool_calls", "content"]
        row = [role, tool_names_str, content_one_line]
        caps = [10, 30, 100]
        widths = [len(h) for h in headers]
        for i, cell in enumerate(row):
            widths[i] = min(max(widths[i], len(cell)), caps[i])

        def fmt_cell(text, width):
            if len(text) > width:
                return text[: max(0, width - 1)] + "…"
            return text.ljust(width)

        sep = "+" + "+".join(["-" * (w + 2) for w in widths]) + "+"
        print(sep)
        print("| " + " | ".join(fmt_cell(h, w) for h, w in zip(headers, widths)) + " |")
        print(sep)
        print("| " + " | ".join(fmt_cell(c, w) for c, w in zip(row, widths)) + " |")
        print(sep)
    except Exception as e:
        print(f"[debug] error printing output message: {e}")