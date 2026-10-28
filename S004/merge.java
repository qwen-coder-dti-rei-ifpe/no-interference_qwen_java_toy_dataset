class Report {
    public String title() {
        return "Quarterly report";
    }

    // NEW (right): format an amount with a currency symbol
    public String format(double value) {
        return "$" + String.format("%.2f", value);
    }

    // NEW (left): format a day/month/year date
    public String format(int d, int m, int y) {
        return d + "/" + m + "/" + y;
    }
}
