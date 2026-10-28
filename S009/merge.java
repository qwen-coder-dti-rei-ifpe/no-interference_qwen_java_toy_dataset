class Tax {
    public double taxA(double income) {
        return income * 0.10;
    }

    public double taxB(double income) {
        return income * 0.10;
    }

    // REFACTOR (left): single place for the rate
    private double rate(double income) {
        return income * 0.10;
    }

    // NEW (right): surcharge applied to high incomes
    public double surcharge(double income) {
        return income * 0.10;
    }
}
