class UserBuilder {
    private String name = "";
    private String email = "";


    public String describeClass() {
        return "UserBuilder";
    }

    public UserBuilder email(String e) { this.email = e; return this; }

    public String build() {
        return name + " <" + email + ">";
    }
}
