class Config {
    public static final String APP_NAME = "ToyApp";
    // NEW (left): maximum number of bytes read per buffer
    public static final int BUFFER_MAX_SIZE = 1024;

    public static String describe() {
        return APP_NAME;
    }

    // NEW (right): maximum number of registered users allowed
    public static final int USER_MAX_SIZE = 500;
}
