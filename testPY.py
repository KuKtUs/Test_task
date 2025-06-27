import csv
import sys
from tabulate import tabulate


def read_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)


def parse_condition(condition):
    operators = ['>=', '<=', '=', '>', '<']
    for op in operators:
        if op in condition:
            parts = condition.split(op)
            if len(parts) == 2:
                return parts[0], op, parts[1]
    raise ValueError(f"Invalid condition format: {condition}")


def apply_filter(data, filter_condition):
    if not filter_condition:
        return data

    column, operator, value = parse_condition(filter_condition)

    filtered_data = []
    for row in data:
        row_value = row[column]
        if operator == '=':
            if str(row_value) == str(value):
                filtered_data.append(row)
        elif operator == '>':
            try:
                if float(row_value) > float(value):
                    filtered_data.append(row)
            except ValueError:
                pass
        elif operator == '<':
            try:
                if float(row_value) < float(value):
                    filtered_data.append(row)
            except ValueError:
                pass

    return filtered_data


def calculate_aggregate(data, aggregate_condition):
    if not aggregate_condition:
        return None

    column, operation = aggregate_condition.split('=')
    numeric_values = []

    for row in data:
        try:
            numeric_values.append(float(row[column]))
        except ValueError:
            continue

    if not numeric_values:
        return None

    if operation == 'avg':
        return round(sum(numeric_values) / len(numeric_values), 2)
    elif operation == 'min':
        return min(numeric_values)
    elif operation == 'max':
        return max(numeric_values)
    else:
        raise ValueError(f"Unknown operation: {operation}")


def print_results(data):
    if not data:
        print("No data to display")
        return
    print(tabulate(data, headers="keys", tablefmt="grid"))


def interactive_mode(file_path):
    data = read_csv(file_path)

    while True:
        print("\nAvailable commands:")
        print("1. filter [condition]")
        print("2. aggregate [column=operation]")
        print("3. show - Display current data")
        print("4. reset - Reset to original data")
        print("5. exit - Quit the program")

        try:
            command = input("\nEnter command: ").strip().split()
            if not command:
                continue

            if command[0] == 'filter' and len(command) > 1:
                filtered = apply_filter(data, command[1])
                print(f"Found {len(filtered)} matching records")
                print_results(filtered)
                data = filtered

            elif command[0] == 'aggregate' and len(command) > 1:
                result = calculate_aggregate(data, command[1])
                print(f"Aggregate result: {result}")

            elif command[0] == 'show':
                print_results(data)

            elif command[0] == 'reset':
                data = read_csv(file_path)
                print("Data reset to original")

            elif command[0] == 'exit':
                print("ПАкеда!")
                break

            else:
                print("Invalid command. Try again.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file>")
        sys.exit(1)

    try:
        interactive_mode(sys.argv[1])
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found")
    except Exception as e:
        print(f"An error occurred: {e}")
