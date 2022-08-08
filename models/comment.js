const Sequelize = require('sequelize');

/**
 * 게시물 댓글 관련 테이블
 * @type {Comment}
 */
module.exports = class Comment extends Sequelize.Model {
    static init(sequelize) {
        return super.init({
            // 코멘트 내용
            content: {
                type: Sequelize.STRING(255),
                allowNull: false,
            },
        }, {
            sequelize,
            timestamps: true, // DB 유저스에 생성 수정 삭제일이 기록
            underscored: false,
            modelName: 'Comment',
            tableName: 'comments',
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
        // 코멘트는 작성된 글에 속해있다.
        db.Comment.belongsTo(db.Post, {
            foreignKey: 'postId'
        });
        // 하나의 글은 여러개의 코멘트를 가지고있다 (일대다)
        db.Post.hasMany(db.Comment, {
            foreignKey: { // FK 설정
                name: 'postId', // FK 컬럼명
                allowNull: false // 코멘트는 글아이디를 가지고 있어야한다.
            }
        });

        // 코멘트는 코멘트 자신을 여러개 가시고 있을수 있다. (대댓글)
        db.Comment.hasMany(db.Comment, {
            foreignKey: {
                name: 'parentId', // FK 컬럼명
                allowNull: true // 대댓글이 없을수도 있으니 null을 허용한다.
            },
            onDelete: 'CASCADE', // 부모 댓글이 삭제되면 하위 댓글도 모두 삭제처리한다.
        });

        // 하나의 코멘트는 사용자에게 속해있다.
        db.Comment.belongsTo(db.User, {
            foreignKey: 'userId' // FK 컬럼명
        });
        // 하나의 사용자는 여러 코멘트를 가지고있다.
        db.User.hasMany(db.Comment, {
            foreignKey: {
                name: 'userId', // FK 컬럼명
                allowNull: false // 코멘트는 작성자를 반드시 가지고있으므로 null허용을 하지않는다.
            },
            onDelete: 'CASCADE', // 사용자가 삭제될시 코멘트도 삭제되게한다.
        });
    }
};
