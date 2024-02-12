import java.util.Arrays;

public class Matrix {
    private double[][] matrix;

    public Matrix(double[][] matrix) {
        this.matrix = matrix;
    }

    public Matrix transpose() {
        // TODO: Check if its faster to not copy and loop over more of the matrix instead
        double[][] transposed = deepCopy();

        for (int row = 0; row < matrix.length; row++) {
            for (int col = row; col < matrix[row].length; col++) {
                transposed[row][col] = matrix[col][row];
                transposed[col][row] = matrix[row][col];
            }
        }

        return new Matrix(transposed);
    }

    public Matrix multiply(Matrix other, Oblig2Precode.Mode mode) {
        switch (mode) {
            case SEQ_NOT_TRANSPOSED:
                return multiplySequential(other);

            case SEQ_A_TRANSPOSED:
                Matrix seq_this_transposed = transpose();
                return seq_this_transposed.multiplySequential(other);

            case SEQ_B_TRANSPOSED:
                Matrix seq_other_transposed = other.transpose();
                return multiplySequential(seq_other_transposed);

            case PARA_NOT_TRANSPOSED:
                return multiplyParallel(other);

            case PARA_A_TRANSPOSED:
                Matrix para_this_transposed = transpose();
                return para_this_transposed.multiplyParallel(other);

            case PARA_B_TRANSPOSED:
                Matrix para_other_transposed = other.transpose();
                return multiplyParallel(para_other_transposed);

            default:
                throw new EnumConstantNotPresentException(mode.getClass(), mode.getClass().getName());
        }
    }

    private Matrix multiplySequential(Matrix other) {
        Matrix out = new Matrix(Arrays.copyOf(matrix, matrix.length));

        for (int row = 0; row < matrix.length; row++) {
            for (int col = 0; col < matrix[row].length; col++) {
                for (int otherRow = 0; otherRow < other.matrix.length; otherRow++) {
                    out.matrix[row][col] += matrix[row][col] * other.matrix[otherRow][col];
                }
            }
        }

        return out;
    }

    private Matrix multiplyParallel(Matrix other) {
        return other;
    }

    private double[][] deepCopy() {
        double[][] copied = new double[matrix.length][matrix[0].length];

        for (int i = 0; i < matrix.length; i++) {
            copied[i] = Arrays.copyOf(matrix[i], matrix[i].length);
        }

        return copied;
    }

    public void print() {
        for (int i = 0; i < matrix.length; i++) {
            System.out.println(Arrays.toString(matrix[i]));
        }
    }
}
