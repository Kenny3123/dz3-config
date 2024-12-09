import json
import re
from collections import deque

class ConfigLangParser:
    def __init__(self):
        self.constants = {}  # Хранение констант

    def parse(self, source):
        lines = source.splitlines()
        result = {}

        for line in lines:
            line = line.strip()
            if "<" in line:  # Проверка на зарезервированный оператор
                raise SyntaxError(f"Operator '<' is reserved for future use: {line}")

            if not line or line.startswith('"'):  # Пропуск комментариев
                continue

            if line.startswith("def "):
                self._parse_constant(line)
            elif line.startswith("!"):
                return self._evaluate_expression(line[1:].strip())
            elif line.startswith("{") and line.endswith("}"):
                return self._parse_array(line)
            else:
                raise SyntaxError(f"Invalid syntax: {line}")

        return result

    def _parse_constant(self, line):
        match = re.match(r"def\s+([_a-z]+)\s*=\s*(.+);", line)
        if not match:
            raise SyntaxError(f"Invalid constant declaration: {line}")
        name, value = match.groups()
        value = self._parse_value(value)
        self.constants[name] = value

    def _evaluate_expression(self, expr):
        # Заменяем константы на их значения в выражении
        tokens = self._tokenize_expression(expr)
        stack = deque()

        for token in tokens:
            if token.isdigit():  # Если токен — число
                stack.append(int(token))
            elif token in self.constants:  # Если токен — константа
                stack.append(self.constants[token])
            elif token in {"+", "-", "min", "mod"}:  # Если токен — оператор
                self._apply_operator(stack, token)
            elif token == "(":  # Обработка открывающей скобки
                continue  # Просто пропускаем её, она не используется отдельно
            elif token == ")":  # Обработка закрывающей скобки
                continue  # Просто пропускаем её, она не используется отдельно
            else:
                raise ValueError(f"Unknown token: {token}. Ensure all variables are defined.")

        if len(stack) != 1:
            raise ValueError(f"Invalid expression: {expr}. Remaining stack: {list(stack)}")
        return stack.pop()

    def _apply_operator(self, stack, operator):
        if len(stack) < 2:
            raise ValueError(f"Not enough operands for operator {operator}.")

        right = stack.pop()
        left = stack.pop()

        if operator == "+":
            stack.append(left + right)
        elif operator == "-":
            stack.append(left - right)
        elif operator == "min":
            stack.append(min(left, right))
        elif operator == "mod":
            stack.append(left % right)
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def _parse_array(self, line):
        elements = line[1:-1].strip().split(".")
        return [self._parse_value(e.strip()) for e in elements if e.strip()]

    def _parse_value(self, value):
        if value.isdigit():
            return int(value)
        if value in self.constants:
            return self.constants[value]
        raise ValueError(f"Invalid value: {value}")

    # Новый метод для токенизации выражений
    def _tokenize_expression(self, expr):
        tokens = []
        temp = ""
        i = 0

        while i < len(expr):
            char = expr[i]

            if char.isalnum():  # Если символ является частью числа или имени
                temp += char
            elif char == " " and temp:  # Если встретили пробел, добавляем токен
                tokens.append(temp)
                temp = ""
            elif char in "+-()":  # Если это один из символов операций или скобок
                if temp:
                    tokens.append(temp)
                    temp = ""
                tokens.append(char)
            elif char == "m" and expr[i:i+3] == "min":  # Если это "min"
                tokens.append("min")
                i += 2  # Пропускаем символы "in"
            elif char == "m" and expr[i:i+3] == "mod":  # Если это "mod"
                tokens.append("mod")
                i += 2  # Пропускаем символы "od"
            i += 1

        if temp:
            tokens.append(temp)  # Добавляем последний токен

        return tokens
