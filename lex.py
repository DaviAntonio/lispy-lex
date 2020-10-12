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
            # ";" and all characters until a newline
            ("COMMENT", r";[^\n]*"),
            # accepts integers, fractions and floating point with exponents
            ("NUMBER", r"[+-]?[\d]+(?:(?:\/[\d]+)|(?:(?:\.[\d]+)?(?:[esfdl][+-]?[\d]+)?))"),
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
            "'(+ 1 2)",
            """;;; The FACT procedure computes the factorial
            ;;; of a non-negative integer.
            (define fact
              (lambda (n)
                (if (= n 0)
                    1        ;Base case: return 1
                    (* n (fact (- n 1))))))""",
            "0.0",
            "0",
            "1.5707963267948965",
            "0.7615941559557649",
            "1024",
            "9/10",
            "4/5",
            "2.762e8",
            "2.762e10",
            "2.762e+10",
            "2.762e-10",
            "2.762s8",
            "2.762s10",
            "2.762s+10",
            "2.762s-10",
            "2.762f8",
            "2.762f10",
            "2.762f+10",
            "2.762f-10",
            "2.762d8",
            "2.762f10",
            "2.762f+10",
            "2.762f-10",
            "2.762l8",
            "2.762l10",
            "2.762l+10",
            "2.762l-10"
    )

    for ex in examples:
        print(ex)
        for tok in lex(ex):
            print(tok)
        print()
