// routes/invoice_search.js

const express = require('express');
const router = express.Router();

router.get('/', function (req, res, next) {
  res.render('invoice_search/invoice_search', {
    title: 'Invoice Search'
  });
});


router.post('/', function (req, res, next) {
  // For now, respond with a static message
  res.status(200).send('INV/25105');
});
module.exports = router;
