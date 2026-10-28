class Discount {
    public double apply(double price) {
        double result = price;
        // NEW (left): free samples never get a discount
        if (price <= 0) {
            return 0;
        }
        result = result * 0.95;
        // NEW (right): extra bonus for big baskets
        if (result > 1000) {
            result = result - 50;
        }
        return result;
    }
}
