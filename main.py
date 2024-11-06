import os
import argparse

def remove_duplicates(line):
    result = []
    words = line.split()
    previous_word = None

    for word in words:
        if word != previous_word:
            result.append(word)
        previous_word = word

    return ' '.join(result)


def process_file(input_file, word_limit):
    """
    Process the input file, count lines and words, and create new files when word limit is reached.

    Args:
    input_file (str): Path to the input file.
    word_limit (int): Maximum number of words per output file.

    Returns:
    tuple: Total number of lines and words processed.
    """
    output_dir = os.path.join(os.getcwd(), 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    total_lines = 0
    total_words = 0
    current_words = 0
    current_content = []
    file_counter = 1
    previous_line_incomplete = False

    with open(input_file, 'r') as file:
        for line in file:
            # Remove leading/trailing whitespace, including newline characters
            line = line.strip()
            if not line:
                continue

            total_lines += 1
            checked_line = remove_duplicates(line)

            words = checked_line.split()
            total_words += len(words)

            if previous_line_incomplete:
                current_content[-1] = f'{current_content[-1].rstrip()} {checked_line.lstrip()}\n'
                previous_line_incomplete = not (checked_line.rstrip().endswith('.') or checked_line.rstrip().endswith('"'))
            else:
                current_content.append(f'{checked_line}\n')
                previous_line_incomplete = not (checked_line.rstrip().endswith('.') or checked_line.rstrip().endswith('"'))

            current_words += len(words)

            if current_words >= word_limit and not previous_line_incomplete:
                save_file(output_dir, file_counter, current_content)
                file_counter += 1
                current_words = 0
                current_content = []
                previous_line_incomplete = False

    # Save any remaining content
    if current_content:
        save_file(output_dir, file_counter, current_content)

    return total_lines, total_words

def save_file(output_dir, file_number, content):
    """
    Save the content to a new file in the output directory.

    Args:
    output_dir (str): Directory to save the file.
    file_number (int): Number to append to the filename.
    content (list): List of lines to write to the file.
    """
    output_file = os.path.join(output_dir, f'output_{file_number}.txt')
    with open(output_file, 'w') as file:
        file.writelines(content)

def main():
    parser = argparse.ArgumentParser(description='Sample teste')

    parser.add_argument('input_file', type=str, help='Main file')
    parser.add_argument('--limit', type=int, default=500, help='Chunk by this number of words')

    args = parser.parse_args()

    total_lines, total_words = process_file(args.input_file, args.limit)
    print(f"Total lines processed: {total_lines}")
    print(f"Total words processed: {total_words}")


if __name__ == "__main__":
    main()
