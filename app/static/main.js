async function play(move) {
  const resp = await fetch('/play', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ move })
  });
  const data = await resp.json();
  if (data.error) {
    document.getElementById('status').textContent = data.error;
    return;
  }

  const status = document.getElementById('status');
  const detail = document.getElementById('detail');
  status.textContent = describeResult(data.result);
  detail.textContent = `You: ${data.user}  |  Computer: ${data.computer}`;

  document.getElementById('wins').textContent = data.score.wins;
  document.getElementById('losses').textContent = data.score.losses;
  document.getElementById('ties').textContent = data.score.ties;
}

function describeResult(result) {
  if (result === 'win') return 'You win!';
  if (result === 'lose') return 'You lose.';
  return "It's a tie.";
}

document.querySelectorAll('.choice').forEach(btn => {
  btn.addEventListener('click', () => play(btn.dataset.move));
});

document.getElementById('reset').addEventListener('click', async () => {
  await fetch('/reset', { method: 'POST' });
  document.getElementById('wins').textContent = 0;
  document.getElementById('losses').textContent = 0;
  document.getElementById('ties').textContent = 0;
  document.getElementById('status').textContent = 'Make your move';
  document.getElementById('detail').textContent = '';
});

