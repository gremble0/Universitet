import java.util.Arrays;
import java.util.Random;

class KLargestNumbersParallel {
    static final int cores = Runtime.getRuntime().availableProcessors();
    static Thread[] threads = new Thread[cores];

    public static void main(String[] args) {
        if (args.length != 2) {
            System.out.println("usage: java KLargestNumbersParallel <int:numsLen> <int:k>");
            return;
        }

        final int numsLen = Integer.parseInt(args[0]);
        int k = Integer.parseInt(args[1]);

        Random r = new Random(7363);
        int[] randNums = new int[numsLen];
        for (int i = 0; i < numsLen; i++) {
            randNums[i] = r.nextInt();
        }

        // Special algorithm won't do anything if k is >= numsLen so just
        // insertion sort the whole list in descending order and call it a day
        if (k >= numsLen) {
            insertSortDesc(randNums, 0, numsLen - 1);
            return;
        }

        findKLargest(randNums, k);
    }

    /**
     * Move the k largest elements in an array to its front in place
     *
     * @param nums array to search through
     * @param effectiveK number of elements to find
     */
    private static void findKLargest(int[] nums, int k) {
        final int intervalSize = nums.length / cores;
        // If the intervalSize is greater than k we would index outside the array
        // if we tried using the normal k, so in this case just use intervalSize as k
        final int effectiveK = Math.min(k, intervalSize);

        class KLargestInInterval implements Runnable {
            private final int start;
            private final int end;

            public KLargestInInterval(int start, int end) {
                this.start = start;
                this.end = end;
            }

            public void run() {
                insertSortDesc(nums, start, start + effectiveK);

                for (int i = start + effectiveK; i < end; i++) {
                    if (nums[i] > nums[start + effectiveK]) {
                        nums[start + effectiveK] = nums[i];
                        insertSortDesc(nums, start, start + effectiveK);
                    }
                }
            }
        }

        int start = 0;
        int end = intervalSize;
        for (int i = 0; i < cores - 1; i++) {
            threads[i] = new Thread(new KLargestInInterval(start, end));
            threads[i].start();

            start += intervalSize;
            end += intervalSize;
        }
        // Last thread searches to the end of the array in case nums.length % cores > 0
        // TODO: make the first core have more to do than the last to optimize
        threads[cores - 1] = new Thread(new KLargestInInterval(start, nums.length - 1));
        threads[cores - 1].start();

        try {
            for (int i = 0; i < threads.length; i++) {
                threads[i].join();
            }
        } catch(Exception e) {
            System.out.println(e);
            System.exit(1);
        }

        int[] biggest = new int[k];

        start = 0;
        for (int i = 0; i < threads.length; i++) {
            for (int j = 0; j < effectiveK; j++) {
                if (nums[j + start] > biggest[biggest.length - 1]) {
                    biggest[biggest.length - 1] = nums[j + start];
                    insertSortDesc(biggest, 0, biggest.length - 1);
                }
            }
            start += intervalSize;
        }

        for (int i = 0; i < biggest.length; i++) {
            nums[i] = biggest[i];
        }
    }

    /**
     * In place insertion sort in descending order within a given range
     *
     * @param nums array to sort
     * @param start lower range
     * @param end upper range
     */
    private static void insertSortDesc(int[] nums, int start, int end) {
        int j, t;
        for (int i = start; i < end; i++) {
            t = nums[i + 1];
            j = i;
            while (j >= start && nums[j] < t) {
                nums[j + 1] = nums[j];
                j--;
            }
            nums[j + 1] = t;
        }
    }
}
