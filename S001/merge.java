class Inventory {
    private int stock = 0;

    public void setStock(int s) { this.stock = s; }
    public int getStock() { return stock; }

    // NEW (right): validate that an order quantity fits in stock
    public boolean isValid(int qty) {
        return qty > 0 && qty <= stock;
    }

    // NEW (left): validate that the stock itself is not negative
    public boolean isValid() {
        return stock >= 0;
    }
}
