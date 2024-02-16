const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');

require('models/AvailableRides');
const AvailableRide = mongoose.model('ride');

// Root route
router.get('/', (req, res) => {
    res.send('Welcome');
});

// Gets all "available" rides, but this is just the name I used because rides will have more data -
//then what I want to show on the first screen, and I don't want to filter it out.
router.get('/availableRides', async (req, res) => {
    const rides = await AvailableRide.find();
    res.json(rides);
});

module.exports = router;