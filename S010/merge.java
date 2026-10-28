class UserBuilder {
    private String name = "";
    private String email = "";

    /* NEW (left): trim names to avoid leading spaces */
    public UserBuilder name(String n) { this.name = n.trim(); return this; }

    public String describeClass() {
        return "UserBuilder";
    }

    public UserBuilder email(String e) { this.email = e; return this; }
    /* NEW (right): lowercase emails to avoid duplicate accounts */
    public UserBuilder normaliseEmail(String e) {
        this.email = e.toLowerCase();
        return this;
    }

    public String build() {
        return name + " <" + email + ">";
    }
}
