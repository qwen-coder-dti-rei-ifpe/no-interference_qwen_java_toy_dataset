class Discount {
    public double apply(double price) {
        double result = price;
        result = result * 0.95;
        return result;
    }
}
