describe("navigation", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("opens the card sets page from the side menu", () => {
    cy.get("[data-cy='nav-card-sets']").click();
    cy.get("[data-cy='study-set-header']").should("contain", "Study Set Library");
  });

  it("opens the about page from the side menu", () => {
    cy.get("[data-cy='nav-about']").click();
    cy.get("[data-cy='about_page']").should("contain", "About Study Night");
  });

  it("opens the home page from the side menu", () => {
    cy.get("[data-cy='nav-about']").click();
    cy.get("[data-cy='nav-home']").click();
    cy.get("[data-cy='home_header']").should("contain", "Study Night");
  });
});
