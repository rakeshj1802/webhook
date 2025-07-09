const express = require('express');
const app = express();

app.use(express.json());

app.get('/', (req, res) => {
  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];

  const VERIFY_TOKEN = 'POSEBOT123'; // Must match your Facebook token exactly

  if (mode && token) {
    if (mode === 'subscribe' && token === VERIFY_TOKEN) {
      console.log('Webhook Verified Successfully!');
      res.status(200).send(challenge);  // Send challenge back to Facebook
    } else {
      res.sendStatus(403);  // Forbidden - Wrong token
    }
  } else {
    res.sendStatus(400);  // Bad Request - Missing params
  }
});

app.post('/', (req, res) => {
  console.log('Received Instagram Message:', req.body);
  res.sendStatus(200);  // Always acknowledge messages with 200
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Webhook server running on port ${PORT}`);
});
