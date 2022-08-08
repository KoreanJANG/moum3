const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;
const bcrypt = require('bcrypt');

const User = require('../models/user');

//이메일과 비번으로 로그인
module.exports = () => {
  passport.use(new LocalStrategy({
    usernameField: 'userid',  // 프론트에서 req.body.userid 로 보내주어야 한다 
    passwordField: 'password', // 프론트에서 req.body.password 로 해야 한다 
  }, async (userid, password, done) => {
    try {
      const exUser = await User.findOne({ where: { userid } }); //기존에 존재하는 이메일이 있나 찾아보고 
      if (exUser) { // 있는사람 처리 
        const result = await bcrypt.compare(password, exUser.password); //입력된 비번과 실제유저의 비번과 해쉬된 채 비교
        if (result) {
          done(null, exUser);
        } else {  // 이메일이 있으면 비번 체크 
          done(null, false, { message: '비밀번호가 일치하지 않습니다.' });
        }
      } else {  // 이메일이 없어 
        done(null, false, { message: '가입되지 않은 회원입니다.' }); // done의 행동은 나중에 다시봐라...
      }
    } catch (error) {
      console.error(error);
      done(error);
    }
  }));
};
