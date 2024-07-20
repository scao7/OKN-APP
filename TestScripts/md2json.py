import re
import json

def extract_json_blocks_from_markdown(input_file, output_file_prefix, encoding='utf-8'):
    try:
        # Read the contents of the markdown file
        with open(input_file, 'r', encoding=encoding) as file:
            content = file.read()

        # Use regular expression to find all JSON blocks
        pattern = re.compile(r'```json(.*?)```', re.DOTALL)
        matches = pattern.findall(content)

        if matches:
            for index, match in enumerate(matches):
                json_block = match.strip()

                try:
                    # Sanitize and parse the JSON block to ensure it is valid
                    json_data = json.loads(json_block)

                    # Define the output file name for each JSON block
                    output_file = f"{output_file_prefix}_{index + 1}.json"

                    # Write the JSON data to the output file
                    with open(output_file, 'w', encoding=encoding) as file:
                        json.dump(json_data, file, indent=4)

                    print(f"JSON block {index + 1} extracted and saved to {output_file}")
                except json.JSONDecodeError as e:
                    print(f"JSON decoding error in block {index + 1}: {e}")
                    print("JSON block might contain invalid characters or formatting errors.")
        else:
            print("No JSON blocks found in the markdown file.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Usage example
input_file = r'D:\OKN_Front_End\TestScripts\NIBRS-2022-38925-0003-Codebook-ICPSR_entity_relation\output.md'
output_file_prefix = 'extracted_json_block'
extract_json_blocks_from_markdown(input_file, output_file_prefix)

