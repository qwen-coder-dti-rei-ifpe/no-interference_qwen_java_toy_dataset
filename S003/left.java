class Monitor {
    public double average(double[] v) {
        double sum = 0;
        for (double x : v) sum += x;
        return sum / v.length;
    }
}
