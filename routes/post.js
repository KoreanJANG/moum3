const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const Sequelize = require('sequelize');
const Op = Sequelize.Op

const { Post, Hashtag, Comment, User, Trend, Like, Trendcomment } = require('../models');
const { isLoggedIn } = require('./middlewares');
const {spawn} = require("child_process");

const router = express.Router();

try {  // 업로드 폴더 생성  
  fs.readdirSync('uploads');
} catch (error) {
  console.error('uploads 폴더가 없어 uploads 폴더를 생성합니다.');
  fs.mkdirSync('uploads');
}

// aws s3 를 활용한 이미지 업로드는 나중에 한다 
// AWS.config.update({
//   accessKeyId: process.env.S3_ACCESS_KEY_ID,
//   secretAccessKey: process.env.S3_SECRET_ACCESS_KEY,
//   region: 'ap-northeast-2',
// });


// S3로 이미지 업로드(에러난다....)
// const upload = multer({
//   storage: multerS3({
//     s3: new AWS.S3(),
//     bucket: 'moumimg',
//     key(req, file, cb) {
//       cb(null, `original/${Date.now()}${path.basename(file.originalname)}`);
//     },
//   }),
//   limits: { fileSize: 5 * 1024 * 1024 },
// });

//로컬에서 이미지 업로드(구버전)
// const upload = multer({
//   storage: multer.diskStorage({
//     destination(req, file, cb) {
//       cb(null, 'uploads/');  // 업로드 폴더에 이미지를 저장하겟다 
//     },
//     filename(req, file, cb) {
//       const ext = path.extname(file.originalname);
//       cb(null, path.basename(file.originalname, ext) + Date.now() + ext);
//     },
//   }),
//   limits: { fileSize: 5 * 1024 * 1024 },
// });

// router.post('/img', isLoggedIn, upload.single('img'), (req, res) => { 
//   console.log(req.file); // 위의 구문을 해석하면, post('/img'로 로그인한사람이 요청하면 업로드 한다 
//   const originalUrl = req.file.location;
//   const url = originalUrl.replace(/\/original\//, '/thumb/');
//   res.json({ url, originalUrl });
// }); 

// 게시글 업로드 부분
const upload2 = multer();
router.post('/', isLoggedIn, upload2.none(), async (req, res, next) => { 
  try {
    console.log(req.user);
    const post = await Post.create({ // await가 있으면 위에 반드시 async가 있어야 한다 
      content: req.body.content, // 업로드가 없다. 옆에 3줄의 바디들만 올라간다 
      img: req.body.url,
      UserId: req.user.id,
      Type: req.body.type, // 여기서부터 우리꺼다. 우리가 브라우저를 통해 보여줄 데이터인데. 여기 라우터를 타고 입력된다.
      Distributor: req.body.Distributor,
      Publisher: req.body.publisher,
      Thumbnail_image: req.body.Thumbnail_image,
      User_url: req.body.User_url,
      Title: req.body.Title
    });
    const hashtags = req.body.content.match(/#[^\s#]*/g);
    if (hashtags) {
      const result = await Promise.all(
        hashtags.map(tag => {
          return Hashtag.findOrCreate({
            where: { title: tag.slice(1).toLowerCase() },
          })
        }),
      );
      await post.addHashtags(result.map(r => r[0]));
    }
    res.status(200).send(post);
  } catch (error) {
    console.error(error);
    next(error);
  }
});

/**
 * 공개 여부를 변경하는 API (현재 질문하기로 프론트 변경)
 */
router.post('/change/public', isLoggedIn, async (req, res) => {
  const postId = req.body.id;
  const isPublic = req.body.isPublic;
  const subTitle = req.body.subTitle;

  const updateValues = {
    Public: isPublic
  };

  // 공개처리시에는 받은 부제목을 넣어 입력한다.
  if (isPublic) {
    updateValues.Subtitle = subTitle;
  }

  await Post.update(updateValues, {
    where: {
      id: postId
    }
  });

  res.sendStatus(200);
});

/**
 * 부제목 수정 라우터
 */
router.post('/subTitle/update', isLoggedIn, async (req, res) => {
  // 게시물 아이디
  const postId = req.body.id;
  // 부제목 내용
  const subTitle = req.body.subTitle;

  // 게시물에 해당하는 부제목을 수정한다.
  await Post.update({
    Subtitle: subTitle
  }, {
    where: {
      id: postId
    }
  });

  // 수정 완료시 메인화면으로 이동시킨다.
  res.sendStatus(200);
});
  


// 나의 게시물 삭제 
router.post('/delete', isLoggedIn, async (req, res) => {
  // 삭제할 게시물 아이디를 파라미터에서 가져온다.
  const postId = req.body.id;
  // 로그인 세션에서 로그인 사용자 아이디를 가져온다.
  const userId = req.session.passport.user;

  const post = await Post.findByPk(postId);
  // 글 작성자가 아니면 에러를 발생시킨다.
  if (post.UserId !== userId) {
    res.status(500).send({ message: '글 작성자만 삭제할 수 있습니다.' });
    return;
  }

  // 글을 삭제시킨다. (deletedAt에 날짜만 넣어진다.)
  await post.destroy();
  res.sendStatus(200);
});

/**
 * 댓글 등록
 */
router.post('/comment', isLoggedIn, async (req, res) => {
  // 댓글 등록할 게시물 아이디
  const postId = req.body.postId;
  // 댓글내용
  const comment = req.body.comment;
  // 로그인 사용자 아이디
  const userId = req.session.passport.user;

  // 코멘트 생성
  await Trendcomment.create({
    userId: userId, // 작성자 유저 아이디
    postId: postId, // 코멘트 달릴 게시물 아이디
    content: comment // 코멘트 내용
  });

  res.sendStatus(200);
});

/**
 * 대댓글 입력
 */
router.post('/comment/child', isLoggedIn, async (req, res) => {
  // 게시물 아이디
  const postId = req.body.postId;
  // 대댓글 다는 댓글 아이디
  const parentCommentId = req.body.parentCommentId;
  // 코멘트 내용
  const comment = req.body.comment;
  // 로그인 아이디
  const userId = req.session.passport.user;

  // 대댓글 내용 저장
  await Comment.create({
    userId: userId, // 작성자 유저 아이디
    postId: postId, // 코멘트 달릴 게시물 아이디
    content: comment, // 코멘트 내용
    parentId: parentCommentId // 대댓글의 경우 대댓글의 부모 댓글 아이디
  });

  res.sendStatus(200);
});

/**
 * 트랜드의 댓글 등록
 */
 router.post('/trendcomment', isLoggedIn, async (req, res) => {
  // 댓글 등록할 게시물 아이디
  const postId = req.body.postId;
  // 댓글내용
  const trendcomment = req.body.trendcomment;
  // 로그인 사용자 아이디
  const userId = req.session.passport.user;

  // 코멘트 생성
  await Trendcomment.create({
    userId: userId, // 작성자 유저 아이디
    postId: postId, // 코멘트 달릴 게시물 아이디
    trend_content: trendcomment // 코멘트 내용
  });

  res.sendStatus(200);
});

/**
 * 대댓글 입력
 */
router.post('/trendcomment/child', isLoggedIn, async (req, res) => {
  // 게시물 아이디
  const postId = req.body.postId;
  // 대댓글 다는 댓글 아이디
  const parentTrendCommentId = req.body.parentTrendCommentId;
  // 코멘트 내용
  const trendcomment = req.body.trendcomment;
  // 로그인 아이디
  const userId = req.session.passport.user;

  // 대댓글 내용 저장
  await Comment.create({
    userId: userId, // 작성자 유저 아이디
    postId: postId, // 코멘트 달릴 게시물 아이디
    trend_content: trendcomment, // 코멘트 내용
    parentId: parentTrendCommentId // 대댓글의 경우 대댓글의 부모 댓글 아이디
  });

  res.sendStatus(200);
});


/**
 * 좋아요/싫어요 등록
 */
router.post('/like', isLoggedIn, async (req, res) => {
  // 댓글 등록할 게시물 아이디
  const postId = req.body.postId;
  // 좋아요/싫어요 데이터
  const like = req.body.like;
  // 로그인 사용자 아이디
  const userId = req.session.passport.user;

  // 기존에 선택한 좋아요/싫어요 데이터가 있으면 중복되지 않도록 삭제처리한다.
  const likeDbData = await Like.findOne({ where: { userId: userId, postId: postId } });
  if (likeDbData != null) {
    await likeDbData.destroy();
  }

  // 좋아요/싫어요 내용 저장
  await Like.create({
    userId: userId, // 유저 아이디
    postId: postId, // 게시물 아이디
    like: like // 좋아요 or 싫어요 (true/false)
  });

  res.sendStatus(200);
});

// 좋아요 삭제 기능  
router.post('/like/delete', isLoggedIn, async (req, res) => {
  // 댓글 등록할 게시물 아이디
  const postId = req.body.postId;
  // 로그인 사용자 아이디
  const userId = req.session.passport.user;

  // 기존에 선택한 좋아요/싫어요 데이터가 있으면 삭제처리한다.
  const likeDbData = await Like.findOne({ where: { userId: userId, postId: postId } });
  if (likeDbData != null) {
    await likeDbData.destroy();
  }

  res.sendStatus(200);
});

// 댓글보기 
// router.get('/:id/', function(req, res){ // 2
//   var commentForm = req.flash('commentForm')[0] || {_id: null, form: {}};
//   var commentError = req.flash('commentError')[0] || { _id:null, parentComment: null, errors:{}};

//   Promise.all([
//       Post.findOne({_id:req.params.id}).populate({ path: 'author', select: 'username' }),
//       Comment.find({post:req.params.id}).sort('createdAt').populate({ path: 'author', select: 'username' })
//     ])
//     .then(([post, comments]) => {
//       res.render('posts/show', { post:post, comments:comments, commentForm:commentForm, commentError:commentError});
//     })
//     .catch((err) => {
//       console.log('err: ', err);
//       return res.json(err);
//     });
// });


// 댓글 대댓글 삭제 
router.post('/comment/delete', isLoggedIn, async (req, res) => {
  const commentId = req.body.commentId;
  const loginUserId = req.session.passport.user;

  // 댓글아이디로 댓글을 조회한다.
  const comment = await Comment.findByPk(commentId);
  // 댓글이 속한 글을 가져온다.
  const post = await comment.getPost();
  // 코멘트가 자신이 썼거나 아니면 트윗글이 자신의 것일때만 삭제가 가능함.
  if (comment != null && comment.userId === loginUserId || post.UserId === loginUserId) {
    await comment.destroy();
    res.sendStatus(200);
  } else {
    res.status(400).send({message: '댓글 삭제를 실패하였습니다. 자신의 글만 삭제가능합니다.'});
  }
});

router.post('/crawling', isLoggedIn, async (req, res) => {
  // post 파라미터로 크롤링할 url 주소를 받는다.
  const url = req.body.url;
  // 세션에서 사용자 아이디를 가져온다.
  const loginUserId = req.session.passport.user;
  // 파이썬을 실행할 자식 프로세스를 생성한다.
  const spawn = require('child_process').spawn;
  // python3을 통해 crawling.py 파이썬 스크립트를 실행한다.
  // 스크립트 파라미터로 url과 userid를 넣어준다.
  const pythonProcess = spawn('python', ['crawling.py', url, loginUserId]);

  // 스크립트 실행 결과가 나오면 콘솔로 찍고 메인으로 리다이렉트 시킨다.
  pythonProcess.stdout.on('data', function(data) {
    console.log(data.toString());
    res.sendStatus(200);
  });
});

/**
 * 글 퍼가기 라우터
 */
router.post('/copy', isLoggedIn, async (req, res) => {
  // 가져오기 할 게시물 아이디
  const postId = req.body.postId;
  const loginUserId = req.session.passport.user;

  const post = await Post.findByPk(postId, {
    raw: true // json 형태로 가져온다.
  });

  // 가져올 게시물이 없으면 에러 발생시킨다.
  if (!post) {
    res.status(400).send({message: '게시물이 존재하지 않습니다.'});
    return;
  }

  // pk값을 삭제한다.
  delete post.id;
  // 내 글로저장하기 떄문에 아이디를 로그인 아이디로 변경한다.
  post.UserId = loginUserId;
  // 생성일, 수정일은 현재날짜로 바꾼다.
  post.createdAt = new Date();
  post.updatedAt = new Date();
  // 기본 비공개로 변경한다.
  post.Public = false;

  // 위에 결과를 가지고 데이터베이스에 데이터를 생성한다.
  await Post.create(post);

  res.sendStatus(200);
});


/**
 * 좋아요, 취소 라우터 
 */
// router.post('/:id/like', async (req, res, next) => {
//   try {
//     const user = await Post.find({ where : { id: req.params.id}});
//     await post.addLiker(req.user.id);
//     res.send('ok');
//   } catch (error) {
//     console.error(error);
//     next(error);
//   }
// });

// router.delete('/:id/like', async (req, res, next) => {
//   try {
//     const post = await Post.find({ where: { id: req.params.id}});
//     await post.
//   }
// })  ......작성 중 



// 트랜드 업로드 부분
const upload3 = multer();
router.post('/trend', isLoggedIn, upload3.none(), async (req, res, next) => { 
  try {
    console.log(req.user);
    const post = await Post.create({ // await가 있으면 위에 반드시 async가 있어야 한다 
      Trend_Thumbnail_image: req.body.Trend_Thumbnail_image,
      Trend_Title: req.body.Trend_Title,
      Trend_SubTitle: req.body.Trend_SubTitle,
      Trend_text: req.body.Trend_text
    });
    
    res.sendStatus(200);
  } catch (error) {
    console.error(error);
    next(error);
  }
});

// 트랜드 불러오기 라우터 
router.get('/trend', async (req, res, next) => { // Post.findAll로 해서 업로드된 게시글들을 찾고
  try {
    const trends = await Trend.findAll({
      include: [
        {
          model: User,
          attributes: ['id', 'nick'],
        },
        {
          model: Trendcomment, // 
          required: false, // 댓글이 게시물에 존재하지 않을수 있으므로 false로 설정한다.
          where: {
            parentId: { // parentId가 없는 댓글은 대댓글이 아니므로 parentId 가 null인 글만 가져온다.
              [Op.eq]: null
            }
          },
          include: [
            {
              model: User, // 댓글 작성자를 알기위해 댓글을 작성한 사용자 정보를 가져온다.
              attributes: ['userid'], // User테이블에서 userid만 조회한다.
            },
            {
              model: Trendcomment, // 댓글의 댓글(대댓글)을 가져오기 위한 댓글에 속한 댓글을 가져온다.
              include: {
                model: User, // 대댓글을 작성한 사용자의 정보를 가져온다.
                attributes: ['userid'], // User테이블에서 userid만 조회한다.
              }
            },
          ]
        },
      ],
      order: [
        ['createdAt', 'DESC'], // 글 작성 최신순
        [Trendcomment, 'createdAt', 'DESC'], // 댓글 작성 최신순
        [Trendcomment, Trendcomment, 'createdAt', 'DESC'], // 대댓글 작성 최신순
      ],
    });

    res.status(200).send(['main', {
      // res.render('main', {
        title: 'NodeBird',
        twits: trends,  // 찾은 게시물들은 twits로 넣어준다
        loginUserId: req.session.passport ? req.session.passport.user : null // 현재 로그인한 유저 아이디를 세션에서가져와 view로 전달한다.
      }]);
  } catch (err) {
    console.error(err);
    next(err);
  }
});



module.exports = router;
