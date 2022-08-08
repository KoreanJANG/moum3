const Sequelize = require('sequelize');

module.exports = class Post extends Sequelize.Model {
  static init(sequelize) {
    return super.init({
      content: {
        type: Sequelize.STRING(100),
        allowNull: false,
      },
      img: {  // 이미지 한 개 만 올릴수 있게 만든다. 
        type: Sequelize.STRING(100),
        allowNull: true,
      },

      // 중요!!!! 여기서 부터는 우리가 가져오려는 컨텐츠에 관련된 db이다. 우리의 컬럼을 참고하라 
      Type : {
        type: Sequelize.STRING(100),
        allowNull: true,  // 널을 허락한다 
      },

      Category_in : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Distributor : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Publisher : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Category_out : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Logo_image : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Channel_logo : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Thumbnail_image : {
        type: Sequelize.STRING(2000),
        allowNull: true,
      },
      User_url : {
        type: Sequelize.STRING(1000),
        allowNull: true,
      },
      Title : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Maker : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Date : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Summary : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      crawl_Content : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Emotion_cnt : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Comm_cnt : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      // ALTER TABLE posts MODIFY COLUMN Description varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL;
      Description : {
        type: Sequelize.STRING(2000),
        allowNull: true,
      },
      Comment : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Tag : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      View_cnt : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Duration : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Lower_price : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Lower_mall : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Lower_price_card : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Lower_mall_card : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Star_cnt : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Review_cnt : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Review_content : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Dscnt_rate : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Origin_price : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Dlvry_price : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Dlvry_date : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Model_no : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Color : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Location : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Title_searched : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Lower_price_searched : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Lower_mall_searched : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      // ALTER TABLE posts MODIFY COLUMN Lower_url_searched varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL;
      Lower_url_searched : {
        type: Sequelize.STRING(2000),
        allowNull: true,
      },
      // 변경 쿼리 : ALTER TABLE posts ADD Public1 TINYINT(1) DEFAULT false NOT NULL;
      // 공개여부컬럼 -> 기본값 false
      Public: {
        type: Sequelize.BOOLEAN,
        defaultValue: false,
      },
      Subtitle : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },

    }, {
      sequelize,
      timestamps: true,
      underscored: false,
      modelName: 'Post',
      tableName: 'posts',
      // 게시물은 실제 삭제하지 않고 deletedAt에 날짜를 넣다.
      // 수동 쿼리로 컬럼 생성 - ALTER TABLE posts ADD deletedAt DATETIME NULL;
      paranoid: true,
      charset: 'utf8mb4',  // 이모티콘 가능 
      collate: 'utf8mb4_general_ci',
    });
  }

  static associate(db) {
    db.Post.belongsTo(db.User); //게시글은 유저에 속한다. 헤즈매니하고 벨롱스투 는 같이 써주면 안햇갈린다 
    db.Post.belongsToMany(db.Hashtag, { through: 'PostHashtag' });//다:다 관계일때 쓴다. through를 써서 중간 테이블을 정의 
  }
};
