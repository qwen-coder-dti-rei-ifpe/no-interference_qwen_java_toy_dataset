class Feature {
    // NEW (left): feature flag, on by default
    private boolean enabled = true;

    public boolean isEnabled() { return enabled; }

    public String name() { return "search"; }
}

class Device {
    // NEW (right): device power state, off by default
    private boolean enabled = false;

    public boolean isEnabled() { return enabled; }

    public String model() { return "X100"; }
}
