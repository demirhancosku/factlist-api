const env = process.env.NODE_ENV || 'development';
const config = {
  development: {
    username: 'root',
    password: '',
    logging: false,
    database: 'factlist-api',
    host: 'localhost',
    dialect: 'mysql',
    timezone: '+00:00',
    define: {
      paranoid: true,
      timestamps: true,
      freezeTableName: true,
      underscored: true
    },
    server: {
      port: process.env.port || 4000
    },
    auth: {
      tokenLifeTime: '1h',
      jwtSecret: 'secretKey',
      twitter: {
        consumerKey: 'your-consumer-key-here',
        consumerSecret: 'your-client-secret-here',
        callbackURL: 'http://localhost:4000/auth/twitter/callback'
      }
    },
    logLevel: 'debug'
  },

  docker: {
    username: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    logging: false,
    database: process.env.DB_NAME,
    host: process.env.DB_HOST,
    dialect: 'mysql',
    timezone: '+00:00',
    define: {
      paranoid: true,
      timestamps: true,
      freezeTableName: true,
      underscored: true
    },
    server: {
      port: process.env.port || 4000
    },
    auth: {
      tokenLifeTime: '1h',
      jwtSecret: 'secretKey',
      twitter: {
        consumerKey: 'your-consumer-key-here',
        consumerSecret: 'your-client-secret-here',
				callbackURL: 'http://localhost:4000/auth/twitter/callback'

      }
    }
  },

  test: {
    username: 'root',
    password: '',
    logging: false,
    database: 'factlist-api',
    host: 'localhost',
    dialect: 'mysql',
    timezone: '+00:00',
    define: {
      paranoid: true,
      timestamps: true,
      freezeTableName: true,
      underscored: true
    },
    server: {
      port: process.env.port || 4000
    },
    auth: {
      tokenLifeTime: '1h',
      jwtSecret: 'secretKey',
      twitter: {
        consumerKey: 'your-consumer-key-here',
        consumerSecret: 'your-client-secret-here',
				callbackURL: 'http://localhost:4000/auth/twitter/callback'
      }
    },
    logLevel: 'info'
  },

  production: {
    username: 'root',
    password: '',
    logging: false,
    database: 'factlist-api',
    host: process.env.DB_HOST,
    dialect: 'mysql',
    timezone: '+00:00',
    define: {
      paranoid: true,
      timestamps: true,
      freezeTableName: true,
      underscored: true
    },
    server: {
      port: process.env.port || 4000
    },
    auth: {
      tokenLifeTime: '1h',
      jwtSecret: 'secretKey',
      twitter: {
        consumerKey: 'your-consumer-key-here',
        consumerSecret: 'your-client-secret-here',
				callbackURL: 'http://localhost:4000/auth/twitter/callback'

      }
    }
  },
  logLevel: 'error'
};

module.exports = config[env];
