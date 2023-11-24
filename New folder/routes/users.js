var express = require('express');
var router = express.Router();
var authentication_mdl = require('../middleware/authentication');
var session_store;

router.get('/', authentication_mdl.is_login, function (req, res, next) {
    req.getConnection(function (err, connection) {
        var query = connection.query('SELECT * FROM user', function (err, rows) {
            if (err)
                var error = ("Error Selecting : %s ", err);

            req.flash('msg_error', error);
            res.render('users/list', { title: "Users", data: rows, session_store: req.session});
        });
    });
});

router.post('/add', authentication_mdl.is_login, function (req, res, next) {
  req.check('email', 'Please fill the email').notEmpty();
  req.check('password', 'Please fill the password').notEmpty();
  var errors = req.validationErrors();
  if (!errors) {

      v_email = req.sanitize('email').escape().trim();
      v_password = req.sanitize('password').escape().trim();

      var user = {
          email: v_email,
          password: v_password
      }
      
      var insert_sql = "INSERT INTO user (id, email, password, created) VALUES (NULL, '" + user.email + "', MD5('" + user.password + "'), CURRENT_TIMESTAMP)";
      req.getConnection(function (err, connection) {
          var query = connection.query(insert_sql, function (err, result) {
              if (err) {
                  var errors_detail = ("Something went wrong. Error: %s ", err);
                  req.flash('msg_error', errors_detail);
                  res.render('users/add',
                      {
                          email: req.param('email'),
                          password: req.param('password'),
                      });
              } else {
                  req.flash('msg_info', 'User created with success');
                  res.redirect('/users');
              }
          });
      });
  } else {
      console.log(errors);
      errors_detail = "Sorry there are errors <ul>";

      for (i in errors) {
          error = errors[i];
          errors_detail += '<li>' + error.msg + '</li>';
      }

      errors_detail += "</ul>";
      req.flash('msg_error', errors_detail);
      res.render('users/add',
          {
              email: req.param('email')
          });
  }

});

router.get('/add', authentication_mdl.is_login, function (req, res, next) {
  res.render('users/add',
      {
          title: 'Add New User',
          email: '',
          password: '',
          session_store: req.session
      });
});

router.delete('/delete/(:id)', authentication_mdl.is_login, function(req, res, next) {
	req.getConnection(function(err,connection){
		var user = {
			id: req.params.id,
		}
		
		var delete_sql = 'delete from user where ?';
		req.getConnection(function(err,connection){
			var query = connection.query(delete_sql, user, function(err, result){
				if(err)
				{
					var errors_detail  = ("Error Delete : %s ",err);
					req.flash('msg_error', errors_detail); 
					res.redirect('/users');
				}
				else{
					req.flash('msg_info', 'User deleted'); 
					res.redirect('/users');
				}
			});
		});
	});
});

module.exports = router;
