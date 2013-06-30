/**
 * Top level YoLingo namespace
 * @type {{}}
 */
var Y = {};
(function () {
  Kinvey.init({
    'appKey': 'kid_VPu3mrdS15',
    'appSecret': 'a6d98ed415c940f2972da26528c7accb'
  });

  Y.user = {};
  Y.user.create = function (username, password, email, callback) {
    Kinvey.User.create({
      username: username,
      password: password,
      email: email
    }, {
      success: function (user) {
        // user is the created user, which is now logged in.
        callback(null, user);
      },
      error: function (e) {
        // Failed to create the user.
        // e holds information about the nature of the error.
        callback(e);
      }
    });
  };

  /**
   * Call this after created user.
   *
   * @param callback
   */
  Y.user.verifyEmail = function (callback) {
    var user = Kinvey.getCurrentUser();
    if (null !== user) {
      Kinvey.User.verifyEmail(user.getUsername(), {
        success: function () {
          // Email was sent.
          callback(null, 'Verification sent.');
        },
        error: function (e) {
          // Failed to send verification email.
          // e holds information about the nature of the error.
          callback(e);
        }
      });
    } else {
      callback('User not logged in.');
    }
  };

  Y.user.login = function (username, password, callback) {
    var myUser = new Kinvey.User();
    myUser.login(username, password, {
      success: function (user) {
        // user is the logged in user instance.
        callback(null, user);
      },
      error: function (e) {
        // Failed to login the user.
        // e holds information about the nature of the error.
        callback(e);
      }
    });
  };

  Y.user.getCurrent = function (callback) {
    var user = Kinvey.getCurrentUser();
    if (null !== user) {
      callback(null, user);
    } else {
      callback('User not logged in.');
    }
  };

  Y.article = {};
  Y.article.create = function (doc, callback) {
    var article = new Kinvey.Entity(doc, 'articles');
    article.save({
      success: function (article) {
        callback(null, article);
      },
      error: function (e) {
        callback(e);
      }
    });
  };

  Y.article.get = function (articleId, callback) {
    var article = new Kinvey.Entity({}, 'articles');
    article.load(articleId, {
      success: function (article) {
        callback(null, article);
      },
      error: function (e) {
        callback(e);
      }
    });
  };

  Y.article.list = function (callback) {
    var articleColl = new Kinvey.Collection('articles');
    articleColl.fetch({
      success: function (list) {
        callback(null, list);
      },
      error: function (e) {
        callback(e);
      }
    });
  };

  Y.word = {};
  Y.word.create = function (doc, callback) {

  };

}());