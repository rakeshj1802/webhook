const express = require('express');
const app = express();
const bodyParser = require('body-parser');

const VERIFY_TOKEN = "POSTBOT123"; // Use this exact token in Meta dashboard

app.use(bodyParser.json());

app.get('/webhook', (req, res) => {
  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];

  if (mode === 'subscribe' && token === VERIFY_TOKEN) {
    console.log("✅ Verified Webhook with Meta");
    res.status(200).send(challenge);
  } else {
    console.log("❌ Failed Verification");
    res.sendStatus(403);
  }
});

app.post('/webhook', (req, res) => {
  console.log("📩 Webhook Event:");
  console.log(JSON.stringify(req.body, null, 2));
  res.sendStatus(200);
});

const listener = app.listen(process.env.PORT, () => {
  console.log('✅ Webhook live on port ' + listener.address().port);
});
