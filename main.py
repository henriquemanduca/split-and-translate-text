import os
import argparse


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

    with open(input_file, 'r') as file:
        for line in file:
            total_lines += 1
            words = line.split()
            total_words += len(words)
            current_words += len(words)
            current_content.append(line)

            if current_words >= word_limit:
                save_file(output_dir, file_counter, current_content)
                file_counter += 1
                current_words = 0
                current_content = []

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
