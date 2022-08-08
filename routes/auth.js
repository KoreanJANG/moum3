//회원 가입 

const express = require('express');
const passport = require('passport');
const bcrypt = require('bcrypt');
const { isLoggedIn, isNotLoggedIn } = require('./middlewares');
const User = require('../models/user');

const router = express.Router();

// 회원가입 라우터 부분
router.post('/join', isNotLoggedIn, async (req, res, next) => { 
  const { userid, nick, password } = req.body;  // 프론트에서 이메일 닉 비번을 보낸다
  try {
    const exUser = await User.findOne({ where: { userid } }); // 기존 존재하는 아이디 검사 
    if (exUser) {
      return res.status(400).send("error=user exist"); // 있으면? 리다이렉트 한다. error=exist 이라는 쿼리 스트링을 붙여서 리다이렉트한다. 이거를 프론트에서 보고 처리한다 
    }
    // 기존에 존재하는 아이디가 없다. 그럼 밑에 시작. 
    const hash = await bcrypt.hash(password, 12); // 비밀번호 해쉬화. 뒤에 숫자 높을수록 강도높음 
    await User.create({ // 여기서부터 새로운 유저는 생성한다 
      userid,  // 로그인 ID
      nick,  // 앱에서 보여질 별명
      password: hash,  // 비번만 해쉬화를 한다 
    });
    return res.status(200).send("ok");  // 그리고 나서 메인으로 리다이렉트 한다. 회원가입 끝.
  } catch (error) {
    console.error(error);
    return next(error);
  }
});

// 로그인은 가입보다 복잡하다. 일단 일반 로그인과 소셜 로그인은 다르고 
// 로직이 복잡해서 패스포트 라이브러리를 쓴다 
router.post('/login', isNotLoggedIn, (req, res, next) => { //프론트에서 auth/login 으로 로그인 요청(post)을 보내면 실행된다 
  console.log('/login called'); // 서버에서 직접 수정된 부분
  passport.authenticate('local', (authError, user, info) => { // 여기가 실행되면 passport가 로컬스트레티지를 찾는다 
    if (authError) {                                  // passport/index.js에서 local은 localStrategy.js를 참조하라고 정의했음 
      console.error(authError);                       // 구조적으로 중요한 것은 일단 실행하면 passport.authenticate('local' 까지만 실행되고 
      return next(authError);                         // 로컬스트레티지로 가서 한번 돌고 온다 
    }
    if (!user) {  // 로그인이 실패한 경우 
      return res.status(400)(`로그인 실패`); //${info.message}를 프폰트로 보낸다
    }
    return req.login(user, (loginError) => { // 로그인 성공한 경우. 사용자 객체를 넣어준다 
      if (loginError) {               // 이게 실행되면 passport/index.js로 간다  
        console.error(loginError);
        return next(loginError);
      }
      // 브라우저로 세션쿠키와 함께 리다이렉트 한다. 이때부터 브라우저는 로그인 상태가 된다 
      return res.status(200).send("ok");
    });
  })(req, res, next); // 미들웨어 내의 미들웨어에는 (req, res, next)를 붙입니다.
});

router.get('/logout', isLoggedIn, (req, res) => {
  req.logout();
  req.session.destroy();  // 세션쿠키를 세션에서 지운다. 세션 자체를 파괴한다 
  res.status(200).send("ok");
});

//회원정보 수정 
router.get('/update', isLoggedIn, async(req, res, next) => {
  try {
    await User.update({
      where : {
        nick: req.user.nick, 
      },
    });
    res.status(200).send("ok");
  } catch (error) {
    console.error(error);
    next(error);
  }
});

//회원탈퇴 
router.get('/delete', isLoggedIn, async(req, res, next) => {
  try {
    await User.destroy({
      where : {
        Id: req.user.id, 
      },
    });
    res.status(200).send("ok");
  } catch (error) {
    console.error(error);
    next(error);
  }
});

//카카오 로그인
router.get('/kakao', passport.authenticate('kakao'));  //카카오전략.js로 이동  

router.get('/kakao/callback', passport.authenticate('kakao', {
  failureRedirect: '/',
}), (req, res) => {
  res.status(200).send("ok");
});

//네이버로그인
router.get('/naver', passport.authenticate('naver', { authType: 'reprompt' }));  // 네이버로그인 라우터.   

// 위에서 네이버 서버 로그인이 되면, 네이버 리다이렉트 url 설정에 따라 이쪽 라우투로 온다 
router.get('/naver/callback', passport.authenticate('naver', { // 그리고 passport 로그인 전략에 의해 naverStrategy로 가서 카카오계정 정보와 DB를 비교해서 회원가입시키거나 로그인 처리하게 한다
  failureRedirect: '/',
}), (req, res) => {
  res.status(200).send("ok");
});

module.exports = router;
