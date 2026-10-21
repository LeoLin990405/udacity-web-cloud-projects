describe("forms", () => {
  beforeEach(() => {
    cy.visit("/");
    cy.get("[data-cy='nav-card-sets']").click();
  });

  it("creates a new study set when the set form receives valid input", () => {
    cy.get("[data-cy='toggle_form']").click();
    cy.get("[data-cy='titleInput']").type("Biology Review");
    cy.get("[data-cy='submit-set']").click();
    cy.contains("Biology Review").should("exist");
  });

  it("shows an error when the set form is submitted empty", () => {
    cy.get("[data-cy='toggle_form']").click();
    cy.get("[data-cy='submit-set']").click();
    cy.get(".error").should("contain", "TITLE CANNOT BE EMPTY");
  });

  it("creates a new card when the card form receives valid input", () => {
    cy.get("[data-cy='1']").click();
    cy.get("[data-cy='toggle_form']").click();
    cy.get("[data-cy='termInput']").type("DOM");
    cy.get("[data-cy='descriptionInput']").type("Document Object Model");
    cy.get("[data-cy='add-card']").click();
    cy.contains("DOM").should("exist");
  });

  it("shows an error when the card form is submitted empty", () => {
    cy.get("[data-cy='1']").click();
    cy.get("[data-cy='toggle_form']").click();
    cy.get("[data-cy='add-card']").click();
    cy.get(".error").should("contain", "TERM AND DESCRIPTION CANNOT BE EMPTY");
  });
});
