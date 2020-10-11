import re
from typing import NamedTuple, Iterable


class Token(NamedTuple):
    kind: str
    value: str


def lex(code: str) -> Iterable[Token]:
    """
    Retorna sequência de objetos do tipo token correspondendo à análise léxica
    da string de código fornecida.
    """
    lex_rules = (
            ("QUOTE", r"'"),
            ("LPAR", r"\("),
            ("RPAR", r"\)"),
            ("COMMENT", r";+[^\n]+$"),
            ("NUMBER", r"[+-]?[\d]+(?:\.[\d]+)?"),
            # accepts letters, symbols and digits, but the first char cannot be a digit
            ("NAME", r"[a-zA-Z+\-.*\/<=>!?:$%_&~^][\w+\-.*\/<=>!?:$%&~^]*"),
            ("STRING", r"\".*\""),
            # A "#\" followed by any printable characters
            ("CHAR", r"#\\[!-~]*"),
            ("BOOL", r"#[tf]"),
            ("WHITESPACE", r"[\s]+"),
            ("MISMATCH", r".")
    )

    tok_regex = '|'.join(f"(?P<{name}>{expr})" for name, expr in lex_rules)

    tokens = []
    for found in re.finditer(tok_regex, code):
        group = found.lastgroup
        content = found.group()

        # Discard all whitespace and comments
        if group != "WHITESPACE" and group != "COMMENT":
            tokens.append(Token(group, content))

    return tokens

if __name__ == "__main__":
    examples = (
            "( a )",
            "x ;; comentário",
            '"The word \"recursion\" has many meanings."',
            "'(+ 1 2)"
    )

    for ex in examples:
        print(ex)
        for tok in lex(ex):
            print(tok)
        print()
