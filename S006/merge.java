class Order {
    private double total = 0;

    public void addItem(double price) {
        // NEW (right): count the item before touching the total
        countItem();
        total = total + price;
        // NEW (left): log the item once the total is updated
        logItem(price);
    }

    private void logItem(double price) {
        System.out.println("item added, total now " + price);
    }

    private void countItem() {
        System.out.println("counter updated");
    }

    public double getTotal() { return total; }
}
