import os
import re
import shutil

from pydantic.v1 import validate_arguments

from constants.constants import DIFF_FILE_DIRECTORY, DIFF_FILE_EXTENSION, EXTENSION_TO_LANGUAGE
from dto.code_comment_meta import CodeCommentMetadata
from dto.github_event import ProcessEvent


class DiffFileUtil:
    """Utility class for extracting and separating diff files."""

    def __init__(self):
        """Initializes the diff file utility."""
        pass

    @staticmethod
    def extract_diffs(diff_text):
        # Splitting the diff text by the diff headers
        diffs = [d for d in diff_text.split("diff --git ") if d]

        # Creating a dictionary to store diffs for each file
        diff_dict = {}

        for d in diffs:
            # Extracting file name from the header
            file_name = d.split()[0].split('b/')[-1]
            diff_content = "diff --git " + d
            diff_dict[file_name] = diff_content

        return diff_dict

    @staticmethod
    def save_diffs_to_files(diff_dict, process_event: ProcessEvent) -> str:

        directory_path = os.path.join(DIFF_FILE_DIRECTORY, process_event.org_name, process_event.repo_name,
                                      str(process_event.pr_id), process_event.commit_id)
        os.makedirs(directory_path, exist_ok=True)
        for file_name, diff_content in diff_dict.items():
            safe_name = directory_path + "/" + file_name.replace("/", ".").strip() + DIFF_FILE_EXTENSION
            with open(safe_name, 'w') as f:
                f.write(DiffFileUtil.annotate_diff_with_line_numbers(diff_content))
        return directory_path

    @staticmethod
    def split_diffs_to_files(main_diff_content, process_event: ProcessEvent) -> str:
        # Extracting diffs from each file from the main diff
        diff_dict = DiffFileUtil.extract_diffs(main_diff_content)
        # Saving the diffs to files
        return DiffFileUtil.save_diffs_to_files(diff_dict, process_event)

    @staticmethod
    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def extract_file_info_from_diff(diff_output) -> CodeCommentMetadata:
        # Use regex to capture path after "diff --git a/" and before " b/"
        path_pattern = re.compile(r'diff --git a/(.*?) b/')
        path_match = path_pattern.search(diff_output)

        # Use regex to capture commit ID after "index" and before ".."
        commit_pattern = re.compile(r'index (\w+)\.\.')
        commit_match = commit_pattern.search(diff_output)

        path = path_match.group(1) if path_match else None
        commit_id = commit_match.group(1) if commit_match else None

        return CodeCommentMetadata(path=path, commit_id=commit_id)

    @staticmethod
    def delete_directory(directory_path):
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)
            print(f"Deleted directory: {directory_path}")
        else:
            print(f"Directory {directory_path} does not exist.")

    @staticmethod
    def language_from_diff_file(diff_file_content):

        # Extract the file path from the diff
        pattern = re.compile(r'diff --git a/(.*?) b/')
        match = pattern.search(diff_file_content)
        if not match:
            return None

        # Extract file extension
        filepath = match.group(1)
        _, extension = os.path.splitext(filepath)

        # Get the language from the dictionary based on the file extension
        return EXTENSION_TO_LANGUAGE.get(extension, None)

    @staticmethod
    def annotate_diff_with_line_numbers(diff):
        lines = diff.split('\n')
        annotated_lines = []
        new_line_num = None
        within_chunk = False

        for line in lines:
            # Detect chunk header
            if line.startswith('@@'):
                # Extract line numbers from chunk header
                match = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
                if match:
                    new_line_num = int(match.group(1))
                    within_chunk = True
                else:
                    within_chunk = False  # In case regex fails, set to False to prevent processing below
                annotated_lines.append(line)
                continue

            # Ensure we're within a chunk before annotating lines
            if not within_chunk:
                annotated_lines.append(line)
                continue

            # Annotate lines based on their type
            if line.startswith('+'):
                annotated_lines.append(f"+{new_line_num} {line[1:]}")  # Place line number after '+'
                new_line_num += 1
            else:
                # Either a removed line or context line (unchanged), add as is
                annotated_lines.append(line)
                if not line.startswith('-'):  # Increment only if it's a context line
                    new_line_num += 1

        return '\n'.join(annotated_lines)
