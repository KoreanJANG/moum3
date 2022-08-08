const Sequelize = require('sequelize');
const env = process.env.NODE_ENV || 'development';
const config = require('../config/config')[env];
const User = require('./user');
const Post = require('./post');
const Hashtag = require('./hashtag');
const Comment = require('./comment');
const Like = require('./like');
const Trend = require('./trend');

const db = {};
const sequelize = new Sequelize(
  config.database, config.username, config.password, config,
);

db.sequelize = sequelize;  //테이블구조를 잠깐 보자 
db.User = User;   // 유저와 게시글은 1:다 .   사용자와 사용자(팔로워)는 다:다
db.Post = Post;  // 게시글과 헤시테그는 다:다
db.Hashtag = Hashtag;  // 위의 관계는 모델스안에 각각의 js 에서 정의한다 
db.Comment = Comment;
db.Like = Like;
db.Trend = Trend;

User.init(sequelize);
Post.init(sequelize);
Hashtag.init(sequelize);
Comment.init(sequelize);
Like.init(sequelize);
Trend.init(sequelize);

User.associate(db);
Post.associate(db);
Hashtag.associate(db);
Comment.associate(db);
Like.associate(db);
Trend.associate(db);

module.exports = db;
