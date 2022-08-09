const express = require('express');
const { isLoggedIn, isNotLoggedIn } = require('./middlewares');
const { Post, User, Hashtag, Comment, Like} = require('../models');
const Sequelize = require('sequelize');
const Op = Sequelize.Op;

const router = express.Router();

router.use((req, res, next) => {  // 팔로잉 구현 부분
  res.locals.user = req.user;
  res.locals.followerCount = req.user ? req.user.Followers.length : 0;
  res.locals.followingCount = req.user ? req.user.Followings.length : 0;
  res.locals.followerIdList = req.user ? req.user.Followings.map(f => f.id) : [];
  next();
});

router.get('/profile', isLoggedIn, (req, res) => {  // profile.html에서 들어오면 얘가 받는다 
  res.render('profile', { title: '내 정보 - NodeBird' });
});

/**
 * 내 컨텐츠 목록 라우터
 */
router.get('/mycontents', isLoggedIn, async (req, res) => {  
  // 로그인 세션에서 로그인 사용자 아이디를 가져온다.
  const userId = req.session.passport.user;
  // 로그인한 사용자의 게시물만 조회해서 가져온다.
  const posts = await Post.findAll({
    include: {
      model: User,
      attributes: ['id', 'nick'],
      where: {
        id: userId, // 로그인한 사용자의 컨텐츠만 가져오도록 조건절을 넣어준다.
      }
    },
    order: [['createdAt', 'DESC']], // 최신순으로 가져오도록 정렬 조건을 준다.
  });

  res.status(200).send(posts)
  // res.render('mycontents', {
  //   title: '내 컨텐츠 - NodeBird',
  //   twits: posts,
  // });
});

router.get('/join', isNotLoggedIn, (req, res) => {  // join.html에서 들어오면 얘가 받는다 
  res.render('join', { title: '회원가입 - NodeBird' });
});

// 로그인 직후 메인화면에서 전체공개 게시글 및 댓글 보는 백엔드
router.get('/', async (req, res, next) => { // Post.findAll로 해서 업로드된 게시글들을 찾고
  try {
    const posts = await Post.findAll({
      include: [
        {
          model: User,
          attributes: ['id', 'nick'],
        },
        {
          model: Like,
          required: false,
          attributes: ['like'],
        },
        {
          model: Comment, // 댓글도 게시물을 가져올때 같이 가져온다. -> post.Comments 로 접근한다.
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
              model: Comment, // 댓글의 댓글(대댓글)을 가져오기 위한 댓글에 속한 댓글을 가져온다.
              include: {
                model: User, // 대댓글을 작성한 사용자의 정보를 가져온다.
                attributes: ['userid'], // User테이블에서 userid만 조회한다.
              }
            },
          ]
        },
      ],
      where: {
        Public: true // 공개된 게시물만 출력시킨다.
      },
      order: [
        ['createdAt', 'DESC'], // 글 작성 최신순
        [Comment, 'createdAt', 'DESC'], // 댓글 작성 최신순
        [Comment, Comment, 'createdAt', 'DESC'], // 대댓글 작성 최신순
      ],
    });

    res.status(200).send(['main', {
      // res.render('main', {
        title: 'NodeBird',
        twits: posts,  // 찾은 게시물들은 twits로 넣어준다
        loginUserId: req.session.passport ? req.session.passport.user : null // 현재 로그인한 유저 아이디를 세션에서가져와 view로 전달한다.
      }]);
  } catch (err) {
    console.error(err);
    next(err);
  }
});


// 댓글 대댓글만 불러오는 라우터 
router.get('/comment', async (req, res, next) => { // Post.findAll로 해서 업로드된 게시글들을 찾고
  try {
    const posts = await Post.findAll({
      include: [
        {
          model: User,
          attributes: ['id', 'nick'],
        },
        {
          model: Comment, // 댓글도 게시물을 가져올때 같이 가져온다. -> post.Comments 로 접근한다.
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
              model: Comment, // 댓글의 댓글(대댓글)을 가져오기 위한 댓글에 속한 댓글을 가져온다.
              include: {
                model: User, // 대댓글을 작성한 사용자의 정보를 가져온다.
                attributes: ['userid'], // User테이블에서 userid만 조회한다.
              }
            },
          ]
        },
      ],
      where: {
        Public: true // 공개된 게시물만 출력시킨다.
      },
      order: [
        ['createdAt', 'DESC'], // 글 작성 최신순
        [Comment, 'createdAt', 'DESC'], // 댓글 작성 최신순
        [Comment, Comment, 'createdAt', 'DESC'], // 대댓글 작성 최신순
      ],
    });    

    res.status(200).send(['main', {
      // res.render('main', {
        title: 'NodeBird',
        twits: posts,  // 찾은 게시물들은 twits로 넣어준다
        loginUserId: req.session.passport ? req.session.passport.user : null // 현재 로그인한 유저 아이디를 세션에서가져와 view로 전달한다.
      }]);
  } catch (err) {
    console.error(err);
    next(err);
  }
}); 

router.get('/hashtag', async (req, res, next) => {
  const query = req.query.hashtag;
  if (!query) {
    return res.redirect('/');
  }
  try {
    const hashtag = await Hashtag.findOne({ where: { title: query } });
    let posts = [];
    if (hashtag) {
      posts = await hashtag.getPosts({ include: [{ model: User }] });
    }

    return res.render('main', {
      title: `${query} | NodeBird`,
      twits: posts,
    });
  } catch (error) {
    console.error(error);
    return next(error);
  }
});

router.get('/user/search', isLoggedIn, async (req, res) => {
  // 사용자가 입력한 검색어를 가져온다.
  const searchText = req.query.searchText;
  // where 조건에 넣어줄 데이터를 저장할 객체를 생성한다.
  const search = { };
  // 사용자가 입력한 검색어가 있으면 nick 컬럼을 기준으로 like검색을한다.
  if (searchText != null) {
    search.nick = {
      [Op.like]: '%' + searchText + '%'
    }
  }

  // 전체 사용자 정보를 데이터베이스에서 검색한다.
  const users = await User.findAll({
    attributes: {
      // createdAt, updatedAt 날짜 정보를 보기 좋게 dateformat 해서 가져온다.
      include: [
        [Sequelize.fn ("DATE_FORMAT", Sequelize.col("createdAt"), "%Y-%m-%d %H:%i:%s"), "createdAt"],
        [Sequelize.fn ("DATE_FORMAT", Sequelize.col("updatedAt"), "%Y-%m-%d %H:%i:%s"), "updatedAt"],
      ]
    },
    // 위에서 설정한 검색 객체를 where 조건에 넣는다.
    where: search
  });
  res.status(200).send(users, searchText);
});

router.get('/twit/search', isLoggedIn, async (req, res) => {
  // 사용자가 입력한 검색어를 가져온다.
  const searchText = req.query.searchText;
  // where 조건에 넣어줄 데이터를 저장할 객체를 생성한다.
  const search = { Public: true };  // 공개된 게시물만 출력시킨다.
  // 사용자가 입력한 검색어가 있으면 Title, Type, Publisher, Distributor 컬럼을 기준으로 like검색을 OR로 연결하여 검색한다.
  if (searchText != null) {
    search[Op.or] = [
      { Title: { [Op.like]: '%' + searchText + '%' } },
      { Type: { [Op.like]: '%' + searchText + '%' } },
      { Publisher: { [Op.like]: '%' + searchText + '%' } },
      { Distributor: { [Op.like]: '%' + searchText + '%' } },
    ];
  }

  const posts = await Post.findAll({
    include: {
      model: User,
    },
    // 위에서 설정한 검색 객체를 where 조건에 넣는다.
    where: search,
    order: [['createdAt', 'DESC']], // 최신순으로 가져오도록 정렬 조건을 준다.
  });

  res.status(200).send(posts, searchText);
});

module.exports = router;
