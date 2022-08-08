const express = require('express');
const cookieParser = require('cookie-parser');//쿠키를 알아서 파싱해준다 
const morgan = require('morgan');  // 응답과 요청을 기록. "GET / 304 70.580 ms - - " 이런거 뜨게 한다 
const path = require('path');  // 경로처리할때 쓴다
const session = require('express-session'); // 개인의 요청을 저장한다??.....??....이 부분 다시 공부할 것 
const nunjucks = require('nunjucks');
const dotenv = require('dotenv');
const passport = require('passport');  // 각종 페키지를 가져온다 


dotenv.config();  // dotenv 이거는 리콰이어 끝나고 바로 적어줘라. 이게 밑에 있으면 위에거는 참조 못한다 

const pageRouter = require('./routes/page'); // 라우터다. 변수를 지정했고, 해당 위치의 파일을 라우터 한다. 소스 밑에 app.use로 사용한다 
const authRouter = require('./routes/auth');  // 회원가입, 로그인 라우터
const postRouter = require('./routes/post');
const userRouter = require('./routes/user');
const { sequelize } = require('./models');  // 모델스로 부터 시퀄라이즈할 내용들을 참조한다 
const passportConfig = require('./passport');

const app = express(); //보통 app.set이 가장먼저 나온다. 그리고 공통미들웨어, 그리고 라우터, 범위가 넓은 라우터, 에러 순으로 작성 
passportConfig(); // 패스포트 설정
app.set('port', process.env.PORT || 8001);  // 아직 개발 버전 
app.set('view engine', 'html');  // 뷰 엔진 
nunjucks.configure('views', { // 넌적스를 써서 템플릿을 만들겠다 
  express: app,
  watch: true,  // 현재 템플릿은 넌적스 쓴다. 여기는 넌적스 정의하느 부분
});
sequelize.sync({ force: false }) //true로 하면 서버킬때마다 테이블이 새로 생성된다. 데이터 날라간다
                               // force대신 alter쓰면 데이터 그대로 두고 컬럼명만 바꿀 수 있는데 에러 많이 난다. 
                              // force: false 이거를 그냥 기본적으로 써라 
  .then(() => {  // db싱크가 성공하면 시뭘라이즈 실행하여 db를 만들던지 한다 
    console.log('데이터베이스 연결 성공');
   })
  .catch((err) => {
    console.error(err);
  });

app.use(morgan('combined'));  // dev쓰면 간결하게 combined 쓰면 상세하게 나온다. combined 이거는 배포 올라갈때 쓴다 
app.use(express.static(path.join(__dirname, 'public')));  // 퍼블릭 폴더에 css가 들어간다. 전체 주석처리해놈 
app.use('/img', express.static(path.join(__dirname, 'uploads')));
app.use(express.json());  // 필수. 클라이언트에서 제이슨을 받으면 바디에 제이슨으로 꽂아준다 
app.use(express.urlencoded({ extended: false })); // 필수. 클라이언트에서 폼을 보낼 때 파싱해준다. 이미지나 파일은 처리 못한다. 그럴때는 멀터를 쓴다 
app.use(cookieParser(process.env.COOKIE_SECRET));
app.use(session({
  resave: false,
  saveUninitialized: false,
  secret: process.env.COOKIE_SECRET,
  cookie: {
    httpOnly: true,
    secure: false,
  },
}));
app.use(passport.initialize()); // 
app.use(passport.session());

// 요청을 받으면 아래의 라우터를 통해 넘긴다
app.use('/', pageRouter);     // page.js 가 거의 인덱스나 메인 부분인것 같다 
app.use('/auth', authRouter);
app.use('/post', postRouter);
app.use('/user', userRouter);

app.use((req, res, next) => {  //라우터에서 요청을 처리할 수 없는 경우 아래가 실행. 이때 미들웨어 쪽은 꼭 next 붙여야 한다 
  const error =  new Error(`${req.method} ${req.url} 라우터가 없습니다.`);
  error.status = 404;
  next(error); // 에러 미들웨어로 넘긴다 
});

app.use((err, req, res, next) => {  // 에러 처리 미들웨어. 꼭 next 를 넣어줘야 에러 미들웨어가 된다 
  res.locals.message = err.message;
  res.locals.error = process.env.NODE_ENV !== 'production' ? err : {};   // 배포모드에서는 안보인다 
  res.status(err.status || 500);
  res.render('error');
});

app.listen(app.get('port'), () => {
  console.log(app.get('port'), '번 포트에서 대기중');
});
