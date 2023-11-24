require('dotenv').config();

const express = require('express');
const path = require('path');
const favicon = require('serve-favicon');
const logger = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const flash = require('express-flash');
const session = require('express-session');
const index = require('./routes/index');
const users = require('./routes/users');
const customers = require('./routes/customers');
const api = require('./routes/api');
const invoicesearch = require('./routes/invoice_search');


const expressValidator = require('express-validator');
const methodOverride = require('method-override');
const connection = require('express-myconnection');
const mysql = require('mysql2');
const app = express();

const PORT = process.env.PORT || 3000;

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(session({ secret: "secretpass123456" }));
app.use(flash());
app.use(expressValidator());
app.use(methodOverride(function (req, res) {
  if (req.body && typeof req.body == 'object' && '_method' in req.body) {
    var method = req.body._method;
    delete req.body._method;
    return method;
  }
}));

app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use(
  connection(mysql, {
    host: process.env.DBHOST,
    user: process.env.DBUSER,
    password: process.env.DBPASS,
    port: process.env.DBPORT,
    database: process.env.DBNAME,
  }, 'pool') //single, pool, request
);

app.use('/', index);
app.use('/customers', customers);
app.use('/users', users);
app.use('/api', api);
app.use('/invoice_search', invoicesearch);



// catch 404 and forward to error handler
app.use(function (req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});

module.exports = app;