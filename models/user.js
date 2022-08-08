const Sequelize = require('sequelize');

module.exports = class User extends Sequelize.Model {
  static init(sequelize) {
    return super.init({
      userid: {
        type: Sequelize.STRING(40), // 한번 생성 후 여기서 수정한다고 DB를 수정해 주지는 않는다
        allowNull: true,            // 여기 수정하고 DB가서 또 수정해라 
        unique: true,
      },
      nick: {
        type: Sequelize.STRING(15),
        allowNull: false,
      },
      password: {
        type: Sequelize.STRING(100),
        allowNull: true,  //요즘엔 비밀번호 없을수도 있다. sns로 가입하면 비밀번호 없다 
      },
      provider: {  // 로그인 제공자
        type: Sequelize.STRING(10),
        allowNull: false,
        defaultValue: 'local',  // 로컬아니면 일단 여기서는 카카오. 로컬이면 일반 로그인일 것이다 
      },
      snsid: {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      email: {
        type: Sequelize.STRING(30),
        allowNull: true,
      },
      mobile: {
        type: Sequelize.STRING(20),
        allowNull: true,
      },
      birthday: {
        type: Sequelize.STRING(10),
        allowNull: true,
      },
      age: {
        type: Sequelize.STRING(3),
        allowNull: true,
      },
      
      
    }, {
      sequelize,
      timestamps: true, // DB 유저스에 생성 수정 삭제일이 기록 
      underscored: false, 
      modelName: 'User',
      tableName: 'users',
      paranoid: true, // 딜리티드엣에 기록만 되고 삭제하면 삭제안하고 한 척 한다 
      charset: 'utf8',  // 한글 
      collate: 'utf8_general_ci',
    });
  }

  static associate(db) {  // 모델들간의 관계들을 associate를 써서 작성한다 
    db.User.hasMany(db.Post); // 유저는 많은 게시글을 가진다 
    db.User.belongsToMany(db.User, {
      foreignKey: 'followingId', // foreignKey랑 as는 반대의미 
      as: 'Followers', // 팔로워를 가져올때  
      through: 'Follow',
    });
    db.User.belongsToMany(db.User, {  // 팔로잉 팔로워 관계. 다:다
      foreignKey: 'followerId',
      as: 'Followings',
      through: 'Follow',
    });
  }
};
