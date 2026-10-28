class Monitor {
    public double average(double[] v) {
        double sum = 0;
        for (double x : v) sum += x;
        return sum / v.length;
    }

    // NEW (left): alert when the average CPU load is too high
    public boolean cpuAlert(double[] loads) {
        double threshold = 80.0;
        return average(loads) > threshold;
    }

    // NEW (right): alert when the average memory usage is too high
    public boolean memAlert(double[] usage) {
        double threshold = 90.0;
        return average(usage) > threshold;
    }
}
