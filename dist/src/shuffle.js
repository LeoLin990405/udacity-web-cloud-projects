const shuffle = (cards) => {
  let current = cards.length;
  const newCardsArray = [...cards];

  while (current !== 0) {
    const randomIndex = Math.floor(Math.random() * current);
    current -= 1;

    [newCardsArray[current], newCardsArray[randomIndex]] = [
      newCardsArray[randomIndex],
      newCardsArray[current],
    ];
  }

  return newCardsArray;
};

export { shuffle };
