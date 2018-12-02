const User = require('../models').users;
const passport = require('passport');
const TwitterStrategy = require('passport-twitter').Strategy;
const config = require('../config');
const token = require('../helpers/token');

const twitterOptions = { ...config.auth.twitter, passReqToCallback: true };

passport.use(
  new TwitterStrategy(
    twitterOptions,
    async (req, token, tokenSecret, profile, done) => {
      let user = await User.find({ where: { twitter: profile.id } });
      if (!user) {
        user = User.create({
          twitter: profile.id,
          username: profile.username,
          name: profile.displayName,
          email: profile.emails[0].value
        });
      }
      done(null, user);
    }
  )
);

passport.serializeUser((user, done) => done(null, user));
passport.deserializeUser((user, done) => done(null, user));

module.exports = app => {
  app.get('/auth/twitter', passport.authenticate('twitter'));
  app.get(
    '/auth/twitter/callback',
    passport.authenticate('twitter', { failureRedirect: '/login' }),
    handleSocialAuth
  );
};

const handleSocialAuth = (req, res) => {
  if (!req.user) {
    return res.send('Unauthorized');
  }
  return res.send({
    token: token.generate({ id: req.user.id }, config.auth.tokenLifeTime)
  });
};
