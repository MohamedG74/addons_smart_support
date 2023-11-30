var express = require('express');
var router = express.Router();

router.get('/customers', function (req, res, next) {
    req.getConnection(function (err, connection) {
        var query = connection.query('SELECT * FROM customer', function (err, rows) {
            if (err)
                var error = ("Error Selecting : %s ", err);

            res.setHeader('Content-Type', 'application/json');
            res.send(JSON.stringify(rows));
        });
    });
});


module.exports = router;