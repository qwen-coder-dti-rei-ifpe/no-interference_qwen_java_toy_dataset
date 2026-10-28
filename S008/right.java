class WeekdayName {
    public static String of(int day) {
        switch (day) {
            case 1: return "Monday";
            case 2: return "Tuesday";
            default: return "unknown";
        }
    }
}
