const passport = require('passport');
const KakaoStrategy = require('passport-kakao').Strategy;

const User = require('../models/user');

// 카카오 로그인 
module.exports = () => {
  passport.use(new KakaoStrategy({
    clientID: process.env.KAKAO_ID,
    callbackURL: '/auth/kakao/callback',
  }, async (accessToken, refreshToken, profile, done) => {  // 오스2 에서 사용한다. 오스2를 따로 공부한다 
    console.log('kakao profile', profile);
    try {
      const exUser = await User.findOne({  // 기존 카카오 가입자인지 찾아보고 
        where: { snsId: profile.id, provider: 'kakao' }, 
      });
      if (exUser) {  // 있으면 통과 
        done(null, exUser);
      } else {  // 없으면 가입시킨다. 소셜 로그인은 로그인, 가입 같이 처리한다  
        const newUser = await User.create({
          email: profile._json && profile._json.kakao_account_email,
          nick: profile.displayName,
          snsId: profile.id,
          provider: 'kakao',
        });
        done(null, newUser);
      }
    } catch (error) {
      console.error(error);
      done(error);
    }
  }));
};
