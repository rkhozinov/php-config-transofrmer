#!/usr/bin/env python3
"""
Simple PHP Config Environment Variable Transformer

A focused utility that transforms PHP define() statements from src/ directory
to result/ directory, converting them to use environment variables with fallbacks.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import List, Tuple, Optional, Dict


class EnvTransformer:
    """Simple transformer to convert PHP define() statements to use environment variables"""

    def __init__(self):
        # Pattern to match define() statements with various quote styles and spacing
        self.define_pattern = re.compile(
            r'define\s*\(\s*([\'"])(.*?)\1\s*,\s*(.*?)\s*\)\s*;',
            re.MULTILINE
        )
        # Pattern to check if already using getenv
        self.getenv_pattern = re.compile(r'getenv\s*\(')

    def transform_define_line(self, line: str) -> Tuple[str, bool]:
        """
        Transform a define() line to use environment variable with fallback
        Returns: (transformed_line, was_changed)
        """
        # Preserve original line ending
        line_ending = ''
        if line.endswith('\r\n'):
            line_ending = '\r\n'
            line_content = line[:-2]
        elif line.endswith('\n'):
            line_ending = '\n'
            line_content = line[:-1]
        else:
            line_content = line

        # Skip if already uses getenv
        if self.getenv_pattern.search(line_content):
            return line, False

        # Try to match define() pattern
        match = self.define_pattern.search(line_content)
        if not match:
            return line, False

        quote_char = match.group(1)  # Single or double quote used for constant name
        const_name = match.group(2)
        const_value = match.group(3).strip()

        # Skip if the value is already a getenv() call
        if const_value.startswith('getenv('):
            return line, False

        # Transform to use getenv() with current value as default
        # Preserve the original quote style for the constant name
        transformed_line = f"define({quote_char}{const_name}{quote_char}, getenv('{const_name}', {const_value}));{line_ending}"

        return transformed_line, True

    def preview_transform(self, file_path: str) -> List[dict]:
        """
        Preview what changes would be made without actually modifying the file
        Returns: List of changes that would be made
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        changes = []

        for line_num, line in enumerate(lines, 1):
            transformed_line, was_changed = self.transform_define_line(line)
            if was_changed:
                changes.append({
                    'line_number': line_num,
                    'original_line': line.rstrip(),
                    'transformed_line': transformed_line.rstrip()
                })

        return changes

    def transform_file(self, file_path: str) -> List[dict]:
        """
        Transform all define() statements in a file
        Returns: list_of_changes
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read file content
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        changes = []
        transformed_lines = []

        for line_num, line in enumerate(lines, 1):
            transformed_line, was_changed = self.transform_define_line(line)

            if was_changed:
                changes.append({
                    'line_number': line_num,
                    'original_line': line.rstrip(),
                    'transformed_line': transformed_line.rstrip()
                })

            transformed_lines.append(transformed_line)

        # Write transformed content back to file
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(transformed_lines)

        return changes

    def get_stats(self, file_path: str) -> dict:
        """Get statistics about defines in a file"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        total_defines = len(self.define_pattern.findall(content))
        getenv_defines = len(self.getenv_pattern.findall(content))

        return {
            'total_defines': total_defines,
            'getenv_defines': getenv_defines,
            'plain_defines': total_defines - getenv_defines,
            'transformable_defines': self._count_transformable_defines(content)
        }

    def _count_transformable_defines(self, content: str) -> int:
        """Count defines that can be transformed (not already using getenv)"""
        transformable = 0
        matches = self.define_pattern.finditer(content)

        for match in matches:
            const_value = match.group(3).strip()
            if not const_value.startswith('getenv('):
                transformable += 1

        return transformable


def setup_parser() -> argparse.ArgumentParser:
    """Setup command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Transform PHP define() statements to use environment variables with fallbacks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Transform files from src/ to result/
  python main.py src/

  # Transform with custom output directory
  python main.py src/ result/

  # Preview changes
  python main.py --preview src/

  # Show statistics
  python main.py --stats src/
        """
    )

    parser.add_argument('src_dir', nargs='?', default='src', help='Source directory (default: src)')
    parser.add_argument('result_dir', nargs='?', default='result', help='Result directory (default: result)')
    parser.add_argument('--preview', action='store_true', help='Preview changes without writing files')
    parser.add_argument('--stats', action='store_true', help='Show statistics about defines')

    return parser


def preview_transformations(src_dir: str, result_dir: str) -> None:
    """Preview what transformations would be made"""
    transformer = EnvTransformer()
    src_path = Path(src_dir)
    result_path = Path(result_dir)

    if not src_path.exists():
        print(f"✗ Source directory not found: {src_dir}")
        sys.exit(1)

    # Find all .inc files
    config_files = list(src_path.glob("*.inc"))
    if not config_files:
        print(f"No .inc files found in {src_dir}")
        return

    print(f"Preview of transformations from {src_dir} to {result_dir}:")
    print("=" * 60)

    total_changes = 0
    for file_path in sorted(config_files):
        try:
            changes = transformer.preview_transform(str(file_path))
            if changes:
                print(f"\n{file_path.name}: {len(changes)} changes")
                for change in changes[:3]:  # Show first 3 changes
                    print(f"  Line {change['line_number']}: {change['transformed_line']}")
                if len(changes) > 3:
                    print(f"  ... and {len(changes) - 3} more changes")
                total_changes += len(changes)
            else:
                print(f"\n{file_path.name}: no changes needed")
        except Exception as e:
            print(f"\n{file_path.name}: error - {e}")

    print(f"\nTotal transformations: {total_changes}")


def show_statistics(src_dir: str) -> None:
    """Show statistics about defines in source files"""
    transformer = EnvTransformer()
    src_path = Path(src_dir)

    if not src_path.exists():
        print(f"✗ Source directory not found: {src_dir}")
        sys.exit(1)

    config_files = list(src_path.glob("*.inc"))
    if not config_files:
        print(f"No .inc files found in {src_dir}")
        return

    print(f"Statistics for {src_dir}:")
    print("=" * 40)

    total_defines = 0
    total_getenv = 0
    total_transformable = 0

    for file_path in sorted(config_files):
        try:
            stats = transformer.get_stats(str(file_path))
            print(f"\n{file_path.name}:")
            print(f"  Total defines: {stats['total_defines']}")
            print(f"  Already using getenv(): {stats['getenv_defines']}")
            print(f"  Transformable: {stats['transformable_defines']}")

            total_defines += stats['total_defines']
            total_getenv += stats['getenv_defines']
            total_transformable += stats['transformable_defines']
        except Exception as e:
            print(f"\n{file_path.name}: error - {e}")

    print(f"\nOverall totals:")
    print(f"  Total defines: {total_defines}")
    print(f"  Already using getenv(): {total_getenv}")
    print(f"  Transformable: {total_transformable}")


def transform_files(src_dir: str, result_dir: str) -> None:
    """Transform files from source to result directory"""
    transformer = EnvTransformer()
    src_path = Path(src_dir)
    result_path = Path(result_dir)

    if not src_path.exists():
        print(f"✗ Source directory not found: {src_dir}")
        sys.exit(1)

    # Create result directory if it doesn't exist
    result_path.mkdir(exist_ok=True)

    # Find all .inc files
    config_files = list(src_path.glob("*.inc"))
    if not config_files:
        print(f"No .inc files found in {src_dir}")
        return

    print(f"Transforming files from {src_dir} to {result_dir}:")
    print("=" * 50)

    total_files = 0
    total_changes = 0
    files_with_changes = 0

    for file_path in sorted(config_files):
        result_file = result_path / file_path.name

        try:
            # Copy original file to result directory
            shutil.copy2(file_path, result_file)

            # Transform the file in result directory
            changes = transformer.transform_file(str(result_file))

            if changes:
                files_with_changes += 1
                total_changes += len(changes)
                print(f"✓ {file_path.name}: {len(changes)} changes")
            else:
                print(f"- {file_path.name}: no changes needed")

            total_files += 1

        except Exception as e:
            print(f"✗ {file_path.name}: error - {e}")

    print(f"\nSummary:")
    print(f"  Files processed: {total_files}")
    print(f"  Files with changes: {files_with_changes}")
    print(f"  Total transformations: {total_changes}")


def main():
    """Main entry point"""
    parser = setup_parser()
    args = parser.parse_args()

    if args.stats:
        show_statistics(args.src_dir)
    elif args.preview:
        preview_transformations(args.src_dir, args.result_dir)
    else:
        transform_files(args.src_dir, args.result_dir)


if __name__ == '__main__':
    main()