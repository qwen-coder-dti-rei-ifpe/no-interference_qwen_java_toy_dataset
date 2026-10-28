class Order {
    private double total = 0;

    public void addItem(double price) {
        total = total + price;
    }


    public double getTotal() { return total; }
}
