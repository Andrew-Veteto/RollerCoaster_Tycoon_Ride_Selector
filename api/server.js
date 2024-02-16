// Stuff neeeded for the api
require('dotenv').config();
require('app-module-path').addPath(__dirname);
const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');

// Routes
const formRouter = require('../api/routes/index');
const apiRouter = require('../api/routes/api/v1/index');

// App initalization
const app = express();

// View engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

// Connect to Mongo via mongoose
mongoose.set('strictQuery', false);
mongoose.connect(process.env.MONGO_CONNECTION_STRING, {})
.then( () => console.log('MongoDB Connected'))
.catch( error => console.error(error));

// MiddleWare
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(cors());
app.use(bodyParser.urlencoded({ extended: true}));
app.use('/', formRouter);
app.use('/api/v1', apiRouter);

module.exports = app;