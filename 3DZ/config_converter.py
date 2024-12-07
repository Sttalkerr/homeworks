import argparse
import sys
import yaml
import re
import math
import operator


class ConfigConverter:
    def __init__(self):
        self.constants = {}
        self.operators = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "pow": math.pow,
            "abs": abs,
        }

    def evaluate_expression(self, expression):
        """Вычисляет выражение."""
        try:
            # Проверяем на выражение сложения
            if expression.startswith("|+"):
                # Извлекаем все числа после "|+"
                numbers = expression[3:].strip().split()  # Получаем строку без "|+" и "|"
                # Преобразуем каждое число в float и суммируем
                result = sum(float(num) for num in numbers)  
                return result
            # Остальные выражения оцениваются стандартным образом
            result = eval(expression, {}, self.constants)
            return result
        except (SyntaxError, NameError, TypeError) as e:
            return f"Error evaluating expression: {e}"

    def convert_yaml(self, yaml_data):
        """Конвертирует YAML в конфигурационный язык."""
        try:
            data = yaml.safe_load(yaml_data)
            return self.convert_value(data)
        except yaml.YAMLError as e:
            return f"Error parsing YAML: {e}"

    def convert_value(self, value):
        """Конвертирует отдельное значение в конфигурационный язык."""
        if isinstance(value, dict):
            return self.convert_dict(value)
        elif isinstance(value, list):
            return self.convert_list(value)
        elif isinstance(value, str):
            if value.startswith("|"):
                result = self.evaluate_expression(value)
                return str(result) if not isinstance(result, str) else result
            elif value.startswith("(define"):
                parts = value[len("(define"):].strip().split()
                if len(parts) == 2:
                    name, expression = parts
                    self.constants[name] = self.evaluate_expression(expression)
                    return value
                else:
                    return "Error: Invalid (define) syntax"
            elif value.startswith("(comment"):
                return self.convert_comment(value)
            else:
                return value
        else:
            return str(value)

    def convert_comment(self, comment_str):
        """Преобразует многострочный комментарий в нужный формат."""
        pattern = r"\(comment\s+(.*?)\)"
        match = re.match(pattern, comment_str, re.DOTALL)
        if match:
            lines = match.group(1).strip().splitlines()
            return f"(comment\n{' '.join(line.strip() for line in lines)}\n)"
        return ""

    def convert_dict(self, data):
        """Конвертирует словарь в формат конфигурационного языка."""
        result = "@{\n"
        for key, value in data.items():
            result += f"    {key} = {self.convert_value(value)};\n"
        result += "}"
        return result

    def convert_list(self, data):
        """Конвертирует список в формат конфигурационного языка."""
        return "[" + "; ".join(self.convert_value(item) for item in data) + "]"


def main():
    parser = argparse.ArgumentParser(description='Convert YAML to custom config format.')
    parser.add_argument('input', type=str, help='Input YAML file')
    parser.add_argument('output', type=str, help='Output config file')

    args = parser.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8') as infile:
            yaml_data = infile.read()

        converter = ConfigConverter()
        output = converter.convert_yaml(yaml_data)

        if isinstance(output, str) and output.startswith("Error"):
            print(output)
            sys.exit(1)

        with open(args.output, 'w', encoding='utf-8') as outfile:
            outfile.write(output)

    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

# Пример запуска: python config_converter.py example.yaml output.conf
