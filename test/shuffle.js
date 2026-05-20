import { expect } from "chai";
import { shuffle } from "../src/shuffle.js";

describe("shuffle", () => {
  it("returns a new array with the same cards", () => {
    const cards = [
      { term: "HTML", description: "HyperText Markup Language" },
      { term: "CSS", description: "Cascading Style Sheets" },
      { term: "JS", description: "JavaScript" },
    ];
    const shuffled = shuffle(cards);

    expect(shuffled).to.have.length(cards.length);
    expect(shuffled).to.have.deep.members(cards);
    expect(shuffled).to.not.equal(cards);
  });

  it("can rearrange indexes of an array", () => {
    const originalRandom = Math.random;
    Math.random = () => 0;

    const cards = ["first", "second", "third", "fourth"];
    const shuffled = shuffle(cards);

    Math.random = originalRandom;

    expect(shuffled).to.deep.equal(["second", "third", "fourth", "first"]);
  });
});
