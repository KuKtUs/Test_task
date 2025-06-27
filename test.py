import argparse
import csv
from tabulate import tabulate


def read_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)


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


def parse_condition(condition):
    operators = ['>=', '<=', '=', '>', '<']
    for op in operators:
        if op in condition:
            parts = condition.split(op)
            if len(parts) == 2:
                return parts[0], op, parts[1]
    raise ValueError(f"Invalid condition format: {condition}")


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
        return sum(numeric_values) / len(numeric_values)
    elif operation == 'min':
        return min(numeric_values)
    elif operation == 'max':
        return max(numeric_values)
    else:
        raise ValueError(f"Unknown aggregation operation: {operation}")


def main():
    parser = argparse.ArgumentParser(description='Process CSV file with filtering and aggregation.')
    parser.add_argument('file', help='Path to CSV file')
    parser.add_argument('--where', help='Filter condition (e.g., "price>500")')
    parser.add_argument('--aggregate', help='Aggregate condition (e.g., "price=avg")')

    args = parser.parse_args()

    data = read_csv(args.file)

    if args.where:
        data = apply_filter(data, args.where)

    if args.aggregate:
        result = calculate_aggregate(data, args.aggregate)
        if result is not None:
            print(f"Aggregate result: {result:.2f}" if isinstance(result, float) else f"Aggregate result: {result}")
        else:
            print("No numeric data available for aggregation")
    else:
        if data:
            print(tabulate(data, headers="keys", tablefmt="grid"))
        else:
            print("No data matches the filter condition")


if __name__ == '__main__':
    main()
