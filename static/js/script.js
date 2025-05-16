document.getElementById('compiler-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  const code = document.getElementById('code').value;

  const response = await fetch('/compile', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ code }),
  });

  const result = await response.text();
  document.getElementById('output').textContent = result;
});
