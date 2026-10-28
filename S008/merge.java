class WeekdayName {
    public static String of(int day) {
        switch (day) {
            case 1: return "Monday";
            case 2: return "Tuesday";
            // NEW (left): support Wednesday
            case 3: return "Wednesday";
            default: return "unknown";
            // NEW (right): support the weekend
            case 6: return "Saturday";
            case 7: return "Sunday";
        }
    }
}
