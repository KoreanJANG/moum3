const passport = require('passport');
const local = require('./localStrategy');
const kakao = require('./kakaoStrategy');
const naver = require('./naverStrategy'); // 네이버서버로 로그인할때
const User = require('../models/user');

// 여기서는 로그인을 어떻게 할 지 정의한다. 이때 전략이라는 표현을 쓴다.
module.exports = () => {
  passport.serializeUser((user, done) => {  // req login에서 넘어온 유저를 가지고 
    done(null, user.id);  // id만 뽑아서 던 을 해준다. 그래서 세션에 유저의 id만 저장 
  });  // 그런데...실무에서는 메모리 용 DB가 따로 있다. 15강에서 한다 

  passport.deserializeUser((id, done) => {  // 유저의 id를 세션에 저장하게 되면 어떤 시리얼 넘버(세션쿠키)가 나오고 그 시리얼 넘버와 
    User.findOne({                        // id를 비교하여 해당 사용자인지 판단한다 
      where: { id },
      include: [{
        model: User,
        attributes: ['id', 'nick'],
        as: 'Followers',
      }, {
        model: User,
        attributes: ['id', 'nick'],
        as: 'Followings',
      }],
    })
      .then(user => done(null, user))
      .catch(err => done(err));
  });

  local();
  kakao();
  naver();
};
