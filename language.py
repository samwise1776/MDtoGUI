#!/usr/bin/env python3

import sys
import re
import customtkinter as ctk
from pathlib import Path


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

if len(sys.argv) < 2:
    print("Usage: ./language.y app.md")
    raise SystemExit(1)

FILE = Path(sys.argv[1])

if not FILE.exists():
    print("File not found:", FILE)
    raise SystemExit(1)


root = ctk.CTk()
root.geometry("900x720")
root.minsize(600, 450)
root.title(FILE.stem)

container = ctk.CTkScrollableFrame(root)
container.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

STATE = {}
history = []


# ============================================================
# VARIABLES
# ============================================================

def setv(name, value):
    STATE[str(name)] = value


def getv(name, default=""):
    return STATE.get(str(name), default)


def replace_vars(text):
    def replace(match):
        name = match.group(1).strip()
        return str(getv(name, ""))

    return re.sub(
        r"\{\{(.*?)\}\}",
        replace,
        text
    )


# ============================================================
# UI
# ============================================================

def clear_page():
    for widget in container.winfo_children():
        widget.destroy()


def add_label(
    text,
    size=16,
    weight="normal",
    slant="roman",
    pady=3
):
    lbl = ctk.CTkLabel(
        container,
        text=replace_vars(text),
        anchor="w",
        justify="left",
        wraplength=820,
        font=ctk.CTkFont(
            size=size,
            weight=weight,
            slant=slant
        )
    )

    lbl.pack(
        fill="x",
        anchor="w",
        pady=pady
    )

    return lbl


# ============================================================
# LANGUAGE DEFINITIONS
# ============================================================

LANGUAGES = {
    "python": {
        "aliases": ["py"],
        "keywords": [
            "and", "as", "assert", "async", "await",
            "break", "class", "continue", "def", "del",
            "elif", "else", "except", "False", "finally",
            "for", "from", "global", "if", "import",
            "in", "is", "lambda", "None", "nonlocal",
            "not", "or", "pass", "raise", "return",
            "True", "try", "while", "with", "yield"
        ],
        "comment": r"#.*"
    },

    "javascript": {
        "aliases": ["js"],
        "keywords": [
            "const", "let", "var", "function", "return",
            "if", "else", "for", "while", "class",
            "new", "this", "true", "false", "null",
            "undefined", "async", "await", "try", "catch",
            "throw", "switch", "case", "break", "continue",
            "import", "export", "from"
        ],
        "comment": r"//.*"
    },

    "java": {
        "aliases": [],
        "keywords": [
            "public", "private", "protected", "class",
            "static", "final", "void", "int", "long",
            "double", "float", "boolean", "char", "byte",
            "short", "new", "return", "if", "else",
            "for", "while", "do", "switch", "case",
            "break", "continue", "try", "catch", "finally",
            "throw", "throws", "extends", "implements",
            "interface", "package", "import", "this",
            "super", "true", "false", "null"
        ],
        "comment": r"//.*"
    },

    "c": {
        "aliases": [],
        "keywords": [
            "auto", "break", "case", "char", "const",
            "continue", "default", "do", "double", "else",
            "enum", "extern", "float", "for", "goto",
            "if", "int", "long", "register", "return",
            "short", "signed", "sizeof", "static", "struct",
            "switch", "typedef", "union", "unsigned",
            "void", "volatile", "while"
        ],
        "comment": r"//.*"
    },

    "cpp": {
        "aliases": ["c++"],
        "keywords": [
            "auto", "bool", "break", "case", "catch",
            "char", "class", "const", "constexpr",
            "continue", "default", "delete", "do",
            "double", "else", "enum", "explicit",
            "extern", "false", "float", "for", "friend",
            "if", "inline", "int", "long", "namespace",
            "new", "nullptr", "private", "protected",
            "public", "return", "short", "signed",
            "sizeof", "static", "struct", "switch",
            "template", "this", "throw", "true",
            "try", "typedef", "typename", "union",
            "unsigned", "using", "virtual", "void",
            "volatile", "while"
        ],
        "comment": r"//.*"
    },

    "perl": {
        "aliases": ["pl"],
        "keywords": [
            "use", "sub", "my", "our", "local",
            "if", "elsif", "else", "unless", "while",
            "until", "for", "foreach", "return",
            "package", "require", "print", "say",
            "next", "last", "redo", "die", "warn"
        ],
        "comment": r"#.*"
    },

    "bash": {
        "aliases": ["sh", "shell"],
        "keywords": [
            "if", "then", "else", "elif", "fi",
            "for", "while", "until", "do", "done",
            "case", "esac", "function", "in",
            "echo", "printf", "read", "export",
            "local", "return", "exit", "source"
        ],
        "comment": r"#.*"
    },

    "lua": {
        "aliases": [],
        "keywords": [
            "and", "break", "do", "else", "elseif",
            "end", "false", "for", "function", "goto",
            "if", "in", "local", "nil", "not",
            "or", "repeat", "return", "then", "true",
            "until", "while"
        ],
        "comment": r"--.*"
    },

    "rust": {
        "aliases": ["rs"],
        "keywords": [
            "as", "async", "await", "break", "const",
            "continue", "crate", "dyn", "else", "enum",
            "extern", "false", "fn", "for", "if",
            "impl", "in", "let", "loop", "match",
            "mod", "move", "mut", "pub", "ref",
            "return", "self", "Self", "static", "struct",
            "super", "trait", "true", "type", "unsafe",
            "use", "where", "while"
        ],
        "comment": r"//.*"
    },

    "html": {
        "aliases": ["htm"],
        "keywords": [],
        "comment": r"<!--.*?-->"
    }
}


def resolve_language(name):
    name = name.lower().strip()

    if name in LANGUAGES:
        return name

    for language, data in LANGUAGES.items():
        if name in data["aliases"]:
            return language

    return None


# ============================================================
# SYNTAX HIGHLIGHTING
# ============================================================

def add_code_block(language, code):
    language = resolve_language(language)

    frame = ctk.CTkFrame(
        container,
        corner_radius=12
    )

    frame.pack(
        fill="x",
        pady=10
    )

    header = ctk.CTkLabel(
        frame,
        text=language or "code",
        anchor="w",
        font=ctk.CTkFont(
            size=13,
            weight="bold"
        )
    )

    header.pack(
        fill="x",
        padx=12,
        pady=(8, 2)
    )

    line_count = max(
        3,
        min(
            20,
            code.count("\n") + 1
        )
    )

    box = ctk.CTkTextbox(
        frame,
        height=line_count * 24,
        wrap="none",
        font=ctk.CTkFont(
            family="monospace",
            size=14
        )
    )

    box.pack(
        fill="x",
        padx=10,
        pady=(2, 10)
    )

    box.insert(
        "1.0",
        code
    )

    text = box._textbox

    text.tag_configure(
        "keyword",
        foreground="#C586C0"
    )

    text.tag_configure(
        "string",
        foreground="#CE9178"
    )

    text.tag_configure(
        "comment",
        foreground="#6A9955"
    )

    text.tag_configure(
        "number",
        foreground="#B5CEA8"
    )

    text.tag_configure(
        "function",
        foreground="#DCDCAA"
    )

    text.tag_configure(
        "tag",
        foreground="#569CD6"
    )

    text.tag_configure(
        "attribute",
        foreground="#9CDCFE"
    )

    if language:
        highlight_code(
            text,
            language,
            code
        )

    box.configure(
        state="disabled"
    )


def apply_regex_tag(textbox, code, pattern, tag):
    try:
        for match in re.finditer(
            pattern,
            code,
            re.MULTILINE | re.DOTALL
        ):
            start = "1.0+%dc" % match.start()
            end = "1.0+%dc" % match.end()

            textbox.tag_add(
                tag,
                start,
                end
            )
    except re.error:
        pass


def highlight_code(textbox, language, code):
    data = LANGUAGES[language]

    # Strings
    apply_regex_tag(
        textbox,
        code,
        r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
        "string"
    )

    # Numbers
    apply_regex_tag(
        textbox,
        code,
        r"\b(?:0x[0-9A-Fa-f]+|\d+(?:\.\d+)?)\b",
        "number"
    )

    # Comments
    if language == "html":
        apply_regex_tag(
            textbox,
            code,
            r"<!--.*?-->",
            "comment"
        )
    else:
        apply_regex_tag(
            textbox,
            code,
            data["comment"],
            "comment"
        )

    # Keywords
    for keyword in data["keywords"]:
        apply_regex_tag(
            textbox,
            code,
            rf"\b{re.escape(keyword)}\b",
            "keyword"
        )

    # Function calls
    apply_regex_tag(
        textbox,
        code,
        r"\b[A-Za-z_][A-Za-z0-9_]*(?=\s*\()",
        "function"
    )

    # HTML extras
    if language == "html":
        apply_regex_tag(
            textbox,
            code,
            r"</?[A-Za-z][A-Za-z0-9:-]*",
            "tag"
        )

        apply_regex_tag(
            textbox,
            code,
            r"\b[A-Za-z_:][-A-Za-z0-9_:.]*(?=\s*=)",
            "attribute"
        )


# ============================================================
# PYTHON EXECUTION
# ============================================================

def run_python(code):
    generated = []

    def emit(markdown):
        generated.extend(
            str(markdown).splitlines()
        )

    environment = {
        "setv": setv,
        "getv": getv,
        "emit": emit,
        "STATE": STATE,
        "root": root,
        "ctk": ctk,
        "print": print,
        "str": str,
        "int": int,
        "float": float,
        "len": len,
        "range": range,
        "min": min,
        "max": max,
        "sum": sum
    }

    try:
        exec(
            code,
            environment,
            environment
        )

    except Exception as e:
        generated.append(
            f"> Python error: {e}"
        )

    return generated


# ============================================================
# PARSER
# ============================================================

def parse_blocks(lines):
    blocks = []

    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()


        # CODE FENCE
        #
        # ```python
        # print("hello")
        # ```

        if stripped.startswith("```"):
            language = stripped[3:].strip()

            code = []

            i += 1

            while i < len(lines):
                if lines[i].strip() == "```":
                    break

                code.append(lines[i])
                i += 1

            blocks.append({
                "type": "code",
                "language": language,
                "code": "\n".join(code)
            })


        # BUTTON
        #
        # [] Hello ->
        # ...
        # <-

        elif (
            (
                stripped.startswith("[] ")
                or stripped.startswith("[ ] ")
            )
            and stripped.endswith("->")
        ):
            if stripped.startswith("[] "):
                name = stripped[3:-2].strip()
            else:
                name = stripped[4:-2].strip()

            body = []

            depth = 1
            i += 1

            while i < len(lines):
                current = lines[i]
                test = current.strip()

                if (
                    (
                        test.startswith("[] ")
                        or test.startswith("[ ] ")
                    )
                    and test.endswith("->")
                ):
                    depth += 1

                if test == "<-":
                    depth -= 1

                    if depth == 0:
                        break

                body.append(current)
                i += 1

            blocks.append({
                "type": "button",
                "name": name,
                "body": body
            })


        # MULTILINE PYTHON
        #
        # r: {
        # print(...)
        # }

        elif stripped == "r: {":
            code = []

            i += 1

            while i < len(lines):
                if lines[i].strip() == "}":
                    break

                code.append(lines[i])
                i += 1

            blocks.append({
                "type": "python",
                "code": "\n".join(code)
            })


        # ONE LINE PYTHON

        elif (
            stripped.startswith("r: {")
            and stripped.endswith("}")
        ):
            blocks.append({
                "type": "python",
                "code": stripped[4:-1].strip()
            })


        else:
            blocks.append({
                "type": "line",
                "text": line
            })

        i += 1

    return blocks


# ============================================================
# RENDERING
# ============================================================

def render(lines, remember=True):
    if remember:
        history.append(lines)

    clear_page()
    render_fragment(lines)


def render_fragment(lines):
    blocks = parse_blocks(lines)

    for item in blocks:

        # CODE

        if item["type"] == "code":
            add_code_block(
                item["language"],
                item["code"]
            )

            continue


        # PYTHON EXECUTION

        if item["type"] == "python":
            generated = run_python(
                item["code"]
            )

            if generated:
                render_fragment(
                    generated
                )

            continue


        # BUTTON

        if item["type"] == "button":
            button = ctk.CTkButton(
                container,
                text=replace_vars(
                    item["name"]
                ),
                height=42,
                corner_radius=10,
                command=lambda body=item["body"]:
                    render(body)
            )

            button.pack(
                fill="x",
                pady=6
            )

            continue


        line = item["text"]
        stripped = line.strip()


        # BLANK

        if not stripped:
            space = ctk.CTkFrame(
                container,
                height=8,
                fg_color="transparent"
            )

            space.pack()
            continue


        # COMMANDS

        if stripped == "@back":
            button = ctk.CTkButton(
                container,
                text="← Back",
                command=go_back
            )

            button.pack(
                fill="x",
                pady=8
            )

            continue


        if stripped == "@exit":
            button = ctk.CTkButton(
                container,
                text="Exit",
                command=root.destroy
            )

            button.pack(
                fill="x",
                pady=8
            )

            continue


        if stripped == "@theme dark":
            ctk.set_appearance_mode("Dark")
            continue


        if stripped == "@theme light":
            ctk.set_appearance_mode("Light")
            continue


        if stripped == "@theme system":
            ctk.set_appearance_mode("System")
            continue


        # WINDOW TITLE
        #
        # title: "My App"
        # title: My App

        if stripped.startswith("title:"):
            value = stripped[len("title:"):].strip()

            if (
                len(value) >= 2
                and value[0] in ("'", '"')
                and value[-1] == value[0]
            ):
                value = value[1:-1]

            root.title(
                replace_vars(value)
            )

            continue


        # HEADINGS

        if stripped.startswith("# "):
            text = replace_vars(
                stripped[2:]
            )

            root.title(text)

            add_label(
                text,
                size=34,
                weight="bold",
                pady=10
            )


        elif stripped.startswith("## "):
            add_label(
                stripped[3:],
                size=26,
                weight="bold",
                pady=7
            )


        elif stripped.startswith("### "):
            add_label(
                stripped[4:],
                size=21,
                weight="bold"
            )


        elif stripped.startswith("#### "):
            add_label(
                stripped[5:],
                size=18,
                weight="bold"
            )


        # BOLD ITALIC

        elif (
            stripped.startswith("***")
            and stripped.endswith("***")
            and len(stripped) > 6
        ):
            add_label(
                stripped[3:-3],
                weight="bold",
                slant="italic"
            )


        # BOLD

        elif (
            stripped.startswith("**")
            and stripped.endswith("**")
        ):
            add_label(
                stripped[2:-2],
                weight="bold"
            )


        # ITALIC

        elif (
            stripped.startswith("*")
            and stripped.endswith("*")
        ):
            add_label(
                stripped[1:-1],
                slant="italic"
            )


        # LIST

        elif stripped.startswith("- "):
            add_label(
                "• " + stripped[2:]
            )


        elif stripped.startswith("+ "):
            add_label(
                "• " + stripped[2:]
            )


        # QUOTE

        elif stripped.startswith("> "):
            quote = ctk.CTkFrame(
                container,
                corner_radius=8
            )

            quote.pack(
                fill="x",
                pady=6
            )

            qlabel = ctk.CTkLabel(
                quote,
                text=replace_vars(
                    stripped[2:]
                ),
                anchor="w",
                justify="left",
                wraplength=780,
                font=ctk.CTkFont(
                    size=15,
                    slant="italic"
                )
            )

            qlabel.pack(
                fill="x",
                padx=15,
                pady=12
            )


        # HORIZONTAL LINE

        elif stripped in (
            "---",
            "___"
        ):
            line_widget = ctk.CTkFrame(
                container,
                height=2
            )

            line_widget.pack(
                fill="x",
                pady=12
            )


        # TEXT INPUT

        elif stripped.startswith("[text]"):
            data = stripped[6:].strip()

            if ":" in data:
                variable, placeholder = data.split(
                    ":",
                    1
                )

                variable = variable.strip()
                placeholder = placeholder.strip()

            else:
                variable = ""
                placeholder = data

            entry = ctk.CTkEntry(
                container,
                placeholder_text=replace_vars(
                    placeholder
                ),
                height=40
            )

            entry.pack(
                fill="x",
                pady=5
            )

            if variable:
                def update(
                    event=None,
                    entry=entry,
                    variable=variable
                ):
                    setv(
                        variable,
                        entry.get()
                    )

                entry.bind(
                    "<KeyRelease>",
                    update
                )


        # TEXT AREA

        elif stripped.startswith("[area]"):
            box = ctk.CTkTextbox(
                container,
                height=150
            )

            box.pack(
                fill="x",
                pady=5
            )


        # CHECK

        elif stripped.startswith("[check]"):
            check = ctk.CTkCheckBox(
                container,
                text=replace_vars(
                    stripped[7:].strip()
                )
            )

            check.pack(
                anchor="w",
                pady=5
            )


        # SWITCH

        elif stripped.startswith("[switch]"):
            switch = ctk.CTkSwitch(
                container,
                text=replace_vars(
                    stripped[8:].strip()
                )
            )

            switch.pack(
                anchor="w",
                pady=5
            )


        # SLIDER

        elif stripped.startswith("[slider]"):
            slider = ctk.CTkSlider(
                container,
                from_=0,
                to=100
            )

            slider.pack(
                fill="x",
                pady=8
            )


        # PROGRESS

        elif stripped.startswith("[progress]"):
            try:
                value = float(
                    replace_vars(
                        stripped[10:].strip()
                    )
                )
            except ValueError:
                value = 0

            progress = ctk.CTkProgressBar(
                container
            )

            progress.set(
                max(
                    0,
                    min(
                        100,
                        value
                    )
                ) / 100
            )

            progress.pack(
                fill="x",
                pady=8
            )


        # SELECT

        elif stripped.startswith("[select]"):
            values = [
                x.strip()
                for x in stripped[8:].split(",")
                if x.strip()
            ]

            menu = ctk.CTkOptionMenu(
                container,
                values=values or ["Empty"]
            )

            menu.pack(
                fill="x",
                pady=5
            )


        # NORMAL TEXT

        else:
            add_label(
                stripped
            )


# ============================================================
# BACK
# ============================================================

def go_back():
    if len(history) <= 1:
        return

    history.pop()

    render(
        history[-1],
        remember=False
    )


# ============================================================
# START
# ============================================================

source = FILE.read_text(
    encoding="utf-8"
).splitlines()

render(source)

root.mainloop()
