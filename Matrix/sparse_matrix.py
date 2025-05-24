class SparseMatrix:
    def __init__(self, file_path=None, num_rows=None, num_cols=None):
        self.rows = 0
        self.cols = 0
        self.data = {}  # Dictionary of dictionaries: {row: {col: value}}

        if file_path is not None:
            self._load_from_file(file_path)
        elif num_rows is not None and num_cols is not None:
            if num_rows <= 0 or num_cols <= 0:
                raise ValueError("Matrix dimensions must be positive")
            self.rows = num_rows
            self.cols = num_cols
        else:
            raise ValueError("Either file_path or both num_rows and num_cols must be provided")

    def _load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file if line.strip()]

                if len(lines) < 2:
                    raise ValueError("Input file must specify rows and cols")

                if not lines[0].startswith('rows='):
                    raise ValueError("First line must specify rows")
                self.rows = int(lines[0][5:])

                if not lines[1].startswith('cols='):
                    raise ValueError("Second line must specify cols")
                self.cols = int(lines[1][5:])

                for line in lines[2:]:
                    self._parse_entry(line)

        except IOError:
            raise ValueError(f"Could not open file: {file_path}")

    def _parse_entry(self, line):
        clean_line = ''.join(line.split())

        if not clean_line.startswith('(') or not clean_line.endswith(')'):
            raise ValueError("Input file has wrong format - missing parentheses")

        content = clean_line[1:-1]
        parts = content.split(',')

        if len(parts) != 3:
            raise ValueError("Input file has wrong format - entry doesn't have 3 values")

        try:
            row = int(parts[0])
            col = int(parts[1])
            value = int(parts[2])
        except ValueError:
            raise ValueError("Input file has wrong format - non-integer value")

        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise ValueError("Input file has wrong format - row or column out of bounds")

        if value != 0:
            if row not in self.data:
                self.data[row] = {}
            self.data[row][col] = value

    def get_element(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise IndexError("Matrix indices out of range")
        return self.data.get(row, {}).get(col, 0)

    def set_element(self, row, col, value):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise IndexError("Matrix indices out of range")
        if value == 0:
            if row in self.data and col in self.data[row]:
                del self.data[row][col]
                if not self.data[row]:
                    del self.data[row]
        else:
            if row not in self.data:
                self.data[row] = {}
            self.data[row][col] = value

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(f"Cannot add matrices of different dimensions. Matrix1: {self.rows}x{self.cols}, Matrix2: {other.rows}x{other.cols}")

        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        for row in self.data:
            for col in self.data[row]:
                result.set_element(row, col, self.data[row][col])
        for row in other.data:
            for col in other.data[row]:
                current = result.get_element(row, col)
                result.set_element(row, col, current + other.data[row][col])
        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(f"Cannot subtract matrices of different dimensions. Matrix1: {self.rows}x{self.cols}, Matrix2: {other.rows}x{other.cols}")

        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        for row in self.data:
            for col in self.data[row]:
                result.set_element(row, col, self.data[row][col])
        for row in other.data:
            for col in other.data[row]:
                current = result.get_element(row, col)
                result.set_element(row, col, current - other.data[row][col])
        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError(f"Cannot multiply matrices. Columns of first matrix ({self.cols}) must match rows of second matrix ({other.rows})")

        result = SparseMatrix(num_rows=self.rows, num_cols=other.cols)
        for row in self.data:
            for col in self.data[row]:
                val_a = self.data[row][col]
                if col in other.data:
                    for other_col in other.data[col]:
                        val_b = other.data[col][other_col]
                        current = result.get_element(row, other_col)
                        result.set_element(row, other_col, current + val_a * val_b)
        return result

    def save_to_file(self, file_path):
        try:
            with open(file_path, 'w') as file:
                file.write(f"rows={self.rows}\n")
                file.write(f"cols={self.cols}\n")
                for row in sorted(self.data):
                    for col in sorted(self.data[row]):
                        file.write(f"({row},{col},{self.data[row][col]})\n")
        except IOError:
            raise ValueError(f"Could not write to file: {file_path}")

    def __str__(self):
        output = [f"Sparse Matrix ({self.rows}x{self.cols}):"]
        for row in sorted(self.data):
            for col in sorted(self.data[row]):
                output.append(f"({row}, {col}): {self.data[row][col]}")
        return "\n".join(output)


def show_menu():
    print("\nMatrix Operations Menu:")
    print("1. Add two matrices")
    print("2. Subtract two matrices")
    print("3. Multiply two matrices")
    print("4. Exit")

    while True:
        try:
            choice = int(input("Enter your choice (1-4): "))
            if 1 <= choice <= 4:
                return choice
            print("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    print("Sparse Matrix Operations Program")

    file1 = "/mnt/d/xammp/htdocs/DSA/sample.txt/easy_sample_02_1.txt"
    file2 = "/mnt/d/xammp/htdocs/DSA/sample.txt/easy_sample_02_2.txt"
    output_file = "/mnt/d/xammp/htdocs/DSA/sample.txt/output.txt"

    while True:
        choice = show_menu()

        if choice == 4:
            print("Exiting program.")
            break

        try:
            matrix1 = SparseMatrix(file1)
            print(f"Matrix 1 dimensions: {matrix1.rows}x{matrix1.cols}")
            matrix2 = SparseMatrix(file2)
            print(f"Matrix 2 dimensions: {matrix2.rows}x{matrix2.cols}")

            if choice == 1:
                result = matrix1.add(matrix2)
            elif choice == 2:
                result = matrix1.subtract(matrix2)
            elif choice == 3:
                result = matrix1.multiply(matrix2)

            result.save_to_file(output_file)
            print(f"\n✅ Operation completed successfully.\n📄 Result saved to: {output_file}")

        except Exception as e:
            print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
