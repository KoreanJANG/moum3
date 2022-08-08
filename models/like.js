const Sequelize = require('sequelize');

/**
 * 게시물 댓글 관련 테이블
 * @type {Like}
 */
module.exports = class Like extends Sequelize.Model {
    static init(sequelize) {
        return super.init({
            // 좋아요 여부(불린으로 처리)
            like: {
                type: Sequelize.BOOLEAN,
                defaultValue: false,
            },
        }, {
            sequelize,
            timestamps: true, // DB 유저스에 생성 수정 삭제일이 기록
            underscored: false,
            modelName: 'Like',
            tableName: 'likes',
            paranoid: false, // 살제로 삭제한다.
            charset: 'utf8',  // 한글
            collate: 'utf8_general_ci',
        });
    }

    /**
     * 테이블 연관 정의
     * @param db
     */
    static associate(db) {
        // 좋아요는 질문하기 게시글에 속해있다.
        db.Like.belongsTo(db.Post, {
            foreignKey: 'postId'
        });
        // 하나의 글은 여러개의 좋아요를 가지고있다 (일대다)
        db.Post.hasMany(db.Like, {
            foreignKey: { // FK 설정
                name: 'postId', // FK 컬럼명
                allowNull: false // 좋아요는 반드시 포스트아이디를 가지고 있어야한다.
            }
        });

        // 하나의 좋아요는 사용자에게 속해있다.
        db.Like.belongsTo(db.User, {
            foreignKey: 'userId' // FK 컬럼명
        });
        // 하나의 사용자는 여러 좋아요를 가지고있다.
        db.User.hasMany(db.Like, {
            foreignKey: {
                name: 'userId', // FK 컬럼명
                allowNull: false // 좋아요 생성자는 반드시 가지고있으므로 null허용을 하지않는다.
            },
        });
    }
};
