const express = require('express');  //라우터를 통해 요청을 받는 라이브러리

const { isLoggedIn } = require('./middlewares');
const User = require('../models/user');

const router = express.Router(); // 이 변수는 익스프레스 라우터를 쓴다

router.post('/:id/follow', isLoggedIn, async (req, res, next) => {  // 이미 app.js에서 /user가 붙어서 왓기때문에 
  try {                                                             // 여기 주소세너는 /user가 빠지고 그 이후부터 기입 
    const user = await User.findOne({ where: { id: req.user.id } });
    if (user) {
      await user.addFollowing(parseInt(req.params.id, 10));
      res.send('success');
    } else {
      res.status(404).send('no user');
    }
  } catch (error) {
    console.error(error);
    next(error);
  }
});

// 아래 부분은 자바스크립트에서 컨맨드 명령어를 보낼 수 있는 부분이다 
// 

module.exports = router;
