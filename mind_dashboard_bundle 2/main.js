const app = document.getElementById('app');

function createCard(gpt) {
  const card = document.createElement('div');
  card.className = 'card';

  const title = document.createElement('h2');
  title.textContent = gpt.name;

  const state = document.createElement('p');
  state.textContent = `Status: ${gpt.status}`;

  card.appendChild(title);
  card.appendChild(state);

  return card;
}

data.gpts.forEach(gpt => {
  app.appendChild(createCard(gpt));
});