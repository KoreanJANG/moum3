const passport = require('passport');
const { Strategy: NaverStrategy, Profile: NaverProfile } = require('passport-naver-v2');
const User = require('../models/user');

// 네이버 로그인 
module.exports = () => {
  passport.use(new NaverStrategy({
    clientID: process.env.NAVER_ID,
    clientSecret: process.env.NAVER_SECRET,
    callbackURL: '/auth/naver/callback',
  }, async (accessToken, refreshToken, profile, done) => {  // 오스2 에서 사용한다. 오스2를 따로 공부한다 
    console.log('naver profile :', profile);
    try {
      const exUser = await User.findOne({  // 네이버 플랫폼에서 로그인 했고 & snsid필드에 네이버 아이디가 일치할경우
        where: { snsid: profile.id, provider: 'naver' }, 
      });
      if (exUser) {  // 있으면 통과 
        done(null, exUser);
      } else {  // 없으면 가입시킨다. 소셜 로그인은 로그인, 가입 같이 처리한다  
        const newUser = await User.create({
          email: profile.email,
          nick: profile.name,
          snsid: profile.id,
          mobile: profile.mobile,
          birthday: profile.birthday,
          age: profile.age,
          provider: 'naver',
        });
        done(null, newUser);
      }
    } catch (error) {
      console.error(error);
      done(error);
    }
  }));
};
